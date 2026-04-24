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
admins = ["elisheva"]
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

@app.route("/")
def home():
    return """
    <h1>Face Recognition System</h1>
    <a href='/add'>➕ Add Employee</a><br><br>
    <a href='/attendance'>🕒 Attendance</a>
    """

@app.route("/add")
def add_page():
    return """
    <h2>Add Employee</h2>
    <input type='text' id='name' placeholder='Employee name'>
    <input type='file' id='image'>
    <button onclick='upload()'>Save</button>

    <script>
    async function upload() {
        let name = document.getElementById('name').value;
        let file = document.getElementById('image').files[0];

        let formData = new FormData();
        formData.append("name", name);
        formData.append("image", file);

        await fetch("/add_employee", {
            method: "POST",
            body: formData
        });

        alert("Employee added");
    }
    </script>
    """

@app.route("/add_employee", methods=["POST"])
def add_employee():
    name = request.form["name"]
    file = request.files["image"]

    path = f"employees/{name}.jpg"
    file.save(path)

    return jsonify({"status": "saved"})

@app.route("/attendance")
def attendance_page():
    return """
    <h2>Attendance</h2>

    <video id="video" width="400" autoplay></video>
    <br>
    <button onclick="capture()">Check In/Out</button>

    <pre id="result"></pre>

    <script>
    const video = document.getElementById('video');

    navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream);

    async function capture() {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0);

        canvas.toBlob(async (blob) => {
            let formData = new FormData();
            formData.append("image", blob);

            let res = await fetch("/recognize", {
                method: "POST",
                body: formData
            });

            let data = await res.json();
            document.getElementById("result").innerText =
                JSON.stringify(data, null, 2);
        }, "image/jpeg");
    }
    </script>
    """

@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(known_names)
    
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = users.get(data["username"])

    if user and user["password"] == data["password"]:
        return jsonify({
            "success": True,
            "role": user["role"],
            "username": data["username"]
        })

    return jsonify({"success": False}), 401

@app.route("/report/<name>", methods=["GET"])
def report(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, check_in, check_out
        FROM attendance
        WHERE name=?
        ORDER BY date DESC
    """, (name,))

    data = cursor.fetchall()
    conn.close()

    return jsonify(data)

@app.route("/identify", methods=["POST"])
def identify():
    file = request.files["image"]
    img_bytes = file.read()

    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    faces = model.get(frame)

    for face in faces:
        embedding = face.embedding

        best_score = 0
        best_name = "Unknown"

        for i, known_embedding in enumerate(known_embeddings):
            score = cosine_similarity(embedding, known_embedding)

            if score > best_score:
                best_score = score
                best_name = known_names[i]

        if best_score < 0.5:
            best_name = "Unknown"

        is_admin = best_name in admins

        return jsonify({
            "name": best_name,
            "is_admin": is_admin
        })

    return jsonify({
        "name": "Unknown",
        "is_admin": False
    })


if __name__ == "__main__":
    app.run(debug=True)