from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pdfplumber
import os
import tempfile
import uuid
from content_processor import ContentProcessor
from ppt_generator import PPTGenerator

app = Flask(__name__)
CORS(app)

# Initialize components
processor = ContentProcessor()
generator = PPTGenerator()

# Create uploads directory
os.makedirs('static/uploads', exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['pdf', 'txt']:
            return jsonify({'error': 'Invalid file type. Only PDF and TXT supported'}), 400
        
        temp_filename = f"{uuid.uuid4()}.{file_ext}"
        temp_path = os.path.join('static/uploads', temp_filename)
        file.save(temp_path)
        
        # Process file based on type
        text_content = ""
        if file_ext == 'pdf':
            with pdfplumber.open(temp_path) as pdf:
                text_content = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif file_ext == 'txt':
            with open(temp_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        
        # Clean up temporary file
        os.remove(temp_path)
        
        if not text_content.strip():
            return jsonify({'error': 'No text content found in file'}), 400
        
        # Process content
        slides_data = processor.create_slide_structure(text_content)
        
        # Create PowerPoint
        output_filename = f"presentation_{uuid.uuid4()}.pptx"
        output_path = os.path.join('static/uploads', output_filename)
        generator.create_presentation(slides_data, output_path)
        
        return jsonify({
            'success': True,
            'slides_count': len(slides_data),
            'download_path': f'/download/{output_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join('static/uploads', filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)