from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import pickle
import sqlite3
from datetime import datetime
from insightface.app import FaceAnalysis

app = Flask(__name__)
CORS(app)

# מודל זיהוי פנים
model = FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=-1)

# טעינת מאגר פנים
with open("faces.pkl", "rb") as f:
    known_embeddings, known_names = pickle.load(f)

# חישוב דמיון
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 🔥 פונקציית נוכחות (תוקן indentation)
def mark_attendance(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    today = datetime.now().date()
    now_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute("""
        SELECT * FROM attendance
        WHERE name=? AND date=?
    """, (name, today))

    record = cursor.fetchone()

    if record is None:
        cursor.execute("""
            INSERT INTO attendance (name, date, check_in)
            VALUES (?, ?, ?)
        """, (name, today, now_time))

        status = "check-in"

    elif record[3] is not None and record[4] is None:
        cursor.execute("""
            UPDATE attendance
            SET check_out=?
            WHERE id=?
        """, (now_time, record[0]))

        status = "check-out"

    else:
        status = "already marked"

    conn.commit()
    conn.close()

    return status


# API לזיהוי
@app.route("/recognize", methods=["POST"])
def recognize():
    file = request.files["image"]
    img_bytes = file.read()

    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    faces = model.get(frame)

    results = []

    for face in faces:
        embedding = face.embedding

        best_score = 0
        best_name = "Unknown"
        status = "no action"  # 🔥 תיקון קריטי

        for i, known_embedding in enumerate(known_embeddings):
            score = cosine_similarity(embedding, known_embedding)

            if score > best_score:
                best_score = score
                best_name = known_names[i]

        if best_score < 0.5:
            best_name = "Unknown"
        else:
            status = mark_attendance(best_name)

        results.append({
            "name": best_name,
            "score": float(best_score),
            "status": status
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)