#!/usr/bin/env python
"""
Enhanced Notebook Printing Utility with Page Size Control

A script to convert Jupyter notebooks to various formats with custom page sizes.
Supports PDF (LaTeX), WebPDF, HTML, and Mercury dashboard generation.
"""

import os
import sys
import argparse
import tempfile
from pathlib import Path

import nbconvert
from nbconvert import WebPDFExporter, PDFExporter, HTMLExporter
from traitlets.config import Config

# Standard page sizes (width × height in mm)
PAGE_SIZES = {
    'a0': (841, 1189), 
    'a1': (594, 841), 
    'a2': (420, 594), 
    'a3': (297, 420), 
    'a4': (210, 297), 
    'a5': (148, 210),
    'letter': (216, 279), 
    'legal': (216, 356), 
    'tabloid': (279, 432), 
    'ledger': (432, 279), 
    'case_study': (420, 1189)
}

def create_custom_html_template(page_size, orientation, margins):
    """Create custom HTML template with proper @page CSS rules."""
    
    # Get dimensions
    if page_size.lower() in PAGE_SIZES:
        width, height = PAGE_SIZES[page_size.lower()]
        css_size = page_size.upper()
    else:
        width, height = PAGE_SIZES['a4']
        css_size = 'A4'
    
    # Swap for landscape
    if orientation.lower() == 'landscape':
        width, height = height, width
        css_orientation = 'landscape'
    else:
        css_orientation = 'portrait'
    
    # Create the HTML template with embedded CSS
    html_template = f'''
{{% extends "lab/index.html.j2" %}}

{{% block html_head_css %}}
{{{{ super() }}}}
<style>
/* Page size control */
@page {{
    size: {css_size} {css_orientation};
    margin: {margins};
}}

/* Alternative approach with explicit dimensions */
@page {{
    size: {width}mm {height}mm;
    margin: {margins};
}}

/* Print-specific styles */
@media print {{
    body {{
        margin: 0;
        padding: {margins};
        width: {width}mm;
        height: {height}mm;
        box-sizing: border-box;
    }}
    
    .jp-Notebook {{
        width: 100%;
        max-width: none;
        margin: 0;
        padding: 0;
    }}
    
    .jp-Cell {{
        page-break-inside: avoid;
        margin-bottom: 10pt;
    }}
    
    .jp-OutputArea-output {{
        page-break-inside: avoid;
    }}
}}

/* General styling */
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 11pt;
    line-height: 1.4;
    color: #333;
}}

.jp-Notebook {{
    background: white;
    padding: 0;
}}

.jp-Cell {{
    margin-bottom: 1em;
}}

/* Code styling */
.jp-CodeCell .jp-Cell-inputWrapper {{
    background: #f8f9fa;
    border-left: 4px solid #007acc;
    padding: 8pt;
    margin: 8pt 0;
}}

.jp-OutputArea {{
    background: white;
    border-left: 4px solid #28a745;
    padding: 8pt;
    margin: 8pt 0;
}}

/* Table styling */
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 6pt;
    text-align: left;
}}

th {{
    background-color: #f2f2f2;
    font-weight: bold;
}}

/* Image sizing */
img {{
    max-width: 100%;
    height: auto;
}}

/* Matplotlib figure sizing */
.jp-OutputArea-output img {{
    max-width: 100%;
    height: auto;
}}
</style>
{{% endblock html_head_css %}}
'''
    
    return html_template

