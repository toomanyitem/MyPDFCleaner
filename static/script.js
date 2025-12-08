const translations = {
    th: {
        subtitle: "ลบข้อความสำคัญออกจากไฟล์ PDF ของคุณอย่างปลอดภัย",
        tab_redact: "ลบข้อความ",
        tab_export: "แปลงไฟล์",
        drop_title: "ลากไฟล์ PDF มาวางที่นี่",
        drop_desc: "หรือคลิกเพื่อเลือกไฟล์",
        label_text_input: "ข้อความที่ต้องการลบ (แยกบรรทัดเพื่อระบุหลายคำ)",
        header_auto_redact: "ตัวช่วยลบอัตโนมัติ",
        chk_all_sensitive: "ลบข้อมูลส่วนตัวทั้งหมด",
        chk_email: "อีเมล",
        chk_phone: "เบอร์โทรศัพท์",
        chk_id_card: "เลขบัตรประชาชน",
        header_ocr: "สำหรับเอกสารสแกน (OCR)",
        chk_enable_ocr: "เปิดใช้งาน OCR",
        ocr_checking: "กำลังตรวจสอบระบบ OCR...",
        ocr_ready: "✅ พบระบบ Tesseract OCR พร้อมใช้งาน",
        ocr_missing: "❌ ไม่พบ Tesseract OCR (กรุณาติดตั้งเพื่อใช้งานฟีเจอร์นี้)",
        btn_start_redact: "เริ่มการลบข้อความ",
        export_desc: "แปลงไฟล์ PDF ของคุณเป็นเอกสารที่แก้ไขได้",
        chk_ocr_export: "ใช้ OCR ช่วยแกะข้อความ (แนะนำ)",
        btn_export_word: "แปลงเป็น Word (.docx)",
        btn_export_text: "แปลงเป็น Text (.txt)"
    },
    en: {
        subtitle: "Securely remove sensitive information from your PDF files.",
        tab_redact: "Redact",
        tab_export: "Export",
        drop_title: "Drop PDF file here",
        drop_desc: "or click to select file",
        label_text_input: "Text to remove (enter multiple words on new lines)",
        header_auto_redact: "Auto Redact",
        chk_all_sensitive: "All Sensitive Data",
        chk_email: "Email",
        chk_phone: "Phone Number",
        chk_id_card: "ID Card / Govt ID",
        header_ocr: "For Scanned Docs (OCR)",
        chk_enable_ocr: "Enable OCR",
        ocr_checking: "Checking OCR system...",
        ocr_ready: "✅ Tesseract OCR Ready",
        ocr_missing: "❌ Tesseract OCR Not Found (Install to endable)",
        btn_start_redact: "Start Redaction",
        export_desc: "Convert your PDF into editable documents.",
        chk_ocr_export: "Use OCR (Recommended for scans)",
        btn_export_word: "Export to Word (.docx)",
        btn_export_text: "Export to Text (.txt)"
    }
};

let currentLang = 'th';

// --- i18n Logic ---
function setLanguage(lang) {
    currentLang = lang;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });

    // Update Input Placeholders
    const txtInput = document.getElementById('text-input');
    if (txtInput) {
        txtInput.placeholder = lang === 'en'
            ? "Example:\nConfidential\nTop Secret\n123456789"
            : "ตัวอย่าง:\nความลับ\nConfidential\n123456789";
    }

    // Toggle Buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
}

document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.getAttribute('data-lang')));
});


// ... (Previous Application Logic Below) ...

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const filenameSpan = document.getElementById('filename');
const removeFileBtn = document.getElementById('remove-file');

// Redact Elements
const processBtn = document.getElementById('process-btn');
const textInput = document.getElementById('text-input');
const ocrCheckRedact = document.getElementById('ocr-checkbox-redact');

// Export Elements
const exportDocxBtn = document.getElementById('export-docx-btn');
const exportTxtBtn = document.getElementById('export-txt-btn');
const ocrCheckExport = document.getElementById('ocr-checkbox-export');

// Tabs
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

let currentFile = null;

// --- Tab Logic ---
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        const tabId = btn.getAttribute('data-tab');
        document.getElementById(`section-${tabId}`).classList.add('active');
    });
});

// --- Drag & Drop ---
dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => { dropZone.classList.remove('dragover'); });
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFileSelect(e.dataTransfer.files[0]);
});
dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) handleFileSelect(e.target.files[0]);
});

removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    currentFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    document.querySelector('.icon-container').style.display = 'block';
    dropZone.querySelector('h3').style.display = 'block';
    dropZone.querySelector('p').style.display = 'block';
    updateButtonState();
});

textInput.addEventListener('input', updateButtonState);

function handleFileSelect(file) {
    if (file.type !== 'application/pdf') {
        alert(currentLang === 'en' ? 'Please upload PDF file only' : 'กรุณาอัพโหลดไฟล์ PDF เท่านั้น');
        return;
    }
    currentFile = file;
    filenameSpan.textContent = file.name;

    document.querySelector('.icon-container').style.display = 'none';
    dropZone.querySelector('h3').style.display = 'none';
    dropZone.querySelector('p').style.display = 'none';
    fileInfo.style.display = 'flex';

    updateButtonState();
}

function updateButtonState() {
    const hasFile = !!currentFile;
    const hasText = textInput.value.trim().length > 0;
    const anyAuto = document.querySelector('input[name="pattern"]:checked');

    // Redact Button
    processBtn.disabled = !(hasFile && (hasText || anyAuto));

    // Export Buttons
    if (exportDocxBtn) exportDocxBtn.disabled = !hasFile;
    if (exportTxtBtn) exportTxtBtn.disabled = !hasFile;
}

// Watch checkboxes for state update
document.querySelectorAll('input[name="pattern"]').forEach(cb => {
    cb.addEventListener('change', updateButtonState);
});


// --- Action Handlers ---

// 1. Redact Process
processBtn.addEventListener('click', async () => {
    await processAction('/api/process', processBtn, (formData) => {
        formData.append('texts', textInput.value);
        if (ocrCheckRedact) formData.append('use_ocr', ocrCheckRedact.checked);
        const patterns = Array.from(document.querySelectorAll('input[name="pattern"]:checked')).map(cb => cb.value);
        formData.append('patterns', patterns.join(','));
        return `cleaned_${currentFile.name}`;
    });
});

// 2. Export Helper
async function handleExport(btn, format) {
    await processAction('/api/export', btn, (formData) => {
        formData.append('format', format);
        if (ocrCheckExport) formData.append('use_ocr', ocrCheckExport.checked);
        return `converted_${currentFile.name}.${format}`;
    });
}

if (exportDocxBtn) exportDocxBtn.addEventListener('click', () => handleExport(exportDocxBtn, 'docx'));
if (exportTxtBtn) exportTxtBtn.addEventListener('click', () => handleExport(exportTxtBtn, 'txt'));


// Generic Process Function
async function processAction(url, btn, formBuilder) {
    if (!currentFile) return;

    setLoading(btn, true);

    try {
        const formData = new FormData();
        formData.append('file', currentFile);

        // Custom form data
        const downloadName = formBuilder(formData);

        const response = await fetch(url, { method: 'POST', body: formData });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || 'Operation failed');
        }

        const blob = await response.blob();
        downloadBlob(blob, downloadName);

    } catch (error) {
        alert((currentLang === 'en' ? 'Error: ' : 'เกิดข้อผิดพลาด: ') + error.message);
    } finally {
        setLoading(btn, false);
    }
}


function downloadBlob(blob, name) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

function setLoading(btn, isLoading) {
    const loader = btn.querySelector('.loader');

    if (isLoading) {
        btn.disabled = true;
        if (loader) loader.style.display = 'inline-block';
    } else {
        btn.disabled = false;
        if (loader) loader.style.display = 'none';
        updateButtonState(); // Re-check if valid
    }
}

// Check OCR
window.addEventListener('load', async () => {
    try {
        const res = await fetch('/api/check_ocr');
        const data = await res.json();
        const ocrStatus = document.getElementById('ocr-status');

        if (data.available) {
            if (ocrStatus) {
                ocrStatus.textContent = translations[currentLang].ocr_ready;
                ocrStatus.classList.add('success');
            }
            if (ocrCheckRedact) ocrCheckRedact.disabled = false;
            if (ocrCheckExport) ocrCheckExport.disabled = false;
        } else {
            if (ocrStatus) {
                ocrStatus.textContent = translations[currentLang].ocr_missing;
                ocrStatus.classList.add('error');
            }
            if (ocrCheckRedact) ocrCheckRedact.disabled = true;
            if (ocrCheckExport) {
                ocrCheckExport.disabled = true;
                ocrCheckExport.checked = false;
            }
        }
    } catch (e) {
        console.error("Failed to check OCR status", e);
    }
});
