import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
from ocr_helper import extract_text_from_image
from gemini_helper import generate_answers
from document_generator import create_document

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'heic', 'heif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        subject = request.form.get('subject', '')
        text_input = request.form.get('text_input', '')
        question_format = request.form.get('question_format', 'short_answer')

        extracted_texts = []
        if text_input:
            extracted_texts.append(text_input)

        # Handle multiple file uploads
        if 'files[]' in request.files:
            files = request.files.getlist('files[]')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)

                    try:
                        # Extract text from image
                        extracted_text = extract_text_from_image(filepath)
                        if extracted_text:
                            extracted_texts.append(extracted_text)
                    except Exception as e:
                        logger.error(f"Error processing file {filename}: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(filepath):
                            os.remove(filepath)

        if not extracted_texts:
            logger.error("No text input provided")
            return jsonify({'error': 'No text provided'}), 400

        # Combine all extracted texts
        combined_text = "\n\n".join(extracted_texts)
        logger.info(f"Processing request for subject: {subject}, format: {question_format}")

        # Generate answers using Gemini
        answers = generate_answers(subject, combined_text, question_format)

        if not answers:
            logger.error("No answers generated")
            return jsonify({'error': 'Failed to generate answers'}), 500

        # Create document
        doc_path = create_document(subject, combined_text, answers)

        return send_file(
            doc_path,
            as_attachment=True,
            download_name=f"{subject}_answers.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)