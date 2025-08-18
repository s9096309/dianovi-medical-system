from sqlalchemy import Column, String, Date
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    # Define the columns for the 'patients' table
    patient_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    date_of_birth = Column(Date)