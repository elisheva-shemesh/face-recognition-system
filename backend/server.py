from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import os
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

# תיקיית מאגר פנים
DB_PATH = "employees"
os.makedirs(DB_PATH, exist_ok=True)


# =========================
# ➕ הוספת עובד למאגר
# =========================
@app.route("/add_employee", methods=["POST"])
def add_employee():
    name = request.form.get("name")
    file = request.files.get("image")

    if not name or not file:
        return jsonify({"error": "missing name or image"}), 400

    path = os.path.join(DB_PATH, f"{name}.jpg")
    file.save(path)

    return jsonify({"status": "saved", "name": name})


# =========================
# 🔍 זיהוי פנים
# =========================
@app.route("/recognize", methods=["POST"])
def recognize():
    file = request.files.get("image")

    if not file:
        return jsonify({"error": "no image provided"}), 400

    np_arr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    try:
        results = DeepFace.find(
            img_path=img,
            db_path=DB_PATH,
            enforce_detection=False
        )

        # אם לא נמצא כלום
        if len(results) == 0 or results[0].empty:
            return jsonify([{"name": "Unknown", "score": 0}])

        best = results[0].iloc[0]

        name = os.path.basename(best["identity"]).split(".")[0]
        distance = float(best["distance"])

        return jsonify([{
            "name": name,
            "score": distance
        }])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 📋 רשימת עובדים
# =========================
@app.route("/employees", methods=["GET"])
def employees():
    files = os.listdir(DB_PATH)
    names = [f.split(".")[0] for f in files]
    return jsonify(names)


# =========================
# 🏠 בדיקה שהשרת עובד
# =========================
@app.route("/")
def home():
    return "DeepFace API is running 🚀"


# =========================
# ▶️ הפעלה מקומית בלבד
# =========================
if __name__ == "__main__":
    app.run(debug=True)