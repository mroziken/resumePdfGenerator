import os
import json
from datetime import datetime
from flask import Request, jsonify
from jinja2 import Environment, FileSystemLoader, select_autoescape
from google.cloud import storage
from weasyprint import HTML

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

BUCKET_NAME = os.getenv('BUCKET_NAME')


def generate_resume_pdf(request: Request):
    """HTTP Cloud Function to generate resume PDF and store in GCS."""
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'}), 405

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid JSON'}), 400

    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    template_name = data.get('template', 'modern') + '.html'
    if not os.path.exists(os.path.join(TEMPLATES_DIR, template_name)):
        return jsonify({'error': f'Template {template_name} not found'}), 400

    context = {
        'name': data.get('name', ''),
        'email': data.get('email', ''),
        'phone': data.get('phone', ''),
        'summary': data.get('summary', ''),
        'experience': data.get('experience', []),
        'education': data.get('education', []),
        'skills': data.get('skills', []),
    }

    template = env.get_template(template_name)
    html_content = template.render(**context)

    pdf = HTML(string=html_content).write_pdf()

    bucket_name = BUCKET_NAME
    if not bucket_name:
        return jsonify({'error': 'BUCKET_NAME environment variable not set'}), 500

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    filename = f"resume_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    blob = bucket.blob(filename)
    blob.upload_from_string(pdf, content_type='application/pdf')
    blob.make_public()

    return jsonify({'url': blob.public_url})
