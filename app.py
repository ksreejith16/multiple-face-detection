from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/take-images', methods=['POST'])
def take_images():
    data = request.get_json()
    
    try:
        user_id = int(data["user_id"])
        username = str(data["username"]).strip()
        print(f"Received user ID: {user_id}, Username: {username}")
    except (KeyError, ValueError, TypeError):
        return jsonify(error="Invalid User ID or Username provided."), 400

    # Run the script and pass user_id and username as arguments
    result = subprocess.run(["python", "take_images.py", str(user_id), username], capture_output=True, text=True)
    
    if result.returncode == 0:
        return jsonify(message="Images taken successfully!"), 200
    else:
        print("Error:", result.stderr)
        return jsonify(error="Failed to take images.", details=result.stderr), 500

@app.route('/train-images', methods=['POST'])
def train_images():
    result = subprocess.run(["python", "training.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        return jsonify(message="Model training completed successfully!"), 200
    else:
        print("Error:", result.stderr)  # Debug print
        return jsonify(error="Failed to train model.", details=result.stderr), 500


@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    subprocess.run(["python", "recognize.py"])
    return "Attendance marked successfully!", 200

if __name__ == "__main__":
    app.run(port=5000)
