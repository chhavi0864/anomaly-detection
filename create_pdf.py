from fpdf import FPDF
import json
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Network Anomaly Detection - Project Source Code', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=10)

files_to_print = [
    'app.py',
    'templates/index.html',
    'static/style.css',
    'static/script.js',
]

for file_path in files_to_print:
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"File: {file_path}", 0, 1)
    pdf.set_font("Courier", size=9)
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # FPDF 1.7 doesn't support full unicode natively, so we replace fancy quotes/chars
                content = content.encode('latin-1', 'replace').decode('latin-1')
                for line in content.split('\n'):
                    pdf.multi_cell(0, 5, line)
        else:
            pdf.cell(0, 10, "File not found.", 0, 1)
    except Exception as e:
        pdf.cell(0, 10, f"Error reading file: {e}", 0, 1)
    pdf.ln(10)

# Handle Jupyter Notebook specifically
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "File: training.ipynb (Python Code Extracts)", 0, 1)
pdf.set_font("Courier", size=9)
try:
    if os.path.exists('training.ipynb'):
        with open('training.ipynb', 'r', encoding='utf-8') as f:
            nb = json.load(f)
            for cell in nb.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = "".join(cell.get('source', []))
                    source = source.encode('latin-1', 'replace').decode('latin-1')
                    pdf.set_text_color(0, 100, 0) # Dark green for code blocks
                    pdf.multi_cell(0, 5, "# --- Jupyter Cell ---")
                    pdf.set_text_color(0, 0, 0)
                    for line in source.split('\n'):
                        pdf.multi_cell(0, 5, line)
                    pdf.ln(5)
    else:
        pdf.cell(0, 10, "Notebook not found.", 0, 1)
except Exception as e:
    pdf.cell(0, 10, f"Error reading notebook: {e}", 0, 1)

pdf.output("Project_Source_Code.pdf")
print("PDF created successfully!")
