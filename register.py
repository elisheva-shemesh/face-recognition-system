import os
import pickle
import cv2
from insightface.app import FaceAnalysis

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=-1)

# טעינה אם קיים
if os.path.exists("faces.pkl"):
    with open("faces.pkl", "rb") as f:
        known_embeddings, known_names = pickle.load(f)
else:
    known_embeddings = []
    known_names = []

for file in os.listdir("employees"):
    name = file.split(".")[0]

    if name in known_names:
        continue  # כבר קיים

    img = cv2.imread(f"employees/{file}")
    faces = app.get(img)

    if len(faces) > 0:
        embedding = faces[0].embedding
        known_embeddings.append(embedding)
        known_names.append(name)

with open("faces.pkl", "wb") as f:
    pickle.dump((known_embeddings, known_names), f)

print("Updated database!")