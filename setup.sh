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
