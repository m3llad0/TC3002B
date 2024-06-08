from flask_cors import CORS
from app import app
from flask import request, jsonify
from app.model.plagarsimDetector import PlagiarismDetector

CORS(app)

@app.route("/plagarsim", methods=["POST"])
def plagarsim():
    try:
        data = request.get_json()

        user_text = data['text']

        detector = PlagiarismDetector()

        detector.set_user_input(user_text)

        results = detector.get_results()

        if results:
            return jsonify({"plgarised_text": True, "results": results}), 200
        else:
            return jsonify({"plgarised_text": False, "results": "No hay plagio"} ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
