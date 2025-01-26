from flask import Flask, request, jsonify
from flask_cors import CORS
from codecarbon import EmissionsTracker
import os
import subprocess
import tempfile
import sys
import google.generativeai as genai
import re

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure Gemini API Key
GOOGLE_API_KEY = 'AIzaSyDE4LGtQ2B0fw2F5oO9aiNNM-AvsTgYc7Q'
genai.configure(api_key=GOOGLE_API_KEY)
model_id = genai.GenerativeModel("gemini-1.5-flash")

# Regex to extract import statements
IMPORT_PATTERN = re.compile(r'^\s*(?:import (\w+)|from (\w+))')

STANDARD_LIBRARIES = set(sys.stdlib_module_names)

def extract_dependencies(filepath):
    """
    Extract third-party dependencies from the Python file.
    """
    with open(filepath, 'r') as file:
        code = file.readlines()
    
    dependencies = set()
    for line in code:
        match = IMPORT_PATTERN.match(line)
        if match:
            module = match.group(1) or match.group(2)
            if module and module not in STANDARD_LIBRARIES:
                dependencies.add(module)
    
    return list(dependencies)

def analyze_script_with_gemini(script_content):
    """
    Analyze Python script content using Gemini.
    """
    prompt = """
    Here is the Python script. Please process it and return the entire script 
    
    {script_content}
    """.format(script_content=script_content)

    response = model_id.generate_content(prompt)
    return response.text.strip()

@app.route('/upload', methods=['POST'])
def upload_script():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = file.filename
    if not filename.endswith('.py'):
        return jsonify({"error": "Only Python (.py) files are allowed"}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)

        # Return the script content for the frontend to display
        with open(filepath, 'r') as f:
            script_content = f.read()

        return jsonify({
            "filename": filename,
            "script_content": script_content  # Return raw Python script content
        })

@app.route('/analyze', methods=['POST'])
def analyze_script():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = file.filename
    if not filename.endswith('.py'):
        return jsonify({"error": "Only Python (.py) files are allowed"}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)

        # Read the Python file content
        with open(filepath, 'r') as f:
            script_content = f.read()

        # Use Gemini to process the entire script and extract insights
        extracted_content = analyze_script_with_gemini(script_content)

        # Create virtual environment
        venv_path = os.path.join(temp_dir, "venv")
        subprocess.run(["python", "-m", "venv", venv_path], check=True)

        # Determine paths for pip and python
        pip_path = os.path.join(venv_path, "Scripts", "pip") if os.name == "nt" else os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python") if os.name == "nt" else os.path.join(venv_path, "bin", "python")

        # Install dependencies
        dependencies = extract_dependencies(filepath)
        if dependencies:
            try:
                subprocess.run([pip_path, "install"] + dependencies, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                return jsonify({"error": f"Failed to install dependencies: {e.stderr.decode()}"}), 500

        # Measure emissions and execute the script
        tracker = EmissionsTracker()
        tracker.start()

        try:
            subprocess.run([python_path, filepath], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            tracker.stop()
            return jsonify({"error": f"Script execution failed: {e.stderr.decode()}"}), 500

        emissions = tracker.stop()

        return jsonify({
            "filename": filename,
            "script_content": script_content,  # The raw Python script content
            "extracted_content": extracted_content,  # Full script with insights from Gemini
            "emissions": round(emissions, 4),  # in kg of CO2
            "message": "Script analyzed successfully."
        })

if __name__ == '__main__':
    app.run(debug=True)