def convert_with_working_pagesize(notebook_file, page_size='a4', orientation='portrait',
                                 margins='20mm', output_file=None, **kwargs):
    """Convert notebook with properly working page size control."""
    
    try:
        # Get dimensions
        if page_size.lower() in PAGE_SIZES:
            width, height = PAGE_SIZES[page_size.lower()]
        else:
            print(f"❌ Unknown page size: {page_size}")
            return False
        
        # Swap for landscape
        if orientation.lower() == 'landscape':
            width, height = height, width
        
        print(f"📄 Target: {page_size.upper()} {orientation} ({width}×{height}mm)")
        
        # Create temporary custom template
        template_content = create_custom_html_template(page_size, orientation, margins)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html.j2', delete=False) as f:
            f.write(template_content)
            template_file = f.name
        
        try:
            # Create configuration
            config = Config()
            config.WebPDFExporter.template_file = template_file
            
            # Create exporter
            exporter = WebPDFExporter(config=config)
            exporter.allow_chromium_download = True
            
            # Apply content options
            if kwargs.get('no_input', False):
                exporter.exclude_input = True
            if kwargs.get('no_prompt', False):
                exporter.exclude_input_prompt = True
                exporter.exclude_output_prompt = True
            
            # Generate filename
            if output_file is None:
                base = Path(notebook_file).stem
                size_suffix = f"_{page_size}_{orientation}" if page_size != 'a4' or orientation != 'portrait' else ""
                output_file = f"{base}_sized{size_suffix}.pdf"
            else:
                output_file = output_file + '.pdf'
            
            print(f"🔄 Converting with custom template...")
            
            # Convert
            (body, resources) = exporter.from_filename(notebook_file)
            
            # Write file
            with open(output_file, 'wb') as f:
                f.write(body)
            
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ Created: {output_file} ({file_size:.1f} MB)")
            
            return True
            
        finally:
            # Clean up template file
            try:
                os.unlink(template_file)
            except:
                pass
                
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def convert_with_playwright_direct(notebook_file, page_size='a4', orientation='portrait',
                                  margins='20mm', output_file=None, **kwargs):
    """Alternative method using Playwright directly for better page size control."""
    
    try:
        from playwright.sync_api import sync_playwright
        
        # Get dimensions
        if page_size.lower() in PAGE_SIZES:
            width, height = PAGE_SIZES[page_size.lower()]
        else:
            print(f"❌ Unknown page size: {page_size}")
            return False
        
        # Swap for landscape
        if orientation.lower() == 'landscape':
            width, height = height, width
        
        print(f"📄 Playwright: {page_size.upper()} {orientation} ({width}×{height}mm)")
        
        # First convert to HTML
        config = Config()
        exporter = HTMLExporter(config=config)
        
        if kwargs.get('no_input', False):
            exporter.exclude_input = True
        if kwargs.get('no_prompt', False):
            exporter.exclude_input_prompt = True
            exporter.exclude_output_prompt = True
        
        print("🔄 Converting to HTML...")
        (html_body, resources) = exporter.from_filename(notebook_file)
        
        # Add page size CSS to HTML
        page_css = f"""
        <style>
        @page {{
            size: {width}mm {height}mm;
            margin: {margins};
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            margin: 0;
            padding: {margins};
        }}
        .jp-Notebook {{
            max-width: none;
            width: 100%;
        }}
        </style>
        """
        
        # Inject CSS into HTML
        html_with_css = html_body.replace('</head>', page_css + '</head>')
        
        # Write temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_with_css)
            html_file = f.name
        
        try:
            # Generate filename
            if output_file is None:
                base = Path(notebook_file).stem
                size_suffix = f"_{page_size}_{orientation}" if page_size != 'a4' or orientation != 'portrait' else ""
                output_file = f"{base}_playwright{size_suffix}.pdf"
            else:
                output_file = output_file + '.pdf'
            
            print("🎭 Converting HTML to PDF with Playwright...")
            
            # Convert HTML to PDF with Playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Navigate to HTML file
                page.goto(f"file://{html_file}")
                
                # Generate PDF with specific page size
                page.pdf(
                    path=output_file,
                    format=None,  # Use custom size
                    width=f"{width}mm",
                    height=f"{height}mm",
                    margin={
                        "top": margins,
                        "right": margins,
                        "bottom": margins,
                        "left": margins
                    },
                    print_background=True
                )
                
                browser.close()
            
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ Created: {output_file} ({file_size:.1f} MB)")
            
            return True
            
        finally:
            # Clean up HTML file
            try:
                os.unlink(html_file)
            except:
                pass
                
    except ImportError:
        print("❌ Playwright not available. Install with: pip install playwright")
        return False
    except Exception as e:
        print(f"❌ Playwright conversion failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Working page size converter for Jupyter notebooks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Methods:
  template   - Custom HTML template with CSS (recommended)
  playwright - Direct Playwright control (most reliable)
  both       - Try both methods

Examples:
  python working_page_converter.py notebook.ipynb --size a3
  python working_page_converter.py notebook.ipynb --size a2 --orientation landscape
  python working_page_converter.py notebook.ipynb --size a1 --method playwright
        """
    )
    
    parser.add_argument('notebook', nargs='?', help='Input notebook file (.ipynb)')
    parser.add_argument('--size', '-s', choices=list(PAGE_SIZES.keys()), 
                       default='a4', help='Page size (default: a4)')
    parser.add_argument('--orientation', choices=['portrait', 'landscape'], 
                       default='portrait', help='Page orientation (default: portrait)')
    parser.add_argument('--method', choices=['template', 'playwright', 'both'], 
                       default='playwright', help='Conversion method (default: playwright)')
    parser.add_argument('--output', '-o', help='Output filename (without extension)')
    parser.add_argument('--margins', default='20mm', help='Page margins (default: 20mm)')
    parser.add_argument('--no-input', action='store_true', help='Exclude code cells')
    parser.add_argument('--no-prompt', action='store_true', help='Exclude prompts')
    parser.add_argument('--list-sizes', action='store_true', help='List available page sizes')
    
    args = parser.parse_args()
    
    if args.list_sizes:
        print("\n📐 Available page sizes:")
        print("=" * 50)
        for size, (w, h) in sorted(PAGE_SIZES.items()):
            print(f"{size.upper():8} - {w:3} × {h:3} mm")
        print("\n🔄 Orientations: portrait, landscape")
        print("🎨 Methods: template, playwright (recommended), both")
        return
    
    if not args.notebook:
        parser.error("notebook argument is required (unless using --list-sizes)")
    
    if not os.path.exists(args.notebook):
        print(f"❌ File not found: {args.notebook}")
        sys.exit(1)
    
    print(f"\n📄 Converting: {args.notebook}")
    print(f"📐 Page size: {args.size.upper()} {args.orientation}")
    print(f"🎨 Method: {args.method}")
    
    success = True
    
    # Convert using selected method(s)
    if args.method in ['template', 'both']:
        print("\n" + "="*50)
        print("📄 Template Method (Custom CSS)")
        print("="*50)
        result = convert_with_working_pagesize(
            args.notebook, args.size, args.orientation,
            args.margins, args.output,
            no_input=args.no_input, no_prompt=args.no_prompt
        )
        success = success and result
    
    if args.method in ['playwright', 'both']:
        print("\n" + "="*50)
        print("🎭 Playwright Method (Direct Control)")
        print("="*50)
        result = convert_with_playwright_direct(
            args.notebook, args.size, args.orientation,
            args.margins, args.output,
            no_input=args.no_input, no_prompt=args.no_prompt
        )
        success = success and result
    
    if success:
        print(f"\n✅ Conversion completed successfully!")
        if args.method == 'both':
            print("🔍 Compare both files - they should now have different page sizes!")
    else:
        print(f"\n❌ Conversion failed")
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

