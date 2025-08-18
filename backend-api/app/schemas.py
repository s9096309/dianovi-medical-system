import datetime
from pydantic import BaseModel

# Pydantic model for creating a patient (request)
class PatientCreate(BaseModel):
    patient_id: str
    name: str
    date_of_birth: datetime.date

# Pydantic model for reading a patient (response)
class Patient(PatientCreate):
    class Config:
        from_attributes = True