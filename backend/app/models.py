from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum

class IncidentStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str

class Incident(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: IncidentStatus = Field(default=IncidentStatus.OPEN)
    severity: IncidentSeverity = Field(default=IncidentSeverity.MEDIUM)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    churn_probability: Optional[float] = None
    last_prediction_date: Optional[datetime] = None
