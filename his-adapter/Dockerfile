FROM python:3.11-slim

WORKDIR /app

# This service needs the 'requests' library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and the sample data
COPY . .

# This command will run the script once the container starts
CMD ["python", "ingest.py"]