from pydantic import BaseModel
from datetime import datetime

class MetricCreate(BaseModel):
    service_key: str
    metric_name: str
    value: float
    unit: str

class MetricRead(BaseModel):
    metric_name: str
    value: float
    unit: str
    timestamp: datetime

    class Config:
        orm_mode = True

class ServiceRead(BaseModel):
    id: int
    name: str
    key: str

    class Config:
        orm_mode = True

