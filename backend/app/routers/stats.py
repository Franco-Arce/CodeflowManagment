from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..database import get_session
from ..models import Incident, IncidentStatus
from ..ml_service import ml_service
from pydantic import BaseModel

router = APIRouter(tags=["stats"])

class PredictionRequest(BaseModel):
    tickets: int
    payment_delays: int
    subscription_months: int

@router.get("/stats")
async def get_stats(session: Session = Depends(get_session)):
    total_incidents = len(session.exec(select(Incident)).all())
    open_incidents = len(session.exec(select(Incident).where(Incident.status == IncidentStatus.OPEN)).all())
    
    # Mock data for now, replace with real aggregations
    avg_payment_delay = 2.5 
    churn_risk_avg = 0.15
    
    return {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "avg_payment_delay": avg_payment_delay,
        "churn_risk_avg": churn_risk_avg
    }

@router.post("/predict")
async def predict_churn(request: PredictionRequest):
    probability = ml_service.predict_churn(request.dict())
    return {"churn_probability": probability}
