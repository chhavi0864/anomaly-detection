document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const errorContainer = document.getElementById('errorContainer');
    
    if (fileInput.files.length === 0) return;
    
    // Reset UI state
    errorContainer.style.display = 'none';
    resultsContainer.style.display = 'none';
    submitBtn.textContent = 'Analyzing Traffic...';
    submitBtn.disabled = true;
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'An unexpected error occurred during prediction.');
        }
        
        // Update the summary cards
        document.getElementById('totalCount').textContent = data.total_processed;
        
        // Handle counts (in case one category has 0, pandas might omit it from the dict)
        document.getElementById('anomalyCount').textContent = data.counts['Anomaly'] || 0;
        document.getElementById('normalCount').textContent = data.counts['Normal'] || 0;
        
        // Populate the results table
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = ''; // Clear old rows
        
        data.predictions.forEach((prediction, index) => {
            const tr = document.createElement('tr');
            
            // Row ID
            const tdIndex = document.createElement('td');
            tdIndex.textContent = `Flow #${index + 1}`;
            
            // Status Badge
            const tdStatus = document.createElement('td');
            const badge = document.createElement('span');
            badge.className = `badge ${prediction.toLowerCase()}`;
            badge.textContent = prediction;
            tdStatus.appendChild(badge);
            
            tr.appendChild(tdIndex);
            tr.appendChild(tdStatus);
            tbody.appendChild(tr);
        });
        
        // Show results with a nice animation
        resultsContainer.style.display = 'block';
        
    } catch (err) {
        errorContainer.textContent = err.message;
        errorContainer.style.display = 'block';
    } finally {
        submitBtn.textContent = 'Detect Anomalies';
        submitBtn.disabled = false;
    }
});
