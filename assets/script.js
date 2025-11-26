// Fallback: JavaScript can call the Python functions
document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    
    if (generateBtn) {
        generateBtn.addEventListener('click', function() {
            if (window.generateQR) {
                window.generateQR();
            } else {
                console.log('Waiting for PyScript to load...');
                setTimeout(function() {
                    if (window.generateQR) {
                        window.generateQR();
                    }
                }, 500);
            }
        });
    }
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            if (window.downloadQR) {
                window.downloadQR();
            } else {
                console.log('Waiting for PyScript to load...');
                setTimeout(function() {
                    if (window.downloadQR) {
                        window.downloadQR();
                    }
                }, 500);
            }
        });
    }
});

