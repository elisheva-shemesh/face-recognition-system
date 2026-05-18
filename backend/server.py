from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

EMP_DIR = "employees"
os.makedirs(EMP_DIR, exist_ok=True)


# =========================
# 🧠 יצירת "חתימה" לתמונה
# =========================
def image_signature(img):
    img = cv2.resize(img, (50, 50))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img.flatten().mean()


# =========================
# ➕ הוספת עובד
# =========================
@app.route("/add_employee", methods=["POST"])
def add_employee():
    name = request.form.get("name")
    file = request.files.get("image")

    if not name or not file:
        return jsonify({"error": "missing data"}), 400

    path = os.path.join(EMP_DIR, f"{name}.jpg")
    file.save(path)

    return jsonify({"status": "saved", "name": name})


# =========================
# 🔍 זיהוי
# =========================
@app.route("/recognize", methods=["POST"])
def recognize():
    file = request.files.get("image")

    if not file:
        return jsonify({"error": "no image"}), 400

    np_arr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    current_sig = image_signature(img)

    best_name = "Unknown"
    best_score = float("inf")

    for f in os.listdir(EMP_DIR):
        ref_img = cv2.imread(os.path.join(EMP_DIR, f))
        if ref_img is None:
            continue

        ref_sig = image_signature(ref_img)
        score = abs(current_sig - ref_sig)

        if score < best_score:
            best_score = score
            best_name = f.split(".")[0]

    # סף זיהוי (אפשר לכוון)
    if best_score > 20:
        best_name = "Unknown"

    return jsonify({
        "name": best_name,
        "score": float(best_score)
    })


# =========================
# 📋 עובדים
# =========================
@app.route("/employees", methods=["GET"])
def employees():
    files = os.listdir(EMP_DIR)
    names = [f.split(".")[0] for f in files]
    return jsonify(names)


# =========================
# 🏠 בדיקה
# =========================
@app.route("/")
def home():
    return "Face Recognition API (FREE VERSION) is running 🚀"


# =========================
# ▶️ הרצה מקומית
# =========================
if __name__ == "__main__":
    app.run(debug=True)