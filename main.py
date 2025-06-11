#!/usr/bin/env python3
"""
PDF Text Processor - Minimal PDF text extraction and rendering
"""

from pdf_processor import process_pdf

def main():
    """Main function to process the input PDF."""
    input_file = "input.pdf"
    output_file = "output.pdf"
    
    try:
        # Read input PDF
        with open(input_file, "rb") as f:
            pdf_data = f.read()
        
        print(f"Processing {input_file}...")
        
        # Process (extract text blocks and render them back)
        result = process_pdf(pdf_data)
        
        # Save output
        with open(output_file, "wb") as f:
            f.write(result)
        
        print(f"Processing complete! Output saved to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please place your PDF file as 'input.pdf' in this directory.")
    except Exception as e:
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    main() 