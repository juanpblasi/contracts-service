/**
 * File Upload Handler
 */

/**
 * Initialize upload functionality
 */
function initializeUpload() {
    setupFileInput('file1Input', 'uploadArea1', 'file1Info', 1);
    setupFileInput('file2Input', 'uploadArea2', 'file2Info', 2);
}

/**
 * Setup file input with drag and drop
 */
function setupFileInput(inputId, areaId, infoId, fileNumber) {
    const input = document.getElementById(inputId);
    const area = document.getElementById(areaId);
    const info = document.getElementById(infoId);

    // Click to upload
    area.addEventListener('click', () => {
        input.click();
    });

    // File selection
    input.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0], area, info, fileNumber);
    });

    // Drag and drop
    area.addEventListener('dragover', (e) => {
        e.preventDefault();
        area.classList.add('drag-over');
    });

    area.addEventListener('dragleave', () => {
        area.classList.remove('drag-over');
    });

    area.addEventListener('drop', (e) => {
        e.preventDefault();
        area.classList.remove('drag-over');

        const file = e.dataTransfer.files[0];
        if (file) {
            // Update the input element
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;

            handleFileSelect(file, area, info, fileNumber);
        }
    });
}

/**
 * Handle file selection
 */
function handleFileSelect(file, area, info, fileNumber) {
    if (!file) return;

    // Validate file type
    const allowedExtensions = ['json', 'csv', 'xlsx', 'xls', 'txt'];
    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
        alert(`Tipo de archivo no permitido. Formatos aceptados: ${allowedExtensions.join(', ')}`);
        return;
    }

    // Validate file size (50MB max)
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
        alert('El archivo es demasiado grande. Tamaño máximo: 50MB');
        return;
    }

    // Update state
    if (fileNumber === 1) {
        AppState.file1 = file;
    } else {
        AppState.file2 = file;
    }

    // Update UI
    area.classList.add('has-file');
    info.classList.remove('hidden');
    info.innerHTML = `
        <strong>✓ Archivo cargado:</strong><br>
        ${file.name}<br>
        <small>${formatFileSize(file.size)} • ${fileExtension.toUpperCase()}</small>
    `;

    // Update compare button
    updateCompareButton();
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
