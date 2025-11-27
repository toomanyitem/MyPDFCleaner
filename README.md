
1️⃣ ไฟล์ setup.sh

สร้างไฟล์ชื่อ setup.sh ไว้ที่ root ของโปรเจกต์ (โฟลเดอร์เดียวกับ README.md) แล้ววางโค้ดนี้:

#!/usr/bin/env bash
set -e

echo "======================================="
echo "  MyPDFCleaner - Setup Script"
echo "======================================="

# ใช้โฟลเดอร์ปัจจุบันเป็นโปรเจกต์
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/4] Creating virtual environment (venv)..."
python3 -m venv venv

echo "[2/4] Activating virtual environment..."
# shellcheck source=/dev/null
source venv/bin/activate

echo "[3/4] Installing dependencies (PyMuPDF)..."
pip install --upgrade pip
pip install pymupdf

echo "[4/4] Creating remove_text.py..."
cat << 'EOF' > remove_text.py
import fitz  # PyMuPDF


def remove_texts_from_pdf(input_pdf_path, output_pdf_path, texts_to_remove):
    """
    Remove multiple text strings from all pages in a PDF using redaction.

    :param input_pdf_path: Path to the input PDF file
    :param output_pdf_path: Path to the output (cleaned) PDF file
    :param texts_to_remove: List of strings to search and remove
    """
    if not texts_to_remove:
        print("❗ No texts provided. Nothing to remove.")
        return

    try:
        doc = fitz.open(input_pdf_path)

        found_counts = {text: 0 for text in texts_to_remove}
        total_found = 0

        for page_index, page in enumerate(doc):
            has_redactions = False

            for text in texts_to_remove:
                areas = page.search_for(text)
                if areas:
                    found_counts[text] += len(areas)
                    total_found += len(areas)
                    has_redactions = True

                    for rect in areas:
                        page.add_redact_annot(rect)

            if has_redactions:
                page.apply_redactions(images=0, graphics=0)

        doc.save(output_pdf_path)
        doc.close()

        print("\n================ RESULT ================")
        print(f"🔍 Total removed occurrences: {total_found}\n")
        for t, c in found_counts.items():
            print(f"   • '{t}' → {c} matches")
        print(f"\n📁 Output saved to: {output_pdf_path}")
        print("========================================\n")

    except Exception as e:
        print(f"Error: {e}")


def ask_texts():
    """
    Ask user to input multiple texts to remove.
    User can input line by line and type 'done' or press ENTER on an empty line to finish.
    """
    print("\nEnter texts you want to remove (one per line).")
    print("Press ENTER on an empty line or type 'done' / 'จบ' / 'q' to start processing.\n")

    items = []
    while True:
        t = input("Text to remove: ").strip()
        if t == "" or t.lower() in ["done", "จบ", "q", "quit", "exit"]:
            break
        items.append(t)

    return items


if __name__ == "__main__":
    input_file = "xy_vending_command.pdf"
    output_file = "xy_vending_command_cleaned.pdf"

    texts_to_remove = ask_texts()

    if not texts_to_remove:
        print("❗ No texts entered. Abort.")
    else:
        remove_texts_from_pdf(input_file, output_file, texts_to_remove)
EOF

echo "---------------------------------------"
echo "✅ Setup completed."
echo "Next steps:"
echo "  1) Put your PDF file as: xy_vending_command.pdf in this folder."
echo "  2) Activate venv: source venv/bin/activate"
echo "  3) Run: python remove_text.py"
echo "---------------------------------------"

จากนั้นในเครื่องจริง (macOS / Linux) อย่าลืมให้สิทธิ์รัน:

chmod +x setup.sh


⸻

2️⃣ ไฟล์ README.md สำหรับ GitHub

สร้างไฟล์ README.md แล้ววางเนื้อหานี้ได้เลย:

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


⸻

Getting Started

1. Clone this repository

git clone https://github.com/your-username/MyPDFCleaner.git
cd MyPDFCleaner

Replace your-username with your actual GitHub username and clone URL.

⸻

2. Run the setup script

The project comes with a helper script that:
	•	creates a virtual environment (venv)
	•	installs PyMuPDF
	•	generates remove_text.py automatically

chmod +x setup.sh
./setup.sh

After this completes, your project folder will look like:

MyPDFCleaner/
├── venv/
├── remove_text.py
├── setup.sh
└── README.md


⸻

3. Prepare your PDF file

Place the PDF you want to clean in the project folder and rename it to:

xy_vending_command.pdf

Final structure example:

MyPDFCleaner/
├── venv/
├── remove_text.py
├── setup.sh
├── README.md
└── xy_vending_command.pdf     # ← your input PDF

You can change this filename later in remove_text.py if you want.
See Customization￼ below.

⸻

4. Activate the virtual environment

source venv/bin/activate

On Windows, use: venv\Scripts\activate

You should see something like (venv) at the beginning of your terminal prompt.

⸻

5. Run the script

python remove_text.py

You will be prompted to enter texts you want to remove:

Enter texts you want to remove (one per line).
Press ENTER on an empty line or type 'done' / 'จบ' / 'q' to start processing.

Text to remove: Hunan Xing Yuan Technology Co., Ltd
Text to remove: XY Vending
Text to remove: www.xy-vending.com
Text to remove: done

After you finish entering texts:
	•	The script will scan all pages of xy_vending_command.pdf
	•	All occurrences of the given texts will be redacted
	•	A new file will be created:

xy_vending_command_cleaned.pdf


⸻

Example Output

A typical run might print:

================ RESULT ================
🔍 Total removed occurrences: 12

   • 'Hunan Xing Yuan Technology Co., Ltd' → 4 matches
   • 'XY Vending' → 3 matches
   • 'www.xy-vending.com' → 5 matches

📁 Output saved to: xy_vending_command_cleaned.pdf
========================================


⸻

Customization

You can modify the behavior in remove_text.py:

if __name__ == "__main__":
    input_file = "xy_vending_command.pdf"
    output_file = "xy_vending_command_cleaned.pdf"

	•	Change input_file to accept a different input filename
	•	Change output_file to control the output filename

You could also extend the script to:
	•	read texts-to-remove from a .txt file
	•	accept filenames and patterns via command-line arguments
	•	batch-process multiple PDFs

⸻

Troubleshooting

Nothing seems to be removed 🤔

Common reasons:
	•	The PDF is actually a scanned image (no real text layer).
In this case, OCR is required before this tool can work.
	•	The text in the PDF is split in strange ways (e.g. “H u n a n”).
Try searching for a shorter or more generic portion of the string.

ModuleNotFoundError: No module named 'fitz'

Most likely the virtual environment is not activated or dependencies not installed.
	•	Ensure:

source venv/bin/activate
pip install pymupdf


	•	Or re-run:

./setup.sh



Permission denied when running setup.sh

Make it executable first:

chmod +x setup.sh
./setup.sh

Want to go back to system Python

Deactivate the virtual environment:

deactivate


⸻

Folder Layout (Recap)

MyPDFCleaner/
├── venv/                         # Virtual environment (auto-created by setup.sh)
├── remove_text.py                # Main script (auto-generated)
├── setup.sh                      # Setup helper script
├── README.md                     # Project documentation
└── xy_vending_command.pdf        # Your input PDF (you provide this)


⸻

Roadmap / Ideas
	•	Add CLI arguments (input/output file flags)
	•	Add support for text patterns from a config file
	•	Basic GUI (Tkinter / web UI) for drag-and-drop PDF cleaning

Feel free to open issues or pull requests if you want to extend this tool. 🙌

--
