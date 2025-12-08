import fitz
from docx import Document

def convert_to_text(pdf_path, output_path):
    """Extract text from PDF and save as .txt"""
    try:
        doc = fitz.open(pdf_path)
        with open(output_path, "w", encoding="utf-8") as f:
            for page in doc:
                text = page.get_text()
                f.write(text)
                f.write("\n" + "-"*20 + "\n") # Page separator
        return True
    except Exception as e:
        print(f"Error converting to text: {e}")
        return False

def convert_to_word(pdf_path, output_path):
    """Extract text from PDF and preserve paragraphs for .docx"""
    try:
        doc = fitz.open(pdf_path)
        document = Document()
        
        for page in doc:
            # get_text("blocks") returns a list of text blocks
            # (x0, y0, x1, y1, "lines of text", block_no, block_type)
            blocks = page.get_text("blocks")
            blocks.sort(key=lambda b: b[1]) # Sort by vertical position (y0)
            
            for b in blocks:
                if b[6] == 0: # text block
                    text = b[4].strip()
                    if text:
                        document.add_paragraph(text)
            
            document.add_page_break()
            
        document.save(output_path)
        return True
    except Exception as e:
        print(f"Error converting to word: {e}")
        return False
