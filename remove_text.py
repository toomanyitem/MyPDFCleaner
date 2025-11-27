import fitz
import os


def remove_texts_from_pdf(input_pdf_path, output_pdf_path, texts_to_remove):
    if not texts_to_remove:
        print("❗ ไม่มีรายการข้อความที่จะลบ → ยกเลิก.")
        return

    try:
        doc = fitz.open(input_pdf_path)
        found_counts = {text: 0 for text in texts_to_remove}
        total_found = 0

        for page in doc:
            has_edit = False
            for text in texts_to_remove:
                areas = page.search_for(text)
                if areas:
                    found_counts[text] += len(areas)
                    total_found += len(areas)
                    has_edit = True
                    for rect in areas:
                        page.add_redact_annot(rect)
            if has_edit:
                page.apply_redactions(images=0, graphics=0)

        doc.save(output_pdf_path)
        doc.close()
        print(f"\n📁 ไฟล์ใหม่ถูกบันทึกแล้ว → {output_pdf_path}")
        print("📊 รายการที่ถูกลบ:")
        for k, v in found_counts.items():
            print(f"  • {k} → {v} จุด")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด ❗ {e}")


def ask_texts():
    print("\nกรอกข้อความที่จะลบ (ENTER ว่างหรือ done เพื่อประมวลผล)\n")
    data = []
    while True:
        t = input("ข้อความ: ").strip()
        if t == "" or t.lower() in ["done", "จบ", "q", "exit"]:
            break
        data.append(t)
    return data


if __name__ == "__main__":
    input_file = input("\n📄 ระบุชื่อไฟล์ PDF ที่ต้องการลบข้อความ: ").strip()
    if not os.path.exists(input_file):
        print(f"❗ ไม่พบไฟล์ {input_file} ในโฟลเดอร์")
        exit()

    output_file = input("📁 ชื่อไฟล์ที่จะบันทึกใหม่ (default: cleaned_output.pdf): ").strip()
    if output_file == "":
        output_file = "cleaned_output.pdf"

    print("\n================ START =================")
    print(f"Input : {input_file}")
    print(f"Output: {output_file}")
    print("========================================\n")

    items = ask_texts()
    remove_texts_from_pdf(input_file, output_file, items)
