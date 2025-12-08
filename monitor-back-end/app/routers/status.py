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


# pega últimas métricas por serviço (uma por nome)
def get_latest_metrics(db: Session, service_id: int):
    metrics = (
        db.query(models.Metric)
        .filter(models.Metric.service_id == service_id)
        .order_by(models.Metric.timestamp.desc())
        .all()
    )

    latest = {}
    for m in metrics:
        # só pega a métrica mais recente de cada tipo
        if m.metric_name not in latest:
            latest[m.metric_name] = m.value

    return latest


# status do banco
def evaluate_db_status(metrics):
    cpu = metrics.get("cpu_usage", 0)
    mem = metrics.get("memory_mb", 0)
    roll = metrics.get("rollback_rate", 0)
    disk = metrics.get("disk_latency_ms", 0)
    slow = metrics.get("slow_queries", 0)
    conn = metrics.get("open_connections", 0)
    avail = metrics.get("availability", 1)

    # segurança
    auth_fail = metrics.get("auth_failures", 0)
    vuln = metrics.get("known_vulnerability", 0)
    config_change = metrics.get("config_change", 0)

    # vermelho
    if (
        avail == 0 or roll > 0.03 or cpu > 90 or mem > 3500 or
        disk > 20 or slow > 10 or conn > 250 or
        auth_fail > 5 or vuln == 1 or config_change == 1
    ):
        return "red", "Banco crítico: desempenho degradado ou problema de segurança detectado."

    # amarelo
    if (
        0.01 <= roll <= 0.03 or 70 < cpu <= 90 or
        2500 < mem <= 3500 or 10 < disk <= 20 or
        5 < slow <= 10 or 150 < conn <= 250 or
        auth_fail > 0
    ):
        return "yellow", "Banco apresenta degradação moderada."

    return "green", None


# status web server
def evaluate_web_status(metrics):
    latency = metrics.get("latency_ms", 0)
    error_rate = metrics.get("error_rate", 0)
    availability = metrics.get("availability", 1)

    anomaly = metrics.get("traffic_anomaly", 0)
    auth_fail = metrics.get("auth_failures", 0)
    vuln = metrics.get("known_vulnerability", 0)
    config_change = metrics.get("config_change", 0)

    # vermelho
    if availability == 0:
        return "red", "Web server fora do ar."
    if latency > 2000 or error_rate > 0.10:
        return "red", "Web crítico: latência extremamente alta ou muitos erros."
    if anomaly == 1 or vuln == 1 or config_change == 1:
        return "red", "Alerta de segurança: tráfego anômalo, vulnerabilidade ou mudança suspeita."

    # amarelo
    if latency > 1000 or error_rate > 0.02:
        return "yellow", "Web degradado: latência alta ou taxa de erro elevada."
    if auth_fail > 5:
        return "yellow", "Falhas de autenticação acima do esperado."

    return "green", None


# status dns
def evaluate_dns_status(metrics):
    latency = metrics.get("latency_ms", 0)
    failures = metrics.get("failures", 0)

    anomaly = metrics.get("traffic_anomaly", 0)
    vuln = metrics.get("known_vulnerability", 0)
    config_change = metrics.get("config_change", 0)

    # vermelho
    if latency > 150 or failures > 0.05 or anomaly == 1 or vuln == 1 or config_change == 1:
        return "red", "DNS crítico: falhas, lentidão ou evento de segurança detectado."

    # amarelo
    if latency > 80 or failures > 0.01:
        return "yellow", "DNS degradado: lentidão ou taxa de falhas acima do normal."

    return "green", None

# status do smtp
def evaluate_smtp_status(metrics):
    queue = metrics.get("queue_length", 0)
    throughput = metrics.get("throughput", 1)
    errors = metrics.get("errors", 0)

    vuln = metrics.get("known_vulnerability", 0)
    auth_fail = metrics.get("auth_failures", 0)
    config_change = metrics.get("config_change", 0)

    # vermelho
    if errors > 5 or queue > 30 or throughput < 1 or vuln == 1 or config_change == 1:
        return "red", "SMTP crítico: fila alta, erros ou alerta de segurança."

    # amarelo
    if errors > 1 or queue > 10 or auth_fail > 0:
        return "yellow", "SMTP degradado: erros moderados ou falhas de autenticação."

    return "green", None



# endpoint status/{service}
@router.get("/{service_key}")
def service_status(service_key: str, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.key == service_key).first()

    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    metrics = get_latest_metrics(db, service.id)

    # decidir avaliador
    if service_key == "db":
        status, msg = evaluate_db_status(metrics)
    elif service_key == "web":
        status, msg = evaluate_web_status(metrics)
    elif service_key == "dns":
        status, msg = evaluate_dns_status(metrics)
    elif service_key == "smtp":
        status, msg = evaluate_smtp_status(metrics)
    else:
        status, msg = "green", None

    # prepara alerta para resposta
    alert = (
        {"level": 3 if status == "red" else 2 if status == "yellow" else 1, "message": msg}
        if msg else None
    )

    # envia e-mail apenas em casos críticos
    if status == "red" and msg:
        send_alert_email(service.name, msg, status)

    return {
        "service": service.key,
        "name": service.name,
        "status": status,
        "metrics": metrics,
        "last_alert": alert
    }

@router.get("/dashboard/all")
def dashboard_view(db: Session = Depends(get_db)):
    services = db.query(models.Service).all()
    result = []

    for s in services:
        metrics = get_latest_metrics(db, s.id)

        # avalia status + mensagem
        if s.key == "db":
            status, msg = evaluate_db_status(metrics)
        elif s.key == "web":
            status, msg = evaluate_web_status(metrics)
        elif s.key == "dns":
            status, msg = evaluate_dns_status(metrics)
        elif s.key == "smtp":
            status, msg = evaluate_smtp_status(metrics)
        else:
            status, msg = "green", None

        # envia email automaticamente
        if status == "red" and msg:
            send_alert_email(s.name, msg, status)

        result.append({
            "key": s.key,
            "name": s.name,
            "status": status
        })

    return result
