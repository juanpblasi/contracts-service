/**
 * Report Generation and Visualization
 */

/**
 * Initialize report functionality
 */
function initializeReport() {
    // Report initialization handled by app.js
    console.log('Report module initialized');
}

/**
 * Compare files and display results
 */
async function compareFiles(file1, file2) {
    showLoading();

    try {
        // Create form data
        const formData = new FormData();
        formData.append('file1', file1);
        formData.append('file2', file2);

        // Send request to API
        const response = await fetch(`${API_BASE_URL}/compare`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error en la comparación');
        }

        const data = await response.json();

        if (data.status === 'success') {
            // Store report
            AppState.currentReport = data.report;

            // Display results
            displayResults(data.report);

            // Scroll to results
            setTimeout(() => {
                document.getElementById('resultsSection').scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 300);
        } else {
            throw new Error(data.message || 'Error desconocido');
        }

    } catch (error) {
        console.error('Comparison error:', error);
        alert('Error al comparar archivos: ' + error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Display comparison results
 */
function displayResults(report) {
    // Show results section
    document.getElementById('resultsSection').classList.add('active');

    // Display summary
    displaySummary(report.summary);

    // Display differences
    displayDifferences(report.details.differences);

    // Display only in file 1
    displayOnlyInFile(report.details.only_in_file1, 1);

    // Display only in file 2
    displayOnlyInFile(report.details.only_in_file2, 2);

    // Display matches
    displayMatches(report.details.matches);
}

/**
 * Display summary statistics
 */
function displaySummary(summary) {
    document.getElementById('totalFields').textContent = summary.total_fields;
    document.getElementById('matchesCount').textContent = summary.matches;
    document.getElementById('differencesCount').textContent = summary.differences;
    document.getElementById('onlyFile1Count').textContent = summary.only_in_file1;
    document.getElementById('onlyFile2Count').textContent = summary.only_in_file2;
    document.getElementById('matchPercentage').textContent = summary.match_percentage + '%';

    // Animate progress bar
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');

    setTimeout(() => {
        progressFill.style.width = summary.match_percentage + '%';
        progressText.textContent = summary.match_percentage + '%';
    }, 100);
}

/**
 * Display differences table
 */
function displayDifferences(differences) {
    const tbody = document.getElementById('differencesTableBody');
    const card = document.getElementById('differencesCard');

    tbody.innerHTML = '';

    if (differences.length === 0) {
        card.style.display = 'none';
        return;
    }

    card.style.display = 'block';

    differences.forEach(diff => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${escapeHtml(diff.field)}</strong></td>
            <td>${formatValue(diff.file1_value)}</td>
            <td>${formatValue(diff.file2_value)}</td>
            <td><span class="badge badge-diff">Diferente</span></td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Display fields only in one file
 */
function displayOnlyInFile(items, fileNumber) {
    const tbody = document.getElementById(fileNumber === 1 ? 'onlyFile1TableBody' : 'onlyFile2TableBody');
    const card = document.getElementById(fileNumber === 1 ? 'onlyFile1Card' : 'onlyFile2Card');

    tbody.innerHTML = '';

    if (items.length === 0) {
        card.style.display = 'none';
        return;
    }

    card.style.display = 'block';

    items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${escapeHtml(item.field)}</strong></td>
            <td>${formatValue(item.value)}</td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Display matches table
 */
function displayMatches(matches) {
    const tbody = document.getElementById('matchesTableBody');
    const card = document.getElementById('matchesCard');

    tbody.innerHTML = '';

    if (matches.length === 0) {
        card.style.display = 'none';
        return;
    }

    card.style.display = 'block';

    // Show first 50 matches to avoid overwhelming the UI
    const displayMatches = matches.slice(0, 50);

    displayMatches.forEach(match => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${escapeHtml(match.field)}</strong></td>
            <td>${formatValue(match.value)}</td>
            <td><span class="badge badge-match">✓ Coincide</span></td>
        `;
        tbody.appendChild(row);
    });

    if (matches.length > 50) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="3" class="text-center">
                <em>Mostrando 50 de ${matches.length} coincidencias totales</em>
            </td>
        `;
        tbody.appendChild(row);
    }
}

/**
 * Format value for display
 */
function formatValue(value) {
    if (value === null || value === undefined) {
        return '<em style="color: #999;">null</em>';
    }

    if (typeof value === 'object') {
        return '<code>' + escapeHtml(JSON.stringify(value)) + '</code>';
    }

    return escapeHtml(String(value));
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Download report as JSON
 */
function downloadJson(report) {
    const jsonStr = JSON.stringify(report, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `contract_comparison_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * Download HTML report
 */
async function downloadHtmlReport(file1, file2) {
    showLoading();

    try {
        const formData = new FormData();
        formData.append('file1', file1);
        formData.append('file2', file2);

        const response = await fetch(`${API_BASE_URL}/compare/html`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error al generar reporte HTML');
        }

        const html = await response.text();
        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `contract_comparison_${Date.now()}.html`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

    } catch (error) {
        console.error('HTML export error:', error);
        alert('Error al descargar reporte HTML: ' + error.message);
    } finally {
        hideLoading();
    }
}
