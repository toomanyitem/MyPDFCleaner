import os
import uuid
import shutil
import re
import subprocess
import io
import logging
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, send_file, after_this_request, jsonify

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
logging.getLogger('werkzeug').setLevel(logging.ERROR) # Quiet werkzeug logs to file

from utils.text_cleaner import remove_texts_from_pdf
try:
    from utils.exporter import convert_to_text, convert_to_word
except ImportError:
    # Handle case where utils module is not found (e.g. if running from wrong dir)
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from utils.exporter import convert_to_text, convert_to_word

try:
    import ocrmypdf
except ImportError:
    ocrmypdf = None

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def setup_tesseract_path():
    """Attempt to find Tesseract in common Windows paths and add to PATH."""
    if shutil.which('tesseract'):
        return # Already in PATH

    common_paths = [
        r"C:\Program Files\Tesseract-OCR",
        r"C:\Program Files (x86)\Tesseract-OCR",
        os.path.expanduser(r"~\AppData\Local\Tesseract-OCR"),
        "/opt/homebrew/bin",  # macOS Homebrew (Apple Silicon)
        "/usr/local/bin",     # macOS Homebrew (Intel) / Linux
        "/usr/bin"            # Standard Linux
    ]
    
    for p in common_paths:
        if os.path.exists(os.path.join(p, 'tesseract.exe')):
            print(f"Found Tesseract at: {p}")
            os.environ["PATH"] += os.pathsep + p
            return

# Run setup on module load
setup_tesseract_path()

# Regex Definitions
PATTERNS = {
    'EMAIL': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'PHONE': r'\b(?:\+?66|0)(?:\d\s?-?){8,9}\d\b',
    'ID_CARD': r'\b\d{13}\b',
    # Credit card is tricky to avoid false positives, but valid for cleaning
    'CREDIT_CARD': r'\b(?:\d[ -]*?){13,16}\b' 
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check_ocr', methods=['GET'])
def check_ocr():
    # Check if Tesseract is available in PATH
    tesseract_available = shutil.which('tesseract') is not None
    return jsonify({'available': tesseract_available})

@app.route('/api/export', methods=['POST'])
def export_pdf():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400
    
    file = request.files['file']
    fmt = request.form.get('format', 'txt') # txt or docx
    use_ocr = request.form.get('use_ocr') == 'true'

    if file.filename == '':
        return {'error': 'No file selected'}, 400

    filename = f"{uuid.uuid4()}_{file.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    ocr_output_path = os.path.join(UPLOAD_FOLDER, f"ocr_{filename}")
    
    file.save(input_path)
    
    current_input_path = input_path
    temp_files = [input_path]

    try:
        # 1. OCR Step (Optional but recommended for export)
        if use_ocr:
            if not shutil.which('tesseract'):
                return {'error': 'OCR requested but Tesseract not installed.'}, 400
            try:
                # force_ocr=True involves rasterizing pages which is slow but accurate for images.
                # skip_text=True is generally faster if existing text is fine.
                # converting to word/txt needs good text layer.
                ocrmypdf.ocr(input_path, ocr_output_path, skip_text=True, language='tha+eng')
                current_input_path = ocr_output_path
                temp_files.append(ocr_output_path)
            except Exception as e:
                logging.error(f"OCR Error: {e}", exc_info=True)
                print(f"OCR Error: {e}")
                pass 

        # 2. Convert Step
        if fmt == 'docx':
            output_filename = f"converted_{filename}.docx"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            success = convert_to_word(current_input_path, output_path)
        else:
            output_filename = f"converted_{filename}.txt"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            success = convert_to_text(current_input_path, output_path)

        if not success:
             return {'error': 'Conversion failed'}, 500
        
        temp_files.append(output_path)

        # Read to memory
        return_data = io.BytesIO()
        with open(output_path, 'rb') as f:
            return_data.write(f.read())
        return_data.seek(0)
        
        # Cleanup immediately
        for p in temp_files:
            try:
                if os.path.exists(p): os.remove(p)
            except: pass

        return send_file(return_data, as_attachment=True, download_name=output_filename)

    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/process', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400
    
    file = request.files['file']
    texts = request.form.get('texts', '')
    use_ocr = request.form.get('use_ocr') == 'true'
    selected_patterns = request.form.get('patterns', '').split(',')
    
    if file.filename == '':
        return {'error': 'No file selected'}, 400

    # Parse inputs
    texts_to_remove = [t.strip() for t in texts.replace(',', '\n').split('\n') if t.strip()]
    
    regex_map = {}
    for p in selected_patterns:
        p = p.strip().upper()
        if p == 'ALL_SENSITIVE':
            # Add all known patterns
            for key in PATTERNS:
                regex_map[key] = PATTERNS[key]
        elif p in PATTERNS:
            regex_map[p] = PATTERNS[p]

    # Save uploaded file
    filename = f"{uuid.uuid4()}_{file.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    ocr_output_path = os.path.join(UPLOAD_FOLDER, f"ocr_{filename}")
    final_output_path = os.path.join(UPLOAD_FOLDER, f"cleaned_{filename}")
    
    file.save(input_path)

    try:
        current_input_path = input_path

        # 1. OCR Step (Optional)
        if use_ocr:
            if not shutil.which('tesseract'):
                return {'error': 'OCR requested but Tesseract not installed on server.'}, 400
            
            try:
                # Run OCR and save to intermediate file
                print("Starting OCR...")
                ocrmypdf.ocr(input_path, ocr_output_path, skip_text=True, language='tha+eng')
                current_input_path = ocr_output_path
            except Exception as e:
                logging.error(f"OCR Process Error: {e}", exc_info=True)
                print(f"OCR Error: {e}")
                return {'error': f"OCR Process Failed: {str(e)}"}, 500

        # 2. Text/Regex Removal Step
        remove_texts_from_pdf(current_input_path, final_output_path, texts_to_remove, regex_patterns=regex_map)

        if not os.path.exists(final_output_path):
             return {'error': 'Processing failed to create output file'}, 500

        # Read to memory
        return_data = io.BytesIO()
        with open(final_output_path, 'rb') as f:
            return_data.write(f.read())
        return_data.seek(0)
        
        # Cleanup files immediately
        for p in [input_path, ocr_output_path, final_output_path]:
            try:
                if os.path.exists(p): os.remove(p)
            except: pass

        return send_file(return_data, as_attachment=True, download_name=f"cleaned_{file.filename}")

    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')
    
    print("====================================================")
    print("🚀  MyPDFCleaner Server Started Successfully!")
    print("====================================================")
    print("📌  Local Address:   http://127.0.0.1:5000")
    print("📌  Network Address: http://0.0.0.0:5000 (If enabled)")
    print("====================================================")
    print("🌐  Browser will open automatically in 1.5 seconds...")
    print("❌  DO NOT CLOSE THIS WINDOW (ห้ามปิดหน้าต่างนี้)")
    print("====================================================")
    
    Timer(1.5, open_browser).start()
    app.run(debug=True, port=5000, use_reloader=False) # Disable reloader to prevent double-open
