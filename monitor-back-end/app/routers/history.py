from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

router = APIRouter(prefix="/metrics/history", tags=["Metrics History"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{service_key}")
def get_metrics_history(service_key: str, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.key == service_key).first()

    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    # Pega as últimas 50 métricas 
    metrics = (
        db.query(models.Metric)
        .filter(models.Metric.service_id == service.id)
        .order_by(models.Metric.timestamp.desc())
        .limit(50)
        .all()
    )


    response = [
        {
            "metric": m.metric_name,
            "value": m.value,
            "timestamp": m.timestamp,
        }
        for m in reversed(metrics) 
    ]

    return response
