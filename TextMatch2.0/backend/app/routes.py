from flask_cors import CORS
from app import app
from flask import request, jsonify

CORS(app)

@app.route("/plagarsim", methods=["POST"])
def plagarsim():
    try:
        data = request.get_json()

        print(data['text'])

        # Logic to check for plagarsim

        return jsonify({"message": "Hello World"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500