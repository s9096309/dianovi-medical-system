document.addEventListener('DOMContentLoaded', () => {
    const patientListContainer = document.getElementById('patient-list-container');
    const addPatientForm = document.getElementById('add-patient-form');
    const API_URL = 'http://localhost:8000';

    // --- DATA FETCHING FUNCTIONS ---

    async function fetchPatients() {
        try {
            const response = await fetch(`${API_URL}/api/v1/patients`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const patients = await response.json();
            renderPatients(patients);
        } catch (error) {
            patientListContainer.innerHTML = '<p>Error loading patients. Is the API running?</p>';
            console.error('Failed to fetch patients:', error);
        }
    }

    async function fetchRecommendations(patientId, recoContainer) {
        recoContainer.innerHTML = '<p>Loading recommendations...</p>';
        try {
            const response = await fetch(`${API_URL}/api/v1/patients/${patientId}/recommendations`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const recommendations = await response.json();
            renderRecommendations(recommendations, recoContainer);
        } catch (error) {
            recoContainer.innerHTML = '<p>Could not load recommendations.</p>';
            console.error('Failed to fetch recommendations:', error);
        }
    }

    // --- UI RENDERING FUNCTIONS ---

    function renderPatients(patients) {
        patientListContainer.innerHTML = ''; // Clear existing content
        patients.forEach(patient => {
            const card = document.createElement('div');
            card.className = 'patient-card';
            card.dataset.patientId = patient.patient_id;
            card.dataset.name = patient.name;
            card.dataset.dob = patient.date_of_birth;

            card.innerHTML = `
                <h2>${patient.name}</h2>
                <p><strong>Patient ID:</strong> ${patient.patient_id}</p>
                <p><strong>Date of Birth:</strong> ${patient.date_of_birth}</p>
                <div class="actions">
                    <button class="edit-btn">Edit</button>
                    <button class="delete-btn">Delete</button>
                </div>
                <div class="recommendations" id="reco-${patient.patient_id}"></div>
            `;
            patientListContainer.appendChild(card);
        });
    }

    function renderRecommendations(recommendations, container) {
        if (recommendations.length > 0) {
            container.innerHTML = `
                <h3>Recommendations:</h3>
                <ul>
                    ${recommendations.map(reco => `<li>${reco.text}</li>`).join('')}
                </ul>
            `;
        } else {
            container.innerHTML = '<p>No recommendations available.</p>';
        }
    }

    // --- EVENT HANDLERS ---

    addPatientForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const newPatient = {
            patient_id: document.getElementById('patient-id').value,
            name: document.getElementById('patient-name').value,
            date_of_birth: document.getElementById('patient-dob').value
        };

        try {
            const response = await fetch(`${API_URL}/api/v1/patients`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newPatient)
            });
            if (!response.ok) throw new Error('Failed to create patient');
            addPatientForm.reset();
            fetchPatients(); // Refresh the list
        } catch (error) {
            console.error('Error adding patient:', error);
            alert('Could not add patient.');
        }
    });

    patientListContainer.addEventListener('click', async (event) => {
        const card = event.target.closest('.patient-card');
        if (!card) return;

        const patientId = card.dataset.patientId;

        // Handle Delete Button
        if (event.target.classList.contains('delete-btn')) {
            if (confirm(`Are you sure you want to delete patient ${patientId}?`)) {
                try {
                    const response = await fetch(`${API_URL}/api/v1/patients/${patientId}`, { method: 'DELETE' });
                    if (!response.ok) throw new Error('Failed to delete');
                    card.remove(); // Remove from UI instantly
                } catch (error) {
                    console.error('Error deleting patient:', error);
                    alert('Could not delete patient.');
                }
            }
        }

        // Handle Edit Button
        if (event.target.classList.contains('edit-btn')) {
            const newName = prompt("Enter new name:", card.dataset.name);
            const newDob = prompt("Enter new date of birth (YYYY-MM-DD):", card.dataset.dob);

            if (newName && newDob) {
                const updatedPatient = { patient_id: patientId, name: newName, date_of_birth: newDob };
                try {
                    const response = await fetch(`${API_URL}/api/v1/patients/${patientId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(updatedPatient)
                    });
                    if (!response.ok) throw new Error('Failed to update');
                    fetchPatients(); // Refresh the list
                } catch (error) {
                    console.error('Error updating patient:', error);
                    alert('Could not update patient.');
                }
            }
        }

        // Handle clicking card to show recommendations (but not on buttons)
        if (!event.target.closest('button')) {
            const recoContainer = card.querySelector(`#reco-${patientId}`);
            fetchRecommendations(patientId, recoContainer);
        }
    });

    // Initial fetch of patients when the page loads
    fetchPatients();
});