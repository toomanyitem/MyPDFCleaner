#!/bin/bash
echo "Starting MyPDFCleaner Web Server..."
echo "=============================================="

# 1. Check for Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "[!] Tesseract OCR not found."
    
    # Check OS type
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo "Attempting to install via Homebrew..."
            brew install tesseract
            brew install tesseract-lang
        else
            echo "Homebrew not found. Please install tesseract manually: brew install tesseract"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
             echo "Attempting to install via apt-get (requires sudo)..."
             sudo apt-get update && sudo apt-get install -y tesseract-ocr tesseract-ocr-tha
        else
             echo "Please install tesseract manually (e.g., sudo apt install tesseract-ocr)"
        fi
    fi
fi

# 2. Check/Create Virtual Environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

echo "Checking dependencies..."
pip install -r requirements.txt

# 3. Run App
# Run the application
python3 app.py

echo ""
echo "Application stopped."
read -p "Press Enter to exit..."
