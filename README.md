# Medical Recommendation System Prototype

This project is a minimal working slice of a medical recommendation system, built as a home assignment for dianovi GmbH.

The system ingests medical records, provides rule-based recommendations, and displays the information to doctors through a simple web interface.

The entire application is containerized using Docker and can be run with a single command.

---

## Tech Stack

* **Backend API**: Python 3.12 with FastAPI
* **Database**: PostgreSQL
* **Frontend**: Vanilla HTML, CSS, and JavaScript
* **Web Server (UI)**: Nginx
* **Containerization**: Docker & Docker Compose

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:
* Docker
* Docker Compose

---

## Running the Application

1.  **Clone the repository** (or ensure you have the project files).

2.  **Navigate to the root directory** of the project (the one containing `docker-compose.yml`).
    ```bash
    cd /path/to/dianovi-system
    ```

3.  **Build and run the application** using Docker Compose. This command will build the necessary images, start all the services, and populate the database with sample data.
    ```bash
    docker-compose up --build
    ```

The application is now running!

---

## Accessing the Services

Once the containers are up, you can access the different parts of the system from your browser:

* **Doctor UI**: [http://localhost:8080](http://localhost:8080)
    * *The main web interface for viewing patient data.*

* **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
    * *Interactive OpenAPI (Swagger UI) documentation for all API endpoints.*

* **API Health Check**: [http://localhost:8000/](http://localhost:8000/)
    * *A simple endpoint to confirm the API is running.*

---

## Project Structure

The project is organized into several services:

* **`backend-api`**: The core FastAPI application that serves data, runs business logic, and connects to the database.
* **`doctor-ui`**: A simple frontend application served by Nginx.
* **`his-adapter`**: A one-shot script that reads sample data from local files and ingests it into the API upon startup.
* **`db`**: The PostgreSQL database service.
