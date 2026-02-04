/**
 * Main Application Controller
 */

// API Configuration
const API_BASE_URL = 'http://localhost:5001/api';

// Application State
const AppState = {
    file1: null,
    file2: null,
    currentReport: null,

    reset() {
        this.file1 = null;
        this.file2 = null;
        this.currentReport = null;
    },

    hasFiles() {
        return this.file1 !== null && this.file2 !== null;
    }
};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Contract Comparison Service initialized');
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Initialize upload handlers
    initializeUpload();

    // Initialize report handlers
    initializeReport();

    // Setup compare button
    setupCompareButton();

    // Setup export buttons
    setupExportButtons();

    // Setup new comparison button
    setupNewComparisonButton();
}

/**
 * Setup compare button handler
 */
function setupCompareButton() {
    const compareBtn = document.getElementById('compareBtn');

    compareBtn.addEventListener('click', async () => {
        if (!AppState.hasFiles()) {
            alert('Por favor, carga ambos archivos antes de comparar.');
            return;
        }

        try {
            await compareFiles(AppState.file1, AppState.file2);
        } catch (error) {
            console.error('Error during comparison:', error);
            alert('Error al comparar archivos: ' + error.message);
        }
    });
}

/**
 * Setup export buttons
 */
function setupExportButtons() {
    const exportJsonBtn = document.getElementById('exportJsonBtn');
    const exportHtmlBtn = document.getElementById('exportHtmlBtn');

    exportJsonBtn.addEventListener('click', () => {
        if (AppState.currentReport) {
            downloadJson(AppState.currentReport);
        }
    });

    exportHtmlBtn.addEventListener('click', async () => {
        if (AppState.hasFiles()) {
            await downloadHtmlReport(AppState.file1, AppState.file2);
        }
    });
}

/**
 * Setup new comparison button
 */
function setupNewComparisonButton() {
    const newComparisonBtn = document.getElementById('newComparisonBtn');

    newComparisonBtn.addEventListener('click', () => {
        resetApplication();
    });
}

/**
 * Reset application to initial state
 */
function resetApplication() {
    // Reset state
    AppState.reset();

    // Reset file uploads
    document.getElementById('file1Input').value = '';
    document.getElementById('file2Input').value = '';
    document.getElementById('file1Info').classList.add('hidden');
    document.getElementById('file2Info').classList.add('hidden');
    document.getElementById('uploadArea1').classList.remove('has-file');
    document.getElementById('uploadArea2').classList.remove('has-file');

    // Disable compare button
    document.getElementById('compareBtn').disabled = true;

    // Hide results
    document.getElementById('resultsSection').classList.remove('active');

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Show loading overlay
 */
function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

/**
 * Update compare button state
 */
function updateCompareButton() {
    const compareBtn = document.getElementById('compareBtn');
    compareBtn.disabled = !AppState.hasFiles();
}
