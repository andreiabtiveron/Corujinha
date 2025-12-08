from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from . import models
from .routers import metrics, services, alerts, status, history

# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)

# Criação da API
app = FastAPI(
    title="DevOps Monitor API",
    version="1.0.0",
    description="API para monitoramento de serviços da disciplina de Redes."
)

# CORS (permite acesso total do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed inicial do banco (insere os serviços)
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


@app.on_event("startup")
def startup_event():
    seed_services()


# Registro dos routers
app.include_router(metrics.router)
app.include_router(services.router)
app.include_router(alerts.router)
app.include_router(status.router)
app.include_router(history.router)   
