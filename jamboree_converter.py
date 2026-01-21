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
import re
import warnings
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
        import json
        
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
        
        # Read notebook to extract Plotly data
        print("📖 Reading notebook and extracting Plotly charts...")
        with open(notebook_file, 'r') as f:
            notebook = json.load(f)
        
        # Extract all Plotly outputs and inject deterministic placeholders so charts render in-place.
        plotly_charts = []
        plotly_index = 0
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code':
                for output in cell.get('outputs', []):
                    if 'data' in output and 'application/vnd.plotly.v1+json' in output['data']:
                        plotly_charts.append(output['data']['application/vnd.plotly.v1+json'])
                        placeholder_id = f"jamboree-plotly-{plotly_index}"  # deterministic ordering
                        plotly_index += 1

                        if 'data' not in output:
                            output['data'] = {}
                        output['data']['text/html'] = f'<div id="{placeholder_id}" class="jamboree-plotly-placeholder"></div>'
        
        print(f"📊 Found {len(plotly_charts)} Plotly chart(s) in notebook")
        
        # First convert to HTML - no custom template needed
        config = Config()
        
        # Use the classic template which handles outputs better
        config.HTMLExporter.template_name = 'classic'
        
        exporter = HTMLExporter(config=config)
        
        if kwargs.get('no_input', False):
            exporter.exclude_input = True
        if kwargs.get('no_prompt', False):
            exporter.exclude_input_prompt = True
            exporter.exclude_output_prompt = True
        
        print("🔄 Converting to HTML...")
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=r"Your element with mimetype\(s\) dict_keys\(\['application/vnd\.plotly\.v1\+json'\]\) is not able to be represented\.",
                category=UserWarning,
            )
            # Convert from a temporary notebook file so we don't mutate the source file.
            temp_notebook_file = None
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as nf:
                json.dump(notebook, nf)
                temp_notebook_file = nf.name

            try:
                (html_body, resources) = exporter.from_filename(temp_notebook_file)
            finally:
                try:
                    if temp_notebook_file:
                        os.unlink(temp_notebook_file)
                except Exception:
                    pass

        has_math = bool(re.search(r"\\\(|\\\[|\$\$|\\begin\{", html_body))
        
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
        /* Preserve math rendering */
        .MathJax, .MathJax_Display, mjx-container {{
            overflow-x: auto;
            overflow-y: visible;
        }}
        </style>
        """
        
        # Embed Plotly charts data and library
        plotly_data_json = json.dumps(plotly_charts)

        plotly_src = None
        try:
            import plotly  # type: ignore
            candidate = Path(plotly.__file__).parent / 'package_data' / 'plotly.min.js'
            if candidate.exists():
                plotly_src = candidate.as_uri()
        except ModuleNotFoundError:
            plotly_src = None

        # Optional offline MathJax: point this env var to MathJax's tex-mml-chtml.js
        # Example:
        #   export JAMBOREE_MATHJAX_JS=/absolute/path/to/mathjax/es5/tex-mml-chtml.js
        mathjax_src = None
        env_mathjax = os.environ.get('JAMBOREE_MATHJAX_JS')
        if env_mathjax:
            p = Path(env_mathjax).expanduser()
            if p.exists():
                mathjax_src = p.as_uri()
        plotly_script = """
        __PLOTLY_SCRIPT_TAG__
        <script>
        // Embedded Plotly chart data
        var plotlyChartsData = __PLOTLY_DATA_JSON__;
        window.plotlyRenderingComplete = false;
        window.plotlyRenderedCount = 0;
        window.plotlyRenderStarted = false;
        window.plotlyRenderFailed = false;
        window.plotlyLastError = null;
        window.plotlyLoadStartTime = Date.now();

        function markPlotlyComplete() {
            window.plotlyRenderingComplete = true;
        }

        function renderPlotlyCharts() {
            if (window.plotlyRenderStarted) return;

            if (plotlyChartsData.length === 0) {
                markPlotlyComplete();
                return;
            }

            if (typeof Plotly === 'undefined') {
                if ((Date.now() - window.plotlyLoadStartTime) > 60000) {
                    console.warn('Plotly did not load within 60s; skipping chart rendering');
                    window.plotlyRenderFailed = true;
                    markPlotlyComplete();
                    return;
                }
                // Plotly might still be loading (CDN slow/blocked). Retry for a while.
                setTimeout(renderPlotlyCharts, 250);
                return;
            }

            window.plotlyRenderStarted = true;
            console.log('Found ' + plotlyChartsData.length + ' Plotly charts to render');

            // Prefer deterministic in-place placeholders injected into the notebook outputs.
            var candidates = Array.from(document.querySelectorAll('.jamboree-plotly-placeholder'));

            // If nbconvert didn't include any recognizable placeholders, render at the end
            if (candidates.length === 0) {
                console.warn('No Plotly placeholders detected in HTML; rendering charts at end of document');
                var container = document.createElement('div');
                container.id = 'plotly-fallback-container';
                document.body.appendChild(container);
                candidates = [container];
            }

            var chartIndex = 0;

            function renderInto(targetArea, chartData) {
                var div = document.createElement('div');
                div.className = 'plotly-graph-div';
                div.style.width = '100%';
                div.style.height = '500px';
                div.style.marginBottom = '20px';

                // Replace placeholder contents with the chart div
                targetArea.innerHTML = '';
                targetArea.appendChild(div);

                return Plotly.newPlot(div, chartData.data, chartData.layout, {
                    responsive: true,
                    displayModeBar: false
                });
            }

            // Render charts into detected candidates first, then append remaining to end
            for (var i = 0; i < candidates.length && chartIndex < plotlyChartsData.length; i++) {
                (function(area, data) {
                    try {
                        console.log('Rendering chart ' + (chartIndex + 1));
                        renderInto(area, data).then(function() {
                            window.plotlyRenderedCount++;
                            if (window.plotlyRenderedCount >= plotlyChartsData.length) {
                                console.log('All Plotly charts rendering complete!');
                                markPlotlyComplete();
                            }
                        }).catch(function(e) {
                            console.error('Failed to render chart:', e);
                            window.plotlyLastError = String(e);
                            window.plotlyRenderedCount++;
                            if (window.plotlyRenderedCount >= plotlyChartsData.length) markPlotlyComplete();
                        });
                    } catch (e) {
                        console.error('Failed to render chart:', e);
                        window.plotlyLastError = String(e);
                        window.plotlyRenderedCount++;
                        if (window.plotlyRenderedCount >= plotlyChartsData.length) markPlotlyComplete();
                    }
                })(candidates[i], plotlyChartsData[chartIndex]);
                chartIndex++;
            }

            if (chartIndex < plotlyChartsData.length) {
                var fallbackContainer = document.getElementById('plotly-fallback-container');
                if (!fallbackContainer) {
                    fallbackContainer = document.createElement('div');
                    fallbackContainer.id = 'plotly-fallback-container';
                    document.body.appendChild(fallbackContainer);
                }

                for (; chartIndex < plotlyChartsData.length; chartIndex++) {
                    (function(data) {
                        try {
                            var holder = document.createElement('div');
                            fallbackContainer.appendChild(holder);
                            renderInto(holder, data).then(function() {
                                window.plotlyRenderedCount++;
                                if (window.plotlyRenderedCount >= plotlyChartsData.length) markPlotlyComplete();
                            }).catch(function(e) {
                                console.error('Failed to render chart (fallback):', e);
                                window.plotlyLastError = String(e);
                                window.plotlyRenderedCount++;
                                if (window.plotlyRenderedCount >= plotlyChartsData.length) markPlotlyComplete();
                            });
                        } catch (e) {
                            console.error('Failed to render chart (fallback):', e);
                            window.plotlyLastError = String(e);
                            window.plotlyRenderedCount++;
                            if (window.plotlyRenderedCount >= plotlyChartsData.length) markPlotlyComplete();
                        }
                    })(plotlyChartsData[chartIndex]);
                }
            }

            // Fallback: mark complete after timeout even if promises don't resolve
            setTimeout(function() {
                if (!window.plotlyRenderingComplete) {
                    console.warn('Plotly rendering timeout fallback triggered');
                    window.plotlyRenderFailed = true;
                    markPlotlyComplete();
                }
            }, 120000);
        }
        
        // Start rendering after DOM is ready; actual chart rendering waits until Plotly exists.
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            renderPlotlyCharts();
        } else {
            document.addEventListener('DOMContentLoaded', renderPlotlyCharts);
        }
        </script>
        """.replace('__PLOTLY_DATA_JSON__', plotly_data_json)

        plotly_script_tag = ''
        if plotly_src:
            plotly_script_tag = f'<script src="{plotly_src}" charset="utf-8"></script>'
        else:
            # Last resort: CDN (may be blocked in some environments)
            plotly_script_tag = '<script src="https://cdn.plot.ly/plotly-2.32.0.min.js" charset="utf-8"></script>'

        plotly_script = plotly_script.replace('__PLOTLY_SCRIPT_TAG__', plotly_script_tag)

        if has_math:
            if mathjax_src:
                mathjax_tag = f'<script src="{mathjax_src}"></script>'
            else:
                # Last resort: CDN (may be blocked in some environments)
                mathjax_tag = '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'

            plotly_script = plotly_script.replace(
                '</script>',
                '</script>\n        ' + mathjax_tag
            )
        
        # Inject CSS and Plotly script into HTML
        html_with_css = html_body.replace('</head>', page_css + plotly_script + '</head>')

        debug_html = None
        if os.environ.get('JAMBOREE_DEBUG_HTML') == '1':
            debug_html = Path(notebook_file).stem + '_debug.html'
            with open(debug_html, 'w') as f:
                f.write(html_with_css)
            print(f"📝 Debug HTML saved: {debug_html}")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_with_css)
            html_file = f.name

        try:
            if output_file is None:
                base = Path(notebook_file).stem
                size_suffix = f"_{page_size}_{orientation}" if page_size != 'a4' or orientation != 'portrait' else ""
                output_file = f"{base}_playwright{size_suffix}.pdf"
            else:
                output_file = output_file + '.pdf'

            print("🎭 Converting HTML to PDF with Playwright...")

            with sync_playwright() as p:
                browser = None
                page = None
                try:
                    browser = p.chromium.launch()
                    page = browser.new_page()

                    # Avoid networkidle hangs when CDNs are blocked; rely on local assets where possible.
                    page.goto(f"file://{html_file}", wait_until="load")
                    try:
                        page.wait_for_load_state("networkidle", timeout=5000)
                    except Exception:
                        pass

                    if len(plotly_charts) > 0:
                        print(f"⏳ Waiting for {len(plotly_charts)} Plotly chart(s) to render...")
                        try:
                            page.wait_for_function("typeof Plotly !== 'undefined'", timeout=60000)
                            page.wait_for_function("window.plotlyRenderingComplete === true", timeout=180000)
                            page.wait_for_timeout(500)
                            print(f"✓ All {len(plotly_charts)} Plotly charts rendered")
                        except Exception as e:
                            print(f"⚠️  Plotly rendering timeout: {e}")
                            print("    Continuing anyway - some charts may be missing")
                    else:
                        print("ℹ️  No Plotly charts found in this notebook")

                    if has_math:
                        print("⏳ Waiting for MathJax to render formulas...")
                        try:
                            page.wait_for_function(
                                "typeof MathJax !== 'undefined' && MathJax.typesetPromise !== undefined",
                                timeout=40000,
                            )
                            page.evaluate("() => MathJax.typesetPromise()")
                            page.wait_for_timeout(500)
                            print("✓ MathJax rendering complete")
                        except Exception as e:
                            print(f"⚠️  MathJax wait skipped (CDN blocked/slow?): {e}")
                    else:
                        print("ℹ️  No MathJax/TeX detected; skipping MathJax wait")

                    page.wait_for_timeout(500)
                    page.pdf(
                        path=output_file,
                        format=None,
                        width=f"{width}mm",
                        height=f"{height}mm",
                        margin={
                            "top": margins,
                            "right": margins,
                            "bottom": margins,
                            "left": margins,
                        },
                        print_background=True,
                    )

                finally:
                    try:
                        if page is not None:
                            page.close()
                    except Exception:
                        pass
                    try:
                        if browser is not None:
                            browser.close()
                    except Exception:
                        pass

            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ Created: {output_file} ({file_size:.1f} MB)")
            return True

        finally:
            try:
                os.unlink(html_file)
            except Exception:
                pass
            try:
                if debug_html:
                    os.unlink(debug_html)
            except Exception:
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

