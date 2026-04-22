from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import pickle
from insightface.app import FaceAnalysis

app = Flask(__name__)
CORS(app)  # 👈 זה הפתרון

model = FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=-1)

with open("faces.pkl", "rb") as f:
    known_embeddings, known_names = pickle.load(f)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

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

        for i, known_embedding in enumerate(known_embeddings):
            score = cosine_similarity(embedding, known_embedding)

            if score > best_score:
                best_score = score
                best_name = known_names[i]

        if best_score < 0.5:
            best_name = "Unknown"

        results.append({
            "name": best_name,
            "score": float(best_score)
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)