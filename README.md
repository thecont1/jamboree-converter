# 📏 Quickly Convert Jupyter Notebooks into PDFs 

Here's why you're here: You have a a lengthy Jupyter Notebook (`.ipynb` file) that you want to turn into a PDF that makes for a visually pleasing (or at least bearable) document. And you're looking for a fuss-free tool that will get the job done. 

In goes your notebook into `jamboree_converter.py` and out comes a PDF with a special size of A2 width and A0 height. Check out the included sample.

## 🚀 Quick Start

### 1. Install Miniconda (if you don't already have it)

[anaconda.com/docs/getting-started/miniconda/install](https://www.anaconda.com/docs/getting-started/miniconda/install)

The following commands are ought to be run from the command line of your terminal.

### 2. Create a new virtual environment and activate it:
Replace `my-venv` with whatever you want to call your environment.
```bash
conda create -n my-venv python=3.10
conda activate my-venv
```

### 3. Clone the `jamboree-converter` repo and switch to its directory:
```bash
git clone https://github.com/thecont1/jamboree-converter.git
cd jamboree-converter
```

### 4. Install required packages
```bash
pip install -r requirements.txt
playwright install chromium
```

### 5. Convert your first notebook
Replace `your_notebook.ipynb` with your actual notebook file. Include the full path if the file doesn't exist in your working directory.

Basic conversion (produces a nicely formatted PDF)
```bash
python jamboree_converter.py your_notebook.ipynb --size case_study --method playwright
```

For a cleaner output without code cells
```bash
python jamboree_converter.py your_notebook.ipynb --size case_study --method playwright --no-input
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
| `case_study` | 420 × 1189 | Custom size for lengthy Jupyter Notebooks |


## 🎯 Methods Available

### 1. WebPDF
**Best for:** Modern styling, complex layouts, interactive content
- Uses Chromium browser engine
- CSS-based page size control
- Excellent rendering quality
- Handles complex HTML/CSS

```bash
$ python jamboree_converter.py notebook.ipynb --size a3 --method webpdf
```

### 2. LaTeX PDF
**Best for:** Academic documents, mathematical content
- Traditional LaTeX typesetting
- High-quality equation rendering
- Professional typography
- Better for text-heavy documents

```bash
$ python jamboree_converter.py notebook.ipynb --size a3 --method latex
```

### 3. Playwright
**Best for:** Precise page control and modern web content
- Direct browser automation
- Excellent rendering consistency
- Perfect for complex layouts
- Handles dynamic content well

```bash
$ python jamboree_converter.py notebook.ipynb --size a3 --method playwright
```

### 4. Mercury
**Best for:** Interactive dashboards and sharing
- Creates interactive web dashboards
- Shareable via URL
- Real-time updates
- Great for collaborative work

```bash
$ python jamboree_converter.py notebook.ipynb --method mercury
```

## 📋 Common Use Cases

### Data Science Reports
```bash
# A3 portrait for standard data analysis
$ python jamboree_converter.py analysis.ipynb --size a3

# A2 landscape for wide visualizations
$ python jamboree_converter.py dashboard.ipynb --size a2 --orientation landscape

# Clean report without code
$ python jamboree_converter.py report.ipynb --size a3 --no-input
```

### Academic Papers
```bash
# A4 with LaTeX for academic formatting
$ python jamboree_converter.py paper.ipynb --size a4 --method latex

# Remove prompts for cleaner look
$ python jamboree_converter.py paper.ipynb --size a4 --no-prompt
```

### Presentations & Posters
```bash
# A1 landscape for poster
$ python jamboree_converter.py poster.ipynb --size a1 --orientation landscape

# A0 for large format
$ python jamboree_converter.py poster.ipynb --size a0
```

## ⚙️ Advanced Options

### Custom Margins
```bash
# Larger margins
$ python jamboree_converter.py notebook.ipynb --size a3 --margins 30mm

# Different units
$ python jamboree_converter.py notebook.ipynb --size a3 --margins 1in
$ python jamboree_converter.py notebook.ipynb --size a3 --margins 2cm
```

### Content Control
```bash
# Exclude code cells (report mode)
$ python jamboree_converter.py notebook.ipynb --size a3 --no-input

# Exclude input/output prompts
$ python jamboree_converter.py notebook.ipynb --size a3 --no-prompt

# Both (cleanest output)
$ python jamboree_converter.py notebook.ipynb --size a3 --no-input --no-prompt
```

### Custom Output Names
```bash
# Custom filename
$ python jamboree_converter.py notebook.ipynb --size a3 --output final_report

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
$ python jamboree_converter.py large_notebook.ipynb --size a3 --method latex
```

**LaTeX errors:**
```bash
# Use WebPDF method instead
$ python jamboree_converter.py notebook.ipynb --size a3 --method webpdf
```

**Content too small:**
```bash
# Reduce margins for more content space
$ python jamboree_converter.py notebook.ipynb --size a3 --margins 15mm
```

## 📄 File Organization

The converter automatically creates descriptive filenames:

```
notebook.ipynb → notebook_webpdf_a3_portrait.pdf
notebook.ipynb → notebook_latex_a2_landscape.pdf
notebook.ipynb → custom_name.pdf (with --output)
```
