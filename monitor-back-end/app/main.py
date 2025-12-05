from fastapi import FastAPI
from .database import Base, engine, SessionLocal
from . import models
from .routers import metrics, services, alerts, status

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Monitor API")

def seed_services():
    db = SessionLocal()
    if db.query(models.Service).count() == 0:
        services_to_add = [
            models.Service(name="Web Server", key="web", type="HTTP", host="https://google.com", port=443),
            models.Service(name="Database", key="db", type="DB", host="localhost", port=5432),
            models.Service(name="DNS", key="dns", type="DNS", host="8.8.8.8", port=53),
            models.Service(name="SMTP", key="smtp", type="SMTP", host="smtp.mailtrap.io", port=587),
        ]
        db.add_all(services_to_add)
        db.commit()
    db.close()

seed_services()

app.include_router(metrics.router)  # /metrics
app.include_router(services.router)# /services
app.include_router(alerts.router) # /alerts
app.include_router(status.router) # /status