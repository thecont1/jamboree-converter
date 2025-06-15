# 📏 Page Size Control Guide for Jupyter Notebooks

Complete guide for controlling PDF page sizes when converting Jupyter notebooks.

## 🚀 Quick Start

```bash
# Activate the notebook-print environment
conda activate notebook-print

# A3 Portrait (recommended for data science notebooks)
python page_size_converter.py notebook.ipynb --size a3

# A2 Landscape (great for wide plots and tables)
python page_size_converter.py notebook.ipynb --size a2 --orientation landscape

# A1 for posters
python page_size_converter.py notebook.ipynb --size a1
```

## 📐 Available Page Sizes

| Size | Dimensions (mm) | Best For |
|------|----------------|----------|
| **A4** | 210 × 297 | Standard documents, reports |
| **A3** | 297 × 420 | Data analysis, charts |
| **A2** | 420 × 594 | Large datasets, dashboards |
| **A1** | 594 × 841 | Posters, presentations |
| **A0** | 841 × 1189 | Large format posters |
| **Letter** | 216 × 279 | US standard |
| **Legal** | 216 × 356 | US legal documents |
| **Tabloid** | 279 × 432 | Newspapers, large prints |

## 🎯 Methods Available

### 1. WebPDF (Recommended) 🌐
**Best for:** Modern styling, complex layouts, interactive content
- Uses Chromium browser engine
- CSS-based page size control
- Excellent rendering quality
- Handles complex HTML/CSS

```bash
python page_size_converter.py notebook.ipynb --size a3 --method webpdf
```

### 2. LaTeX PDF 📜
**Best for:** Academic documents, mathematical content
- Traditional LaTeX typesetting
- High-quality equation rendering
- Professional typography
- Better for text-heavy documents

```bash
python page_size_converter.py notebook.ipynb --size a3 --method latex
```

### 3. Both Methods 🔄
**For comparison and testing**
```bash
python page_size_converter.py notebook.ipynb --size a3 --method both
```

## 📋 Common Use Cases

### Data Science Reports
```bash
# A3 portrait for standard data analysis
python page_size_converter.py analysis.ipynb --size a3

# A2 landscape for wide visualizations
python page_size_converter.py dashboard.ipynb --size a2 --orientation landscape

# Clean report without code
python page_size_converter.py report.ipynb --size a3 --no-input
```

### Academic Papers
```bash
# A4 with LaTeX for academic formatting
python page_size_converter.py paper.ipynb --size a4 --method latex

# Remove prompts for cleaner look
python page_size_converter.py paper.ipynb --size a4 --no-prompt
```

### Presentations & Posters
```bash
# A1 landscape for poster
python page_size_converter.py poster.ipynb --size a1 --orientation landscape

# A0 for large format
python page_size_converter.py poster.ipynb --size a0
```

## ⚙️ Advanced Options

### Custom Margins
```bash
# Larger margins
python page_size_converter.py notebook.ipynb --size a3 --margins 30mm

# Different units
python page_size_converter.py notebook.ipynb --size a3 --margins 1in
python page_size_converter.py notebook.ipynb --size a3 --margins 2cm
```

### Content Control
```bash
# Exclude code cells (report mode)
python page_size_converter.py notebook.ipynb --size a3 --no-input

# Exclude input/output prompts
python page_size_converter.py notebook.ipynb --size a3 --no-prompt

# Both (cleanest output)
python page_size_converter.py notebook.ipynb --size a3 --no-input --no-prompt
```

### Custom Output Names
```bash
# Custom filename
python page_size_converter.py notebook.ipynb --size a3 --output final_report

# Will create: final_report.pdf
```

## 🎨 Page Size Recommendations

### By Content Type

**📊 Data Visualizations:**
- **A3 Portrait**: Standard charts, medium datasets
- **A2 Landscape**: Wide charts, time series, correlation matrices
- **A1 Landscape**: Large datasets, complex dashboards

**📝 Text Reports:**
- **A4 Portrait**: Standard reports, documentation
- **A3 Portrait**: Reports with embedded charts
- **Legal**: US-style reports

**🎯 Presentations:**
- **A3 Landscape**: Slide-style layout
- **A2 Landscape**: Large presentation format
- **Tabloid**: Newspaper-style layout

**🔬 Academic/Scientific:**
- **A4 Portrait**: Papers, articles (LaTeX method)
- **A3 Portrait**: Lab reports with data
- **A1/A0**: Conference posters

## 📏 Size Comparison Visual

```
A0: █████████████████████ (841×1189mm)
A1: ██████████████       (594×841mm)
A2: ██████████           (420×594mm)  
A3: ███████              (297×420mm)  ← Great for data science
A4: █████                (210×297mm)  ← Standard
A5: ███                  (148×210mm)
```

## 🔧 Troubleshooting

### Common Issues

**WebPDF timeout:**
```bash
# For very large notebooks, use LaTeX method
python page_size_converter.py large_notebook.ipynb --size a3 --method latex
```

**LaTeX errors:**
```bash
# Use WebPDF method instead
python page_size_converter.py notebook.ipynb --size a3 --method webpdf
```

**Content too small:**
```bash
# Reduce margins for more content space
python page_size_converter.py notebook.ipynb --size a3 --margins 15mm
```

### Performance Tips

1. **WebPDF** is faster for complex layouts
2. **LaTeX** is better for text-heavy content
3. **A3** is the sweet spot for most data science work
4. **Landscape** orientation works well for wide plots
5. Use `--no-input` for presentation-ready PDFs

## 📄 File Organization

The converter automatically creates descriptive filenames:

```
notebook.ipynb → notebook_webpdf_a3_portrait.pdf
notebook.ipynb → notebook_latex_a2_landscape.pdf
notebook.ipynb → custom_name.pdf (with --output)
```

## 🚀 Batch Processing

For multiple notebooks:

```bash
#!/bin/bash
for notebook in *.ipynb; do
    echo "Converting $notebook to A3..."
    python page_size_converter.py "$notebook" --size a3 --no-input
done
```

---

**Environment:** `notebook-print`  
**Python:** 3.10.18  
**Key tools:** WebPDF (Chromium), LaTeX (XeTeX), CSS @page rules

