from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

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
        if m.metric_name not in latest:
            latest[m.metric_name] = m.value

    return latest

def get_last_alert(db: Session, service_id: int):
    return (
        db.query(models.Alert)
        .filter(models.Alert.service_id == service_id)
        .order_by(models.Alert.created_at.desc())
        .first()
    )

@router.get("/{service_key}")
def service_status(service_key: str, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.key == service_key).first()

    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    metrics = get_latest_metrics(db, service.id)
    alert = get_last_alert(db, service.id)

    if alert:
        if alert.level == 1:
            status = "green"
        elif alert.level == 2:
            status = "yellow"
        else:
            status = "red"
    else:
        status = "green"

    return {
        "service": service.key,
        "name": service.name,
        "status": status,
        "metrics": metrics,
        "last_alert": {
            "level": alert.level,
            "message": alert.message
        } if alert else None
    }

# ================================================
# DASHBOARD CONSOLIDADO
# ================================================

@router.get("/dashboard/all")
def dashboard_view(db: Session = Depends(get_db)):
    services = db.query(models.Service).all()
    result = []

    for s in services:
        alert = get_last_alert(db, s.id)

        if alert:
            if alert.level == 1:
                status = "green"
            elif alert.level == 2:
                status = "yellow"
            else:
                status = "red"
        else:
            status = "green"

        result.append({
            "key": s.key,
            "name": s.name,
            "status": status
        })

    return result
