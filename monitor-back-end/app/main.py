from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from . import models
from .routers import metrics, services, alerts, status, history, consolidado

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# ---------------------------------------------
# FUNÇÃO PRECISA ESTAR DEFINIDA ANTES DO STARTUP
# ---------------------------------------------
def seed_services():
    db = SessionLocal()
    try:
        if db.query(models.Service).count() == 0:
            services_to_add = [
                models.Service(name="Web Server", key="web", type="HTTP", host="https://google.com", port=443),
                models.Service(name="Database", key="db", type="DB", host="localhost", port=5432),
                models.Service(name="DNS", key="dns", type="DNS", host="8.8.8.8", port=53),
                models.Service(name="SMTP", key="smtp", type="SMTP", host="smtp.mailtrap.io", port=587),
            ]
            db.add_all(services_to_add)
            db.commit()
    finally:
        db.close()


# ---------------------------------------------
# CONFIG FASTAPI
# ---------------------------------------------
app = FastAPI(
    title="DevOps Monitor API",
    version="1.0.0",
    description="API para monitoramento de serviços."
)

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------
# STARTUP EVENT
# ---------------------------------------------
@app.on_event("startup")
def startup_event():
    seed_services()


# ---------------------------------------------
# REGISTRO DE ROUTERS
# ---------------------------------------------
app.include_router(metrics.router)
app.include_router(services.router)
app.include_router(alerts.router)
app.include_router(status.router)
app.include_router(history.router)
app.include_router(consolidado.router)
