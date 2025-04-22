from flask import request, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from app.services.pdf_reader import extract_text_from_pdf
from app.services.braille_converter import text_to_braille

def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads/pdf', filename)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    braille = text_to_braille(' '.join(text))

    return jsonify({'original_text': text, 'braille': braille})