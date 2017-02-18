# Copyright Douglas Gastonguay-Goddard 2017

import os
import sys
import json
from datetime import datetime as dt
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.pygments2xpre import pygments2xpre as p2x
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, XPreformatted

def add_heading(heading, paragraphs):
    for line in heading:
        if line == '[DATE]':
            line = dt.now().strftime('%B %d, %Y')
        paragraphs.append(Paragraph(line, style=styles['heading']))

def add_description(fname, paragraphs):
    paragraphs.append(Paragraph('Description', style=styles['title']))
    with open(fname) as description_file:
        contents = description_file.read()
        for paragraph in contents.split('\n'):
            if paragraph == '':
                continue
            paragraphs.append(Paragraph(paragraph, style=styles['paragraph']))

def init_styles():
    global styles
    styles = {}

    heading_style = ParagraphStyle('heading')
    heading_style.alignment = 2 # right
    styles['heading'] = heading_style

    paragraph_style = ParagraphStyle('paragraph')
    paragraph_style.spaceBefore = 0.1*inch
    paragraph_style.leftIndent = 0.5*inch
    styles['paragraph'] = paragraph_style

    code_style = getSampleStyleSheet()["Code"]
    styles['code'] = code_style

    title_style = getSampleStyleSheet()["Title"]
    title_style.alignment = 0   # left
    title_style.spaceBefore = 0.5*inch
    styles['title'] = title_style

    markdown_style = ParagraphStyle('markdown')
    markdown_style.spaceBefore = 0.1*inch
    markdown_style.leftIndent = 0.5*inch
    markdown_style.fontName = 'Courier'
    markdown_style.fontSize = 8
    styles['markdown'] = markdown_style

def add_markdown(fname, paragraphs):
    with open(fname) as md_file:
        contents = md_file.read()

        for paragraph in contents.split('\n'):
            if paragraph == '':
                continue
            paragraphs.append(Paragraph(paragraph, style=styles['markdown']))

def add_file(fname, paragraphs):
    extensions = {
        'py': 'python',
        'ml': 'ocaml',
        'mll': 'ocaml',
        'mly': 'ocaml',
        'c': 'c',
        'h': 'c++',
        'cpp': 'c++',
        'cc': 'c++',
        'll': 'llvm',
        'java': 'java',
    }

    paragraphs.append(Paragraph(fname, style=styles['title']))
    with open(fname) as source_file:
        language = 'python'
        if '.' in fname:
            ext = fname.split('.')[-1]
            if ext == 'md':
                add_markdown(fname, paragraphs)
                return
            if ext in extensions:
                language = extensions[ext]

        source = source_file.read()
        pretty = p2x(source, language=language)
        formatted = XPreformatted(pretty, style=styles['code'])
        paragraphs.append(formatted)

def main():
    paragraph_style = ParagraphStyle({})
    paragraphs = []
    init_styles()

    config_file = 'config.json'
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        config_file = sys.argv[1]

    doc = SimpleDocTemplate(
            "out.pdf",
            # pagesize=landscape(letter),
            rightMargin=0.1*inch,
            leftMargin=0.1*inch,
            topMargin=0.25*inch,
            bottomMargin=0.25*inch)

    with open(config_file) as cfg:
        contents = cfg.read()
        config = json.loads(contents)

    add_heading(config['heading'], paragraphs)
    add_description(config['description_file'], paragraphs)

    for fname in config['files']:
        add_file(fname, paragraphs)

    doc.build(paragraphs)

if __name__ == '__main__':
    main()