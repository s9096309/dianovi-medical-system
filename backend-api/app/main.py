from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routers import patients
from .database import engine
from . import models

# --- Lifespan Event for Startup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs on startup
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    yield
    # Code below yield runs on shutdown (not needed for now)

app = FastAPI(
    title="dianovi Medical Recommendation API",
    description="API for patient data and treatment recommendations.",
    version="0.1.0",
    lifespan=lifespan # Use the lifespan event
)

# --- CORS Middleware ---
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers and Root Endpoint ---
app.include_router(patients.router)

@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok"}