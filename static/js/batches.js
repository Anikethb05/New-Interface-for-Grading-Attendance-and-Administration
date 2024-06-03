// Define batches data
const batchesData = {
    'BTech 22': ['A', 'B', 'C'],
    'BSc 22': ['A', 'B', 'C'],
    'BTech 23': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'BSc 23': ['A', 'B', 'C']
};

// Function to update sections dropdown based on selected batch
function updateSections() {
    const batchSelect = document.getElementById('batch-select');
    const sectionSelect = document.getElementById('section-select');
    const selectedBatch = batchSelect.value;

    // Clear the current options in the section dropdown
    sectionSelect.innerHTML = '<option value="">Select a section</option>';

    // Populate the section dropdown based on the selected batch
    if (selectedBatch && batchesData[selectedBatch]) {
        batchesData[selectedBatch].forEach(function(section) {
            const option = document.createElement('option');
            option.value = section;
            option.textContent = section;
            sectionSelect.appendChild(option);
        });
    }
}

// Add event listener to batch select dropdown
document.getElementById('batch-select').addEventListener('change', updateSections);
