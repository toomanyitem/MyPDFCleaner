# MyPDFCleaner 🧹

A small utility to **remove specific text strings from a PDF** using Python + [PyMuPDF](https://pymupdf.readthedocs.io/).  
It supports **multiple text patterns** in one run: you type them in the terminal line by line, then the script will redact them from every page and save a cleaned PDF.

> 📝 Designed for macOS / Linux (command-line based). Windows users can adapt the commands manually.

---

## Features

- ✅ Remove **multiple text strings** in a single run  
- ✅ Uses **redaction**, so removed text is not just hidden but actually gone from the content layer  
- ✅ Keeps the **original PDF unchanged**, writes a new cleaned file instead  
- ✅ Shows a **summary of how many matches** were found and removed for each text

---

## Requirements

- Python **3.8+**
- `python3` available in your terminal
- `pip` for installing dependencies

To check Python:

```bash
python3 --version
