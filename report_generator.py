from flask import render_template
from weasyprint import HTML
import tempfile
import os

def generate_pdf(skills, jobs):
    html_content = render_template('report_template.html', skills=skills, jobs=jobs)

    # Create a temporary file for the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        HTML(string=html_content).write_pdf(tmp_file.name)
        return tmp_file.name
