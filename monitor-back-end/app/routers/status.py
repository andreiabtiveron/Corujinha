from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from ..email_sender import send_alert_email

router = APIRouter(prefix="/status", tags=["Status"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_latest_metrics(db: Session, service_id: int):
    metrics = (
        db.query(models.Metric)
        .filter(models.Metric.service_id == service_id)
        .order_by(models.Metric.timestamp.desc())
        .all()
    )

    latest = {}
    for m in metrics:
        if m.metric_name not in latest:  # pega a mais recente de cada tipo
            latest[m.metric_name] = m.value

    return latest



# Avaliação de STATUS — WEB
def evaluate_web_status(metrics):
    latency = float(metrics.get("latency_ms", 0))
    error_rate = float(metrics.get("error_rate", 0))
    availability = metrics.get("availability", 1)

    anomaly = metrics.get("traffic_anomaly", 0)
    auth_fail = metrics.get("auth_failures", 0)
    vuln = metrics.get("known_vulnerability", 0)
    config_change = metrics.get("config_change", 0)

    if availability == 0:
        return "red", "Web server fora do ar."

    if latency > 2000 or error_rate > 0.10:
        return "red", "Web crítico: latência extrema ou erros."

    if anomaly == 1 or vuln == 1 or config_change == 1:
        return "red", "Alerta de segurança detectado."

    if latency > 1000 or error_rate > 0.02:
        return "yellow", "Web degradado."

    if auth_fail > 5:
        return "yellow", "Falhas de autenticação elevadas."

    return "green", None


# Avaliação de STATUS — DB
def evaluate_db_status(metrics):
    cpu = float(metrics.get("cpu_usage", 0))
    mem = float(metrics.get("memory_mb", 0))
    roll = float(metrics.get("rollback_rate", 0))
    disk = float(metrics.get("disk_latency_ms", 0))
    slow = float(metrics.get("slow_queries", 0))
    conn = float(metrics.get("open_connections", 0))
    avail = metrics.get("availability", 1)

    auth_fail = metrics.get("auth_failures", 0)
    vuln = metrics.get("known_vulnerability", 0)
    config_change = metrics.get("config_change", 0)

    if (
        avail == 0 or roll > 0.03 or cpu > 90 or mem > 3500 or
        disk > 20 or slow > 10 or conn > 250 or
        auth_fail > 5 or vuln == 1 or config_change == 1
    ):
        return "red", "Banco crítico."

    if (
        0.01 <= roll <= 0.03 or
        70 < cpu <= 90 or
        2500 < mem <= 3500 or
        10 < disk <= 20 or
        5 < slow <= 10 or
        150 < conn <= 250 or
        auth_fail > 0
    ):
        return "yellow", "Banco degradado."

    return "green", None



# Avaliação de STATUS — DNS
def evaluate_dns_status(metrics):
    latency = float(metrics.get("latency_ms", 0))
    failures = float(metrics.get("failures", 0))

    anomaly = metrics.get("traffic_anomaly", 0)
    vuln = metrics.get("known_vulnerability", 0)
    config_change = metrics.get("config_change", 0)

    if latency > 150 or failures > 0.05 or anomaly == 1 or vuln == 1 or config_change == 1:
        return "red", "DNS crítico."

    if latency > 80 or failures > 0.01:
        return "yellow", "DNS degradado."

    return "green", None



# Avaliação de STATUS — SMTP
def evaluate_smtp_status(metrics):
    queue = float(metrics.get("queue_length", 0))
    throughput = float(metrics.get("throughput", 1))
    errors = float(metrics.get("errors", 0))

    vuln = metrics.get("known_vulnerability", 0)
    auth_fail = metrics.get("auth_failures", 0)
    config_change = metrics.get("config_change", 0)

    if errors > 5 or queue > 30 or throughput < 1 or vuln == 1 or config_change == 1:
        return "red", "SMTP crítico."

    if errors > 1 or queue > 10 or auth_fail > 0:
        return "yellow", "SMTP degradado."

    return "green", None



# Endpoint: status/service/{service_key}
@router.get("/service/{service_key}")
def service_status(service_key: str, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.key == service_key).first()

    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    metrics = get_latest_metrics(db, service.id)

    if service_key == "web":
        status, msg = evaluate_web_status(metrics)
    elif service_key == "db":
        status, msg = evaluate_db_status(metrics)
    elif service_key == "dns":
        status, msg = evaluate_dns_status(metrics)
    elif service_key == "smtp":
        status, msg = evaluate_smtp_status(metrics)
    else:
        status, msg = "green", None

    return {
        "service": service.key,
        "name": service.name,
        "status": status,
        "metrics": metrics,
        "last_alert": {
            "level": 3 if status == "red" else 2 if status == "yellow" else 1,
            "message": msg,
        } if msg else None
    }



# Endpoint: status/dashboard/all
@router.get("/dashboard/all")
def dashboard_view(db: Session = Depends(get_db)):
    services = db.query(models.Service).all()
    result = []

    for s in services:
        metrics = get_latest_metrics(db, s.id)

        if s.key == "web":
            status, msg = evaluate_web_status(metrics)
        elif s.key == "db":
            status, msg = evaluate_db_status(metrics)
        elif s.key == "dns":
            status, msg = evaluate_dns_status(metrics)
        elif s.key == "smtp":
            status, msg = evaluate_smtp_status(metrics)
        else:
            status, msg = "green", None

        print(f">>> STATUS CALCULADO: {s.key} → {status}")

        # ENVIA EMAIL DE ALERTA 
        if status == "red" and msg:
            send_alert_email(s.name, msg, status)

        result.append({
            "key": s.key,
            "name": s.name,
            "status": status
        })

    return result
