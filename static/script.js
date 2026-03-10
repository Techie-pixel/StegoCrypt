/* ═══════════════════════════════════════════
   StegoCrypt — Client-side JavaScript
   Tab switching, file handling, API calls
   ═══════════════════════════════════════════ */

// ── State ──
const state = {
    encodeImageFile: null,
    decodeImageFile: null,
    encodeAudioFile: null,
    decodeAudioFile: null,
    encodeVideoFile: null,
    decodeVideoFile: null,
};

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initDropzones();
    initCharCounters();
    spawnParticles();
});

// ── Tab Switching ──
function initTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;

            // Update buttons
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update panels
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            const panel = document.getElementById('panel' + capitalize(tab));
            if (panel) {
                panel.classList.remove('active');
                // Force reflow to restart animation
                void panel.offsetWidth;
                panel.classList.add('active');
            }
        });
    });
}

// ── Dropzones ──
function initDropzones() {
    document.querySelectorAll('.dropzone').forEach(zone => {
        const type = zone.dataset.type;
        const fileInput = zone.querySelector('.file-input');

        // Click to browse
        zone.addEventListener('click', (e) => {
            if (e.target.closest('.file-selected') || e.target.closest('.file-remove')) return;
            fileInput.click();
        });

        // File selected via input
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(type, e.target.files[0]);
            }
        });

        // Drag events
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });

        zone.addEventListener('dragleave', () => {
            zone.classList.remove('dragover');
        });

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                handleFileSelect(type, e.dataTransfer.files[0]);
            }
        });
    });
}

function handleFileSelect(type, file) {
    // Map type to state key: "encode_image" -> "encodeImage"
    const key = type.replace(/_([a-z])/g, (m, c) => c.toUpperCase());
    state[key + 'File'] = file;

    // Capitalize key for element IDs
    const elKey = key.charAt(0).toUpperCase() + key.slice(1);

    // Show file info
    const selectedDiv = document.getElementById(key + 'Selected');
    const nameSpan = document.getElementById(key + 'FileName');
    const dropContent = selectedDiv?.closest('.dropzone')?.querySelector('.dropzone-content');

    if (selectedDiv && nameSpan) {
        nameSpan.textContent = file.name + ' (' + formatFileSize(file.size) + ')';
        selectedDiv.style.display = 'flex';
        if (dropContent) dropContent.style.display = 'none';
    }

    showToast('success', `File selected: ${file.name}`);
}

function clearFile(key) {
    state[key + 'File'] = null;

    const selectedDiv = document.getElementById(key + 'Selected');
    const dropContent = selectedDiv?.closest('.dropzone')?.querySelector('.dropzone-content');
    const fileInput = document.getElementById(key + 'File');

    if (selectedDiv) selectedDiv.style.display = 'none';
    if (dropContent) dropContent.style.display = '';
    if (fileInput) fileInput.value = '';
}

// ── Character Counters ──
function initCharCounters() {
    ['encodeImage', 'encodeAudio', 'encodeVideo'].forEach(key => {
        const textarea = document.getElementById(key + 'Msg');
        const counter = document.getElementById(key + 'CharCount');
        if (textarea && counter) {
            textarea.addEventListener('input', () => {
                counter.textContent = textarea.value.length;
            });
        }
    });
}

// ── Encode ──
async function encodeFile(mediaType) {
    const key = 'encode' + capitalize(mediaType);
    const file = state[key + 'File'];
    const msgEl = document.getElementById(key + 'Msg');
    const btn = document.getElementById(key + 'Btn');
    const message = msgEl?.value?.trim();

    if (!file) {
        showToast('error', 'Please select a file first!');
        return;
    }
    if (!message) {
        showToast('error', 'Please enter a secret message!');
        return;
    }

    // UI feedback
    setButtonLoading(btn, true);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('message', message);

    try {
        const response = await fetch(`/encode/${mediaType}`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || 'Encoding failed');
        }

        // Download the file
        const blob = await response.blob();
        const ext = mediaType === 'image' ? 'png' : mediaType === 'audio' ? 'wav' : 'avi';
        downloadBlob(blob, `encoded_${mediaType}.${ext}`);

        showToast('success', `Message encoded successfully! File downloading...`);

        // Clear message and inputs after successful encoding
        setTimeout(() => {
            if (msgEl) {
                msgEl.value = '';
                const counter = document.getElementById(key + 'CharCount');
                if (counter) counter.textContent = '0';
            }
            clearFile(key); // Also clear the file input
        }, 1500); // 1.5s delay so user sees the success state briefly

    } catch (err) {
        showToast('error', err.message);
    } finally {
        setButtonLoading(btn, false);
    }
}

