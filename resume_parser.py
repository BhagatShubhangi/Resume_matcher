import fitz  # PyMuPDF
import nltk
import json
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt')

# Basic skill keywords
SKILL_KEYWORDS = [
    'python', 'java', 'c++', 'html', 'css', 'javascript',
    'sql', 'react', 'flask', 'django', 'excel', 'data analysis',
    'machine learning', 'deep learning', 'nlp', 'git'
]

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

def extract_skills(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    extracted = [skill for skill in SKILL_KEYWORDS if skill in text]
    return list(set(extracted))

def match_jobs(user_skills):
    with open('job_data.json') as f:
        jobs = json.load(f)

    results = []
    for job in jobs:
        required = job['skills']
        matched = list(set(user_skills) & set(required))
        missing = list(set(required) - set(user_skills))
        match_percent = int((len(matched) / len(required)) * 100)
        results.append({
            'title': job['title'],
            'match': match_percent,
            'matched': matched,
            'missing': missing
        })

    results.sort(key=lambda x: -x['match'])  # highest match first
    return results
