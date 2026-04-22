from insightface.app import FaceAnalysis
import cv2
import numpy as np
import pickle

# טעינת מודל
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=-1)

# טעינת מאגר פנים
with open("faces.pkl", "rb") as f:
    known_embeddings, known_names = pickle.load(f)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    faces = app.get(frame)

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

        print(best_name)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == 27:
        break

video.release()
cv2.destroyAllWindows()