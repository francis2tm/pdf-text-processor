import pymupdf  # PyMuPDF
from typing import List
import io

# Simple data structures
class SimpleSpan:
    def __init__(self, text: str = ""):
        self.text = text

class SimpleBlock:
    def __init__(self):
        self.spans: List[SimpleSpan] = []
        self.orig_page: int = 0
        self.orig_bbox: str = ""

def format_bbox_to_string(bbox_rect: pymupdf.Rect) -> str:
    """Format bbox as string for storage."""
    return f"{bbox_rect.x0:.2f},{bbox_rect.y0:.2f},{bbox_rect.x1:.2f},{bbox_rect.y1:.2f}"

def extract_blocks(pdf_bytes: bytes) -> List[SimpleBlock]:
    """Extract text blocks from PDF using PyMuPDF only."""
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    all_blocks: List[SimpleBlock] = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Get text organized by blocks using PyMuPDF
        text_dict = page.get_text("dict")
        
        for block_data in text_dict.get("blocks", []):
            if block_data.get("type") == 0:  # Text block (not image)
                # Extract all text from this block
                block_text = ""
                for line in block_data.get("lines", []):
                    line_text = ""
                    for span in line.get("spans", []):
                        line_text += span.get("text", "")
                    if line_text.strip():
                        block_text += line_text + "\n"
                
                # Only create block if it has text content
                if block_text.strip():
                    block = SimpleBlock()
                    span = SimpleSpan(block_text.strip())
                    block.spans = [span]
                    block.orig_page = page_num
                    
                    # Get bounding box from block data
                    bbox = pymupdf.Rect(block_data.get("bbox", (0, 0, 0, 0)))
                    block.orig_bbox = format_bbox_to_string(bbox)
                    
                    all_blocks.append(block)
    
    doc.close()
    return all_blocks

def parse_bbox_string(bbox_str: str) -> pymupdf.Rect:
    """Convert bbox string back to rect."""
    parts = [float(p) for p in bbox_str.split(',')]
    return pymupdf.Rect(parts[0], parts[1], parts[2], parts[3])

def render_blocks(pdf_bytes: bytes, blocks: List[SimpleBlock]) -> bytes:
    """Render blocks back to PDF with minimal styling."""
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    
    # Group blocks by page
    blocks_by_page = {}
    for block in blocks:
        page_num = block.orig_page
        if page_num not in blocks_by_page:
            blocks_by_page[page_num] = []
        blocks_by_page[page_num].append(block)
    
    # Process each page
    for page_num, page_blocks in blocks_by_page.items():
        if page_num >= len(doc):
            continue
            
        page = doc.load_page(page_num)
        
        # Redact original text areas and insert new text
        for block in page_blocks:
            bbox = parse_bbox_string(block.orig_bbox)
            
            # Redact original text
            page.add_redact_annot(bbox, fill=False)
        
        # Apply all redactions at once
        page.apply_redactions()
        
        # Insert new text
        for block in page_blocks:
            bbox = parse_bbox_string(block.orig_bbox)
            
            # Get text from all spans
            text = " ".join(span.text for span in block.spans)
            
            # Insert simplified HTML (just basic text)
            html_content = f'<div style="font-family: Arial; font-size: 12pt;">{text}</div>'
            page.insert_htmlbox(bbox, html_content)
    
    # Save to buffer
    output_buffer = io.BytesIO()
    doc.save(output_buffer, garbage=4, deflate=True)
    doc.close()
    return output_buffer.getvalue()

def process_pdf(input_pdf_bytes: bytes) -> bytes:
    """Main function: extract text blocks and render them back as-is."""
    # Extract blocks
    blocks = extract_blocks(input_pdf_bytes)
    print(f"Extracted {len(blocks)} text blocks")
    
    # Render back to PDF
    output_pdf_bytes = render_blocks(input_pdf_bytes, blocks)
    return output_pdf_bytes 