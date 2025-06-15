# 📄 Notebook Printing Environment Guide

This guide explains how to use the dedicated `notebook-print` conda environment for converting Jupyter notebooks to various formats.

## 🚀 Quick Start

### Activate the Environment
```bash
conda activate notebook-print
```

### Basic Conversions
```bash
# PDF via LaTeX (recommended for academic/professional documents)
python notebook_printer.py notebook.ipynb --format pdf

# Web-based PDF (better for interactive content)
python notebook_printer.py notebook.ipynb --format webpdf

# HTML export
python notebook_printer.py notebook.ipynb --format html

# Clean report (no code, only outputs)
python notebook_printer.py notebook.ipynb --format pdf --no-input --output report
```

## 🛠 Environment Details

**Python Version:** 3.10.18  
**Key Packages:**
- `nbconvert` 7.16.6 - Core conversion engine
- `mercury` 2.4.3 - Interactive dashboard creation  
- `pandoc` 3.7.0.2 - Document conversion
- `texlive-core` - LaTeX engine for PDF generation
- `playwright` 1.52.0 - Modern web browser automation
- `weasyprint` 65.1 - CSS-based PDF generation

## 📋 Available Conversion Methods

### 1. PDF via LaTeX (`--format pdf`)
**Best for:** Academic papers, professional reports, mathematical content
- High-quality typography
- Excellent equation rendering
- Automatic page breaking
- Professional appearance

### 2. Web-based PDF (`--format webpdf`)
**Best for:** Interactive content, modern styling, complex layouts
- Preserves web styling
- Better handling of interactive plots
- Modern CSS support
- Can handle complex HTML/CSS

### 3. HTML Export (`--format html`)
**Best for:** Web publishing, interactive viewing
- Fully interactive plots
- Responsive design
- Easy web deployment

## 🎯 Advanced Usage

### Command Line Options
```bash
# Create clean report without code
python notebook_printer.py notebook.ipynb --no-input

# Remove input/output prompts for cleaner look
python notebook_printer.py notebook.ipynb --no-prompt

# Custom output filename
python notebook_printer.py notebook.ipynb --output my_report

# Combine options
python notebook_printer.py notebook.ipynb --format webpdf --no-input --no-prompt --output final_report
```

### Mercury Dashboard
```bash
# Start Mercury server for interactive dashboards
mercury run

# Access at http://localhost:8000
```

### Direct Python API
```python
import nbconvert

# PDF conversion
exporter = nbconvert.PDFExporter()
(body, resources) = exporter.from_filename('notebook.ipynb')
with open('output.pdf', 'wb') as f:
    f.write(body)

# WebPDF conversion
exporter = nbconvert.WebPDFExporter()
exporter.allow_chromium_download = True
(body, resources) = exporter.from_filename('notebook.ipynb')
with open('output.pdf', 'wb') as f:
    f.write(body)
```

## 🔧 Troubleshooting

### Common Issues

**1. LaTeX errors:**
- Install missing LaTeX packages: `tlmgr install <package>`
- Use webpdf format as alternative

**2. Large notebooks timing out:**
- Split notebook into smaller sections
- Use PDF format instead of webpdf
- Increase timeout in code

**3. Missing fonts:**
- Fonts are included in the environment
- For custom fonts, add to system font directory

### Environment Management
```bash
# Update packages
conda update --all -c conda-forge

# Install additional packages
conda install -c conda-forge package_name

# List installed packages
conda list

# Environment info
conda info --envs
```

## 📁 File Organization

```
project/
├── notebook.ipynb              # Source notebook
├── notebook_printer.py         # Conversion utility
├── output_pdf.pdf             # LaTeX PDF output
├── output_webpdf.pdf          # Web PDF output  
├── output_html.html           # HTML output
└── clean_report.pdf           # Report without code
```

## 🎨 Customization

### Custom Templates
Create custom LaTeX or HTML templates:
```bash
# Use custom template
jupyter nbconvert --to pdf notebook.ipynb --template custom_template.tplx
```

### Styling Options
```python
# Custom CSS for HTML
exporter = nbconvert.HTMLExporter()
exporter.template_file = 'custom_template.html.j2'

# Custom LaTeX styling
exporter = nbconvert.PDFExporter()
exporter.template_file = 'custom_template.tex.j2'
```

## 🔄 Workflow Integration

### Automated Conversion
Create a script for batch processing:
```bash
#!/bin/bash
for notebook in *.ipynb; do
    python notebook_printer.py "$notebook" --format pdf --no-input
done
```

### CI/CD Integration
Add to your build pipeline:
```yaml
# GitHub Actions example
- name: Convert notebooks
  run: |
    conda activate notebook-print
    python notebook_printer.py report.ipynb --format pdf
```

---

**Environment created:** `notebook-print`  
**Python version:** 3.10.18  
**Compatible with:** Mercury, Pandoc, LaTeX, Modern browsers

