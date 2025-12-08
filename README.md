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

## 🚀 วิธีติดตั้งและใช้งาน (Installation)

**ทำเพียงแค่ข้อเดียว:**
*   **Windows**: ดับเบิ้ลคลิก `run.bat`
*   **macOS / Linux**: เปิด Terminal แล้วรัน `./run.sh`

**🔥 ระบบจะจัดการให้เองทั้งหมด (All-in-One):**
1.  ติดตั้ง/ตรวจสอบ **Python Environment**
2.  ติดตั้ง **Ghostscript** (สำหรับจัดการ PDF)
3.  ติดตั้ง **Tesseract OCR** (สำหรับอ่านภาพ)
4.  ดาวน์โหลด **ไฟล์ภาษาไทย/อังกฤษ (Language Data)** ให้เอง

*หมายเหตุ: หากเป็น Windows ระบบอาจขอให้ท่านกด "Yes" เพื่อติดตั้ง Ghostscript ในครั้งแรกเท่านั้น*
*หมายเหตุ (macOS/Linux): หากยังไม่มี dependencies ระบบจะแจ้งคำสั่งติดตั้งให้ทราบ (เช่น brew/apt)*

---

## 🐳 การใช้งานด้วย Docker (แนะนำสำหรับ Server)

### วิธีที่ 1: Docker Compose (ง่ายที่สุด)
```bash
docker-compose up -d --build
```
เข้าใช้งานได้ที่: `http://localhost:5000`

### วิธีที่ 2: Kubernetes (K8s)
หากท่านมี K8s Cluster อยู่แล้ว:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

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

**Just one step:**
*   **Windows**: Double-click `run.bat`
*   **macOS / Linux**: Run `./run.sh` in your terminal.

**🔥 The script automatically handles:**
1.  **Python Environment** setup.
2.  **Ghostscript** downloading & installation (Automated).
3.  **Tesseract OCR** & **Language Data (Thai/Eng)** downloading.

*Note (Windows): You may be prompted to allow the Ghostscript installer to run.*
*Note (macOS/Linux): If system packages are missing, the script will attempt to install them via `brew` or `apt`.*

### 🐳 Docker Support

**Using Docker Compose:**
```bash
docker-compose up -d --build
```
Access at: `http://localhost:5000`

**Using Kubernetes:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
