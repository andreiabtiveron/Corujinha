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

    model_config = {"from_attributes": True}

class ServiceRead(BaseModel):
    id: int
    name: str
    key: str

    class Config:
        orm_mode = True

