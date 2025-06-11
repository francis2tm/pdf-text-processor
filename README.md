# PDF Text Processor

A minimal PDF text extraction and rendering tool using PyMuPDF.

## Description

This project demonstrates a simple approach to extracting text blocks from a PDF and rendering them back as-is, without translation. It uses only PyMuPDF for both text extraction and rendering, making it lightweight and efficient.

## Features

- Extract text blocks from PDF using PyMuPDF's native text block detection
- Preserve original text layout and positioning
- Render text back to PDF with minimal styling
- Simple, dependency-light implementation

## Installation

1. Make sure you have Python 3.9+ and Poetry installed
2. Clone this repository
3. Install dependencies:

```bash
poetry install
```

4. Activate the Poetry virtual environment:

```bash
poetry shell
```

## Usage

### Option 1: Using Poetry Shell (Recommended)

1. Activate the Poetry virtual environment:

```bash
poetry shell
```

2. Place your PDF file as `input.pdf` in the project directory

3. Run the processor:

```bash
python main.py
```

4. The processed PDF will be saved as `output.pdf`

### Option 2: Using Poetry Run

1. Place your PDF file as `input.pdf` in the project directory
2. Run the processor:

```bash
poetry run python main.py
```

3. The processed PDF will be saved as `output.pdf`

## How it Works

1. **Text Extraction**: Uses PyMuPDF's `get_text("dict")` to extract text organized by blocks
2. **Block Processing**: Converts PyMuPDF text blocks into simple data structures
3. **Rendering**: Redacts original text areas and inserts the same text back with basic HTML styling

## Example

The project includes a sample PDF (`input.pdf`) - the Red Hat Virtualization table of contents document.

## Dependencies

- `pymupdf` - For PDF text extraction and rendering

## Project Structure

```
pdf-text-processor/
├── pdf_processor.py    # Main PDF processing logic
├── main.py            # CLI script
├── input.pdf          # Sample input PDF
├── pyproject.toml     # Poetry configuration
└── README.md          # This file
```

## License

This project is provided as-is for educational and demonstration purposes.
