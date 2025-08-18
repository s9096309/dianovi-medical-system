from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import patients
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="dianovi Medical Recommendation API",
    description="API for patient data and treatment recommendations.",
    version="0.1.0"
)


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, ....)
    allow_headers=["*"],
)

app.include_router(patients.router)

@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok"}