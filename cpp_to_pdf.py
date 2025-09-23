#!/usr/bin/env python3
import os
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter
from weasyprint import HTML, CSS
from datetime import datetime
import random

import json

quotes = []
with open("quotes.json", "r") as f:
    quotes = json.load(f)


def cpp_to_pdf(file_path, teamname, output_pdf=None, css_string=None, job_context={}):
    filename = os.path.basename(file_path)
    output_pdf = output_pdf or filename.rsplit(".", 1)[0] + ".pdf"
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Detect language from filename
    try:
        lexer = get_lexer_for_filename(file_path)
    except Exception:
        lexer = TextLexer()

    with open(file_path, "r") as f:
        code = f.read()

    # Syntax highlight with line numbers
    formatter = HtmlFormatter(
        full=True,
        linenos="inline",
        style="bw",
        cssclass="codehilite"
    )
    highlighted_html = highlight(code, lexer, formatter)

    quote = random.choice(quotes) if quotes else {"quote": "", "author": ""}
    context = {
        "teamname": teamname, 
        "filename": filename, 
        "datetime": dt, 
        "quote": quote["quote"], 
        "quote_author": quote["author"], 
        **{"jobctx_"+k: v for k, v in job_context.items()}
    }
    
    # Convert HTML to PDF with headers/footers
    HTML(string=highlighted_html).write_pdf(
        output_pdf,
        stylesheets=[CSS(
            string=(
                css_string % context) if css_string 
                else f"""
                @page {{
                    size: A4;
                    margin: 2cm;
                    @top-left {{ content: "%(teamname)s - %(filename)s"; color: gray; font-size: 8pt; }}
                    @top-right {{ content: "%(datetime)s"; color: gray; font-size: 8pt; }}
                    @bottom-left {{ content: "%(quote)s — %(quote_author)s"; color: gray; font-size: 6pt; font-style: italic;  }}
                    @bottom-right {{ content: "Page " counter(page) " of " counter(pages); color: gray; font-size: 8pt; }}
                }}
                body {{ 
                    font-family: monospace;
                    font-size: 9pt; 
                }}
                .lineno {{ 
                    color: #888; 
                    padding-right: 2em;
                    padding-left: -2em;
                }}
                pre, code {{
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    overflow-wrap: anywhere;
                }}
            """ % context)]
    )
