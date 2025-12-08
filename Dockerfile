# Use official Python 3.9 image
FROM python:3.9-slim

# Install system dependencies (Ghostscript + Tesseract + Thai Lang)
RUN apt-get update && apt-get install -y \
    ghostscript \
    tesseract-ocr \
    tesseract-ocr-tha \
    libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Check Tesseract version during build
RUN tesseract --version

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
