import os
import pandas as pd
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# === STEP 1: Extract text from DOCX resumes ===
def extract_text_from_docx(path):
    doc = Document(path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

resumes_folder = "."  # Use current directory for resume files
resume_texts = {}

for filename in os.listdir(resumes_folder):
    if filename.endswith(".docx"):
        path = os.path.join(resumes_folder, filename)
        text = extract_text_from_docx(path)
        resume_texts[filename] = text

# === STEP 2: Load labels from CSV ===
labels_df = pd.read_csv("labels.csv")
texts = []
labels = []

for _, row in labels_df.iterrows():
    filename = row['filename']
    label = 1 if row['label'].lower() == "hired" else 0
    if filename in resume_texts:
        texts.append(resume_texts[filename])
        labels.append(label)

# === STEP 3: TF-IDF Vectorization ===
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(texts)

print("Shape of feature matrix:", X.shape)
print("Sample feature names:", vectorizer.get_feature_names()[:10])  # Use get_feature_names for sklearn < 1.0

# === STEP 4: Train the Model ===
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# === STEP 5: Evaluate the Model ===
y_pred = model.predict(X_test)
print("\nModel Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# === STEP 6: Save the Model and Vectorizer ===
joblib.dump(model, 'resume_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("\nModel and vectorizer saved successfully!")
