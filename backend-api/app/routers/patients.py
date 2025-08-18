from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import SessionLocal, engine

# Create the 'patients' table in the database if it doesn't exist
models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"],
)


# Dependency to get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """
    Creates a new patient record in the database.
    """
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient.patient_id).first()
    if db_patient:
        raise HTTPException(status_code=409, detail="Patient already exists")

    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    """
    Retrieves the details for a single patient from the database.
    """
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.get("", response_model=List[schemas.Patient])
def get_all_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all patients from the database.
    """
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients
@router.get("/{patient_id}/recommendations")
def get_patient_recommendations(patient_id: str):
    """
    Returns a list of dummy recommendations for a patient.
    """
    # In a real system, this would run a complex rules engine
    # For now, return the same 2 dummy recommendations for everyone
    return [
        {"id": "rec_001", "text": "Consider Guideline XYZ for billing optimization."},
        {"id": "rec_002", "text": "Check for recent lab result consistency."},
    ]


@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: str, patient_update: schemas.PatientCreate, db: Session = Depends(get_db)):
    """
    Updates an existing patient's record.
    """
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Update the patient's data
    db_patient.name = patient_update.name
    db_patient.date_of_birth = patient_update.date_of_birth

    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    """
    Deletes a patient record.
    """
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()
    return {"ok": True}  # Return empty response