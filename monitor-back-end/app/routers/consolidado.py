from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from .status import (
    evaluate_web_status, evaluate_db_status,
    evaluate_dns_status, evaluate_smtp_status
)

router = APIRouter(prefix="/status", tags=["Consolidado"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/consolidado")
def get_consolidado(db: Session = Depends(get_db)):

    # Últimos alertas (não usados no front, mas backend mantém)
    alerts = (
        db.query(models.Alert)
        .order_by(models.Alert.created_at.desc())
        .limit(5)
        .all()
    )

    services = db.query(models.Service).all()
    latencias = []
    overall_status_levels = []   # green=1, yellow=2, red=3

    for s in services:

        # 🔥 BUSCA CORRETA da última latency_ms
        latency_metric = (
            db.query(models.Metric)
            .filter(
                models.Metric.service_id == s.id,
                models.Metric.metric_name == "latency_ms"
            )
            .order_by(models.Metric.timestamp.desc())
            .first()
        )

        if latency_metric:
            try:
                latencias.append(float(latency_metric.value))
            except:
                pass

        # pegar todas as métricas recentes para avaliação do status
        latest_metrics = (
            db.query(models.Metric)
            .filter(models.Metric.service_id == s.id)
            .order_by(models.Metric.timestamp.desc())
            .all()
        )

        metrics_dict = {}
        for m in latest_metrics:
            if m.metric_name not in metrics_dict:
                metrics_dict[m.metric_name] = m.value

        # status por serviço
        if s.key == "web":
            status, _ = evaluate_web_status(metrics_dict)
        elif s.key == "db":
            status, _ = evaluate_db_status(metrics_dict)
        elif s.key == "dns":
            status, _ = evaluate_dns_status(metrics_dict)
        elif s.key == "smtp":
            status, _ = evaluate_smtp_status(metrics_dict)
        else:
            status = "green"

        # convert to numeric level
        level = 1 if status == "green" else 2 if status == "yellow" else 3
        overall_status_levels.append(level)

    # média real de latência entre os serviços
    media_latencia = sum(latencias) / len(latencias) if latencias else 0

    # status geral
    if 3 in overall_status_levels:
        health = "red"
    elif 2 in overall_status_levels:
        health = "yellow"
    else:
        health = "green"

    return {
        "health": health,
        "media_latencia": round(media_latencia, 2),
        "alertas": [
            {
                "servico": a.service_name,
                "mensagem": a.message,
                "nivel": a.level,
                "quando": a.created_at,
            }
            for a in alerts
        ],
    }
