import fitz
import os
import re

def remove_texts_from_pdf(input_pdf_path, output_pdf_path, texts_to_remove, regex_patterns=None):
    if not texts_to_remove and not regex_patterns:
        print("❗ ไม่มีรายการข้อความที่จะลบ → ยกเลิก.")
        return

    try:
        doc = fitz.open(input_pdf_path)
        found_counts = {text: 0 for text in texts_to_remove}
        regex_counts = {}
        if regex_patterns:
            for name, pattern in regex_patterns.items():
                regex_counts[name] = 0

        total_found = 0

        for page in doc:
            has_edit = False
            
            # 1. Exact Text Search
            for text in texts_to_remove:
                if not text: continue
                areas = page.search_for(text)
                if areas:
                    found_counts[text] += len(areas)
                    total_found += len(areas)
                    has_edit = True
                    for rect in areas:
                        page.add_redact_annot(rect)

            # 2. Regex Search
            if regex_patterns:
                # PyMuPDF doesn't support direct regex search easily across lines, 
                # but we can iterate words or text blocks. 
                # A simpler approach for robust regex: Get all text, find matches, search for matches.
                # However, search_for returns all instances of a string.
                # If regex matches "ABC", search_for("ABC") works.
                
                # Get full text of the page
                page_text = page.get_text("text")
                
                for name, pattern in regex_patterns.items():
                    matches = set(re.findall(pattern, page_text))
                    for match in matches:
                        # Search for the exact string found by regex
                        areas = page.search_for(match)
                        if areas:
                            regex_counts[name] += len(areas)
                            total_found += len(areas)
                            has_edit = True
                            for rect in areas:
                                page.add_redact_annot(rect)

            if has_edit:
                # images=2 (ignore), graphics=2 (ignore) -> Text only
                page.apply_redactions(images=2, graphics=2) 


        doc.save(output_pdf_path)
        doc.close()
        print(f"\n📁 ไฟล์ใหม่ถูกบันทึกแล้ว → {output_pdf_path}")
        print("📊 รายการที่ถูกลบ:")
        for k, v in found_counts.items():
            print(f"  • {k} → {v} จุด")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด ❗ {e}")
