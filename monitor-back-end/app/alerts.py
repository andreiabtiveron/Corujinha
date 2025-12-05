from sqlalchemy.orm import Session
from . import models

WEB_THRESHOLDS = {
    "latency_ms": {"yellow": 200, "red": 500},
    "error_rate": {"yellow": 0.01, "red": 0.05},
}

def evaluate_web_alerts(db: Session, service: models.Service):
    last_latency = (
        db.query(models.Metric)
        .filter(
            models.Metric.service_id == service.id,
            models.Metric.metric_name == "latency_ms",
        )
        .order_by(models.Metric.timestamp.desc())
        .first()
    )

    last_error = (
        db.query(models.Metric)
        .filter(
            models.Metric.service_id == service.id,
            models.Metric.metric_name == "error_rate",
        )
        .order_by(models.Metric.timestamp.desc())
        .first()
    )

    level = 1
    messages = []

    if last_latency and last_latency.value > WEB_THRESHOLDS["latency_ms"]["yellow"]:
        level = 2
        messages.append(f"Latência elevada ({last_latency.value:.0f} ms)")

    if last_latency and last_latency.value > WEB_THRESHOLDS["latency_ms"]["red"]:
        level = 3

    if last_error and last_error.value > WEB_THRESHOLDS["error_rate"]["yellow"]:
        level = max(level, 2)
        messages.append(f"Taxa de erro elevada ({last_error.value*100:.1f}%)")

    if last_error and last_error.value > WEB_THRESHOLDS["error_rate"]["red"]:
        level = max(level, 3)

    if level > 1 and messages:
        alert = models.Alert(
            service_id=service.id,
            level=level,
            message="; ".join(messages),
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    return None
