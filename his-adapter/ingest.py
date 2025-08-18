import csv
import json
import logging
import os
import sys
import time

import requests

# 1. Environment-driven Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000")
PATIENT_CSV_PATH = os.getenv("PATIENT_CSV_PATH", "sample_data/patients.csv")
RECORDS_JSON_PATH = os.getenv("RECORDS_JSON_PATH", "sample_data/records.json")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "12"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))

# 2. Proper Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
)


# --- Data Reading and Validation Functions ---

def read_patient_data_from_csv(filename):
    """Reads patient demographic data from a CSV file."""
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            return list(csv.DictReader(csvfile))
    except FileNotFoundError:
        logging.error(f"FATAL: Patient CSV file not found at {filename}")
        return None
    except Exception as e:
        logging.error(f"FATAL: An unexpected error occurred reading CSV: {e}")
        return None


def read_medical_records_from_json(filename):
    """Reads and validates medical records from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
    except FileNotFoundError:
        logging.error(f"FATAL: Records JSON file not found at {filename}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"FATAL: Could not decode JSON from {filename}: {e}")
        return None

    # 3. Improved JSON Validation
    validated_records = {}
    if not isinstance(data, dict):
        logging.error("FATAL: JSON root is not a dictionary.")
        return None

    for patient_id, records in data.items():
        if not isinstance(records, list):
            logging.warning(f"Skipping patient {patient_id}: records are not a list.")
            continue

        validated_records[patient_id] = []
        for record in records:
            if all(key in record for key in ["record_id", "date", "type", "details"]):
                validated_records[patient_id].append(record)
            else:
                logging.warning(f"Skipping malformed record for patient {patient_id}: {record}")
    return validated_records


# --- Main Application Logic ---

def wait_for_api():
    """Waits for the API to become available using configurable retries."""
    logging.info(f"Checking API readiness at {API_BASE_URL}...")
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=5)
            if response.status_code == 200:
                logging.info("API is ready.")
                return True
        except requests.ConnectionError:
            logging.warning(f"API not ready. Retrying in {RETRY_DELAY}s... (Attempt {attempt + 1}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
    logging.error("FATAL: Could not connect to the API after all retries.")
    return False


def main():
    """Main function to run the ingestion process."""
    logging.info("HIS Adapter starting...")
    if not wait_for_api():
        sys.exit(1)  # 4. Graceful exit on critical failure

    # --- Ingest Patients (CSV) ---
    patients = read_patient_data_from_csv(PATIENT_CSV_PATH)
    if patients is None:
        sys.exit(1)

    logging.info(f"Found {len(patients)} patient records in CSV.")
    for patient in patients:
        try:
            response = requests.post(f"{API_BASE_URL}/api/v1/patients", json=patient)

            # 5. Duplicate Prevention Logic
            if response.status_code in [200, 201]:
                logging.info(f"Successfully sent patient data for {patient.get('patient_id')}")
            elif response.status_code == 409:  # Conflict
                logging.info(f"Patient {patient.get('patient_id')} already exists. Skipping.")
            else:
                logging.warning(
                    f"Failed sending patient {patient.get('patient_id')}. Status: {response.status_code}, Info: {response.text}")
        except requests.RequestException as e:
            logging.error(f"API request failed for patient {patient.get('patient_id')}: {e}")

    # --- Ingest Records (JSON) ---
    medical_records = read_medical_records_from_json(RECORDS_JSON_PATH)
    if medical_records is None:
        sys.exit(1)

    logging.info(f"Found medical records for {len(medical_records)} patients in JSON.")
    for patient_id, records in medical_records.items():
        if not records:
            continue  # Skip if patient had no valid records
        try:
            response = requests.post(f"{API_BASE_URL}/api/v1/patients/{patient_id}/records", json={"records": records})
            if response.status_code == 201:
                logging.info(f"Successfully sent {len(records)} medical records for patient {patient_id}")
            else:
                logging.warning(
                    f"Failed sending records for {patient_id}. Status: {response.status_code}, Info: {response.text}")
        except requests.RequestException as e:
            logging.error(f"API request failed for records of patient {patient_id}: {e}")

    logging.info("HIS Adapter finished successfully.")


if __name__ == "__main__":
    main()