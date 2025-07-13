import os
from docx import Document

def extract_text_from_docx(path):
    doc = Document(path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

resumes_folder = "resumes/"
resume_texts = {}

for filename in os.listdir(resumes_folder):
    if filename.endswith(".docx"):
        path = os.path.join(resumes_folder, filename)
        text = extract_text_from_docx(path)
        resume_texts[filename] = text

# Print preview of one resume
for filename, content in resume_texts.items():
    print(f"--- {filename} ---\n{content[:500]}...\n")
    break  # Just preview the first one
