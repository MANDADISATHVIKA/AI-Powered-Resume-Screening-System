from flask import Flask, render_template, request
import joblib
import os
from docx import Document
from pdfminer.high_level import extract_text as extract_pdf_text  # <- new PDF reader

app = Flask(__name__)

# Load model and vectorizer
model = joblib.load('resume_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Extract text from DOCX
def extract_text_from_docx(path):
    doc = Document(path)
    return '\n'.join(para.text for para in doc.paragraphs)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'resume' not in request.files:
        return "No file part"

    file = request.files['resume']
    if file.filename == '':
        return "No selected file"

    filename = file.filename.lower()
    filepath = os.path.join('uploaded_resume.' + filename.split('.')[-1])
    file.save(filepath)

    # Check extension and extract
    if filename.endswith('.docx'):
        text = extract_text_from_docx(filepath)
    elif filename.endswith('.pdf'):
        text = extract_pdf_text(filepath)  # <- pdfminer
    else:
        return "Unsupported file type. Please upload .docx or .pdf"

    # Predict
    X_input = vectorizer.transform([text])
    prediction = model.predict(X_input)[0]
    result = "Hired ✅" if prediction == 1 else "Not Hired ❌"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
