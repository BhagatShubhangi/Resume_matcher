from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from resume_parser import extract_skills, match_jobs

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    user_skills = extract_skills(filepath)
    job_matches = match_jobs(user_skills)

    return render_template('result.html', skills=user_skills, jobs=job_matches)

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, send_file
from report_generator import generate_pdf
import json

@app.route('/download_report', methods=['POST'])
def download_report():
    skills = request.form['skills'].split(',')
    jobs = json.loads(request.form['jobs'])
    pdf_path = generate_pdf(skills, jobs)
    return send_file(pdf_path, as_attachment=True)