// ── Decode ──
async function decodeFile(mediaType) {
    const key = 'decode' + capitalize(mediaType);
    const file = state[key + 'File'];
    const btn = document.getElementById(key + 'Btn');

    if (!file) {
        showToast('error', 'Please select an encoded file first!');
        return;
    }

    setButtonLoading(btn, true);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`/decode/${mediaType}`, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Decoding failed');
        }

        // Show result
        const resultBox = document.getElementById(key + 'Result');
        const resultText = document.getElementById(key + 'ResultText');
        const resultMeta = document.getElementById(key + 'Meta');

        if (resultBox && resultText) {
            resultText.textContent = data.message;
            resultBox.style.display = 'block';
            if (resultMeta) {
                resultMeta.textContent = `${data.length} characters decoded`;
            }
        }

        showToast('success', `Hidden message revealed! (${data.length} chars)`);

    } catch (err) {
        showToast('error', err.message);
    } finally {
        setButtonLoading(btn, false);
    }
}

// ── Clear Decode Result ──
function clearDecodeResult(mediaType) {
    const key = 'decode' + capitalize(mediaType);
    const resultBox = document.getElementById(key + 'Result');
    const resultText = document.getElementById(key + 'ResultText');

    if (resultBox) resultBox.style.display = 'none';
    if (resultText) resultText.textContent = '';

    clearFile(key);
}

// ── Toast Notifications ──
function showToast(type, message) {
    const container = document.getElementById('toastContainer');
    const icons = { success: '✅', error: '❌', info: 'ℹ️' };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || 'ℹ️'}</span>
        <span class="toast-text">${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.transition = 'opacity 0.3s, transform 0.3s';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(40px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ── Copy to Clipboard ──
function copyResult(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;

    navigator.clipboard.writeText(el.textContent).then(() => {
        showToast('success', 'Copied to clipboard!');
    }).catch(() => {
        // Fallback
        const range = document.createRange();
        range.selectNodeContents(el);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        document.execCommand('copy');
        sel.removeAllRanges();
        showToast('success', 'Copied to clipboard!');
    });
}

// ── Helpers ──
function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function setButtonLoading(btn, loading) {
    if (!btn) return;
    const text = btn.querySelector('.btn-text');
    const icon = btn.querySelector('.btn-icon');
    const loader = btn.querySelector('.btn-loader');

    if (loading) {
        btn.disabled = true;
        btn.classList.add('scanning');
        if (text) text.textContent = 'Processing...';
        if (icon) icon.style.display = 'none';
        if (loader) loader.style.display = 'block';
    } else {
        btn.disabled = false;
        btn.classList.remove('scanning');
        if (icon) icon.style.display = '';
        if (loader) loader.style.display = 'none';

        // Restore original text
        const isEncode = btn.classList.contains('encode-btn');
        if (text) text.textContent = isEncode ? 'Encode & Download' : 'Decode Message';
    }
}

// ── Floating particles ──
function spawnParticles() {
    const container = document.getElementById('bgParticles');
    if (!container) return;

    const isDark = !document.documentElement.getAttribute('data-theme') || document.documentElement.getAttribute('data-theme') === 'dark';
    const colors = isDark
        ? ['rgba(0,217,255,0.3)', 'rgba(168,85,247,0.25)', 'rgba(0,232,123,0.2)', 'rgba(248,87,166,0.2)']
        : ['rgba(0,180,220,0.2)', 'rgba(136,64,217,0.15)', 'rgba(0,184,77,0.12)', 'rgba(214,51,132,0.12)'];

    for (let i = 0; i < 30; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        const size = Math.random() * 4 + 1;
        p.style.width = size + 'px';
        p.style.height = size + 'px';
        p.style.left = Math.random() * 100 + '%';
        p.style.background = colors[Math.floor(Math.random() * colors.length)];
        p.style.animationDuration = (Math.random() * 15 + 10) + 's';
        p.style.animationDelay = (Math.random() * 10) + 's';
        container.appendChild(p);
    }
}
