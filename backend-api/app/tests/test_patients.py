from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.routers.patients import get_db

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use an in-memory SQLite database for tests
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

# Dependency Override: Use the test database instead of the real one
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a TestClient
client = TestClient(app)

# --- The Tests ---

def test_create_patient():
    """
    Test creating a new patient.
    """
    response = client.post(
        "/api/v1/patients",
        json={"patient_id": "P_TEST_001", "name": "Test Patient", "date_of_birth": "2000-01-01"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Test Patient"
    assert data["patient_id"] == "P_TEST_001"


def test_get_all_patients():
    """
    Test retrieving all patients after one has been created.
    """
    response = client.get("/api/v1/patients")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Test Patient"