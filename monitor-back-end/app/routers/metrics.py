from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas, alerts   

router = APIRouter(prefix="/metrics", tags=["Metrics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ingest")
def ingest_metric(metric: schemas.MetricCreate, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.key == metric.service_key).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    m = models.Metric(
        service_id=service.id,
        metric_name=metric.metric_name,
        value=metric.value,
        unit=metric.unit,
    )
    db.add(m)
    db.commit()


    alerts.evaluate_service(db, service)

    return {"status": "ok", "metric": metric}

@router.get("/latest/{service_key}", response_model=list[schemas.MetricRead])
def latest_metrics(service_key: str, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.key == service_key).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    metrics = (
        db.query(models.Metric)
        .filter(models.Metric.service_id == service.id)
        .order_by(models.Metric.timestamp.desc())
        .limit(50)
        .all()
    )

    return metrics
