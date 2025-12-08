# MyPDFCleaner (Web Interface)

[English Version Below]

**MyPDFCleaner** คือโปรแกรมสำหรับลบข้อความออกจากไฟล์ PDF และแปลงไฟล์ PDF เป็น Word/Text ผ่านหน้าเว็บที่ใช้งานง่าย พร้อมดีไซน์ทันสมัยแบบ Glassmorphism

![Screenshot](https://via.placeholder.com/800x500?text=MyPDFCleaner+UI)

## ✨ ฟีเจอร์หลัก
*   **ใช้งานง่าย**: ลากไฟล์วาง (Drag & Drop) ใช้งานผ่านเว็บเบราว์เซอร์
*   **ดีไซน์ทันสมัย**: UI สวยงามแบบ Glassmorphism พร้อมรองรับ 2 ภาษา (ไทย/อังกฤษ)
*   **ลบข้อความ**: ระบุคำที่ต้องการลบ แล้วโปรแกรมจะถมดำ (Redact) ให้ทันที
*   **ลบข้อมูลส่วนตัวอัตโนมัติ**:
    *   📧 อีเมล (Email)
    *   📱 เบอร์โทรศัพท์ (Phone Number)
    *   🆔 เลขบัตรประชาชน (ID Card)
    *   💳 หรือกด "ลบข้อมูลส่วนตัวทั้งหมด" (All Sensitive Data) ทีเดียวจบ
*   **แปลงไฟล์ (Export)**:
    *   แปลง PDF เป็น **Word (.docx)** (แก้ไขต่อได้)
    *   แปลง PDF เป็น **Text (.txt)**
*   **รองรับ OCR**: อ่านข้อความจากไฟล์สแกน (รูปภาพ) ได้แม่นยำด้วย Tesseract OCR
*   **ปลอดภัย**: ไฟล์ประมวลผลในเครื่องตัวเอง (Localhost) ไม่มีการอัปโหลดขึ้นเซิร์ฟเวอร์อื่น

---

## 🚀 วิธีติดตั้งและใช้งาน

### 1. ติดตั้ง Python และ Tesseract OCR
*   **Windows**:
    *   ดาวน์โหลดและติดตั้ง [Python](https://www.python.org/downloads/) (ติ๊กถูกช่อง "Add Python to PATH" ด้วย)
    *   ดาวน์โหลดและติดตั้ง [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (โปรแกรมจะพยายามติดตั้งให้อัตโนมัติถ้าไม่มี)
*   **macOS**: `brew install tesseract tesseract-lang`
*   **Linux**: `sudo apt install tesseract-ocr tesseract-ocr-tha`

### 2. รันโปรแกรม
ดับเบิ้ลคลิกที่ไฟล์สำหรับระบบของคุณ:
*   **Windows**: ดับเบิ้ลคลิก `run.bat`
*   **macOS / Linux**: เปิด Terminal แล้วรัน `./run.sh`

โปรแกรมจะตรวจสอบและติดตั้งตัวช่วย (Dependencies) ที่จำเป็นให้อัตโนมัติ แล้วเปิดหน้าเว็บขึ้นมา

---

# MyPDFCleaner (English)

**MyPDFCleaner** is a secure, local web application to redact sensitive text from PDFs and export them to editable formats, featuring a modern Glassmorphism UI.

## ✨ Key Features
*   **User-Friendly**: Drag & drop interface running locally in your browser.
*   **Modern UI**: Beautiful Glassmorphism design with bilingual support (TH/EN).
*   **Redaction**: Remove specific words or phrases instantly.
*   **Auto-Redaction**: Automatically detect and remove:
    *   📧 Emails
    *   📱 Phone Numbers
    *   🆔 ID Cards / Govt IDs
    *   💳 Or select "All Sensitive Data" for one-click privacy.
*   **Export Tools**:
    *   Convert PDF to **Word (.docx)** (Editable).
    *   Convert PDF to **Text (.txt)**.
*   **OCR Integration**: Built-in support for Tesseract OCR to process scanned documents.
*   **Secure**: All processing happens locally on your machine. No cloud uploads.

---

## 🚀 Installation & Usage

### 1. Prerequisites
*   **Python**: Install [Python](https://www.python.org/downloads/) (Ensure "Add to PATH" is checked).
*   **Tesseract OCR**:
    *   **Windows**: Program attempts auto-install via Winget, or download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
    *   **macOS**: `brew install tesseract tesseract-lang`
    *   **Linux**: `sudo apt install tesseract-ocr tesseract-ocr-tha`

### 2. How to Run
Simply execute the script for your OS:
*   **Windows**: Double-click `run.bat`
*   **macOS / Linux**: Run `./run.sh` in terminal.

The script will automatically install dependencies (in a virtual environment) and launch the web interface.
