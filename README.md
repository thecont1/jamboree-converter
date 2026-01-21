## Jamboree Converter

Here's why you're here: You have a a lengthy Jupyter Notebook (`.ipynb` file) that you want to turn into a visually pleasing (or at least bearable) PDF document. And you're looking for a fuss-free tool that will get the job done.

In goes your notebook into `jamboree_converter.py` and out comes a PDF in a special size of A2 width and A0 height. Check out the included sample.

### Requirements

- Python 3.13+
- `uv`
- Playwright’s Chromium browser

### Installation

1. Clone this repo

```bash
git clone https://github.com/thecont1/jamboree-converter.git
```

2. Create the environment and install dependencies 

Install `uv`, if you haven't already, by following the official instructions at [docs.astral.sh/uv](https://docs.astral.sh/uv/). Then, from the repo root:

```bash
uv sync
```

3. Install Playwright’s Chromium

```bash
uv run playwright install chromium
```

### Quick start

Convert a notebook to an A4 PDF:

```bash
uv run python jamboree_converter.py /path/to/notebook.ipynb
```

Convert to the long-form `case_study` paper size:

```bash
uv run python jamboree_converter.py /path/to/notebook.ipynb --size case_study
```

Hide code and prompts for a report-style PDF:

```bash
uv run python jamboree_converter.py /path/to/notebook.ipynb --size case_study --no-code --no-prompts
```

The PDF in `example1/` was generated using:

```bash
uv run python jamboree_converter.py example1/RecSys.ipynb --size case_study --no-code --no-prompts
```

### Common options

- **`--size`**
  Choose a paper size preset.

- **`--orientation`**
  `portrait` or `landscape`.

- **`--margins`**
  CSS margin value like `20mm` (default), `15mm`, `1in`.

- **`--output` / `-o`**
  Output filename without extension. The program appends `.pdf`.

- **`--no-code`**
  Hides code cells.

- **`--no-prompts`**
  Hides `In [1]` / `Out [1]` prompts.

### Available page sizes

These are defined in `jamboree_converter.py`:

- `a0`, `a1`, `a2`, `a3`, `a4`, `a5`
- `letter`, `legal`, `tabloid`, `ledger`
- `case_study` (420×1189mm)

You can list them from the CLI:

```bash
uv run python jamboree_converter.py --list-sizes
```

### Plotly notes (offline-friendly)

This project installs the Python `plotly` package and loads Plotly JS from the environment (offline).

If your PDF is missing Plotly charts:

- Make sure you ran `uv sync`.
- Re-run with `JAMBOREE_DEBUG_HTML=1` to keep the intermediate HTML for inspection.

### Troubleshooting

#### The program hangs after generating a PDF

This usually indicates the browser didn’t close or a network wait never finished.
The current version avoids `networkidle` hangs and closes page/browser in `finally` blocks.

#### The PDF is missing math

This tool does not run MathJax.
If math is important, ensure the notebook output renders it correctly before conversion.

#### Debugging output HTML

```bash
JAMBOREE_DEBUG_HTML=1 uv run python jamboree_converter.py your.ipynb --size case_study
```

### Help

Run:

```bash
uv run python jamboree_converter.py -h
```

It shows the full list of options and examples.
