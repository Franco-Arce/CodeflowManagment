from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ..database import get_session
from ..models import Incident, IncidentStatus, User
from ..auth import get_current_user

router = APIRouter(
    prefix="/incidents",
    tags=["incidents"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[Incident])
async def read_incidents(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    incidents = session.exec(select(Incident).offset(skip).limit(limit)).all()
    return incidents

@router.post("/", response_model=Incident)
async def create_incident(incident: Incident, session: Session = Depends(get_session)):
    session.add(incident)
    session.commit()
    session.refresh(incident)
    return incident

@router.put("/{incident_id}", response_model=Incident)
async def update_incident(incident_id: int, incident_update: Incident, session: Session = Depends(get_session)):
    db_incident = session.get(Incident, incident_id)
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident_data = incident_update.dict(exclude_unset=True)
    for key, value in incident_data.items():
        setattr(db_incident, key, value)
    
    session.add(db_incident)
    session.commit()
    session.refresh(db_incident)
    return db_incident
