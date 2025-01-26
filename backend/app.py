from flask import Flask, request, jsonify
from flask_cors import CORS
from codecarbon import EmissionsTracker
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/analyze', methods=['POST'])
def analyze_script():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    tracker = EmissionsTracker()
    tracker.start()
    
    # Simulate running the script (you can use `subprocess` for real execution)
    exec(open(filepath).read())
    
    emissions = tracker.stop()

    return jsonify({
        "filename": filename,
        "emissions": round(emissions, 4),  # in kg of CO2
        "message": "Script analyzed successfully."
    })

if __name__ == '__main__':
    app.run(debug=True)
