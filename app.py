# === app.py ===
from flask import Flask, render_template, request
import os
from docx import Document
from pdfminer.high_level import extract_text as extract_pdf_text

app = Flask(__name__)

# === Helper functions ===
def extract_text_from_docx(path):
    doc = Document(path)
    return '\n'.join(para.text for para in doc.paragraphs)

def is_hired_by_rules(text, keywords_list, min_match=0.75):
    """
    Returns True if at least `min_match` percent of keywords are found.
    Example: 0.75 = 75% of required keywords must match
    """
    text_lower = text.lower()
    matched = 0

    for keyword in keywords_list:
        if keyword.strip().lower() in text_lower:
            matched += 1

    match_ratio = matched / len(keywords_list)
    return match_ratio >= min_match

# === Flask Routes ===
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'resume' not in request.files or 'keywords' not in request.form:
        return "Missing resume or keywords."

    file = request.files['resume']
    keywords = request.form['keywords'].strip()
    if file.filename == '' or keywords == '':
        return "Please upload a file and enter required keywords."

    filename = file.filename.lower()
    file_ext = filename.split('.')[-1]
    filepath = f'uploaded_resume.{file_ext}'
    file.save(filepath)

    # Extract text
    if filename.endswith('.docx'):
        text = extract_text_from_docx(filepath)
    elif filename.endswith('.pdf'):
        text = extract_pdf_text(filepath)
    else:
        return "Unsupported file type. Only .pdf or .docx allowed."

    # Rule-based prediction with threshold
    required_keywords = keywords.split(',')
    prediction = is_hired_by_rules(text, required_keywords, min_match=0.75)
    result = "Hired " if prediction else "Not Hired "

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)