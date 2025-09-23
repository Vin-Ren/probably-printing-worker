#!/usr/bin/env python3
import os
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter
from weasyprint import HTML, CSS
from datetime import datetime
import random

import json

default_quotes = []
with open("default_quotes.json", "r") as f:
    default_quotes = json.load(f)


def cpp_to_pdf(file_path, teamname, output_pdf=None, css_string=None, quotes=[], job_context={}):
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

    if quotes:
        quotes = json.loads(quotes)
    else:
        quotes = default_quotes
    quote = random.choice(quotes) if quotes else {"quote": "", "author": ""}
    context = {
        "teamname": teamname, 
        "filename": filename, 
        "datetime": dt, 
        "quote": quote["quote"], 
        "quote_author": quote["author"], 
        **{"jobctx_"+k: v for k, v in job_context.items()}
    }
    
    if not css_string:
        with open("default_template.css", "r") as f:
            css_string = f.read()
    
    # Convert HTML to PDF with headers/footers
    HTML(string=highlighted_html).write_pdf(
        output_pdf,
        stylesheets=[CSS(string=css_string % context)]
    )
