import cv2
import numpy as np
import os
import onnxruntime as ort

# ---------------- PATHS ----------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
KNOWN_DIR = os.path.join(BASE_DIR, "data", "known_faces")
MODEL_PATH = os.path.join(BASE_DIR, "backend", "model.onnx")

# ---------------- LOAD MODEL ----------------
session = ort.InferenceSession(MODEL_PATH)

# ---------------- FACE DETECTOR (FIXED HAAR) ----------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- UTILS ----------------
def normalize(v):
    return v / np.linalg.norm(v)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ---------------- EMBEDDING ----------------
def get_embedding(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(80, 80)
    )

    # 🔥 fallback if no face
    if len(faces) == 0:
        print("⚠️ Using full image (fallback)")
        face = img
    else:
        # take largest face
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        x, y, w, h = faces[0]

        margin = int(0.2 * w)
        x1 = max(x - margin, 0)
        y1 = max(y - margin, 0)
        x2 = min(x + w + margin, img.shape[1])
        y2 = min(y + h + margin, img.shape[0])

        face = img[y1:y2, x1:x2]

    face = cv2.resize(face, (112, 112))
    face = face.astype(np.float32) / 255.0
    face = np.expand_dims(face, axis=0)

    input_name = session.get_inputs()[0].name
    embedding = session.run(None, {input_name: face})[0]

    return normalize(embedding[0])

# ---------------- LOAD KNOWN FACES ----------------
known_embeddings = {}

for file in os.listdir(KNOWN_DIR):
    path = os.path.join(KNOWN_DIR, file)
    img = cv2.imread(path)

    if img is None:
        continue

    emb = get_embedding(img)

    if emb is not None:
        name = file.split(".")[0].rstrip("0123456789")
        known_embeddings.setdefault(name, []).append(emb)

# 🔍 DEBUG
print("Loaded people:", list(known_embeddings.keys()))

# 🔥 MEAN EMBEDDING
for name in known_embeddings:
    known_embeddings[name] = np.mean(known_embeddings[name], axis=0)

# ---------------- RECOGNITION ----------------
def recognize_from_image(img_path):
    img = cv2.imread(img_path)

    if img is None:
        return "Invalid image"

    emb = get_embedding(img)

    if emb is None:
        return "No face detected"

    best_match = "Unknown"
    max_sim = -1

    for name, known_emb in known_embeddings.items():
        sim = cosine_similarity(emb, known_emb)

        if sim > max_sim:
            max_sim = sim
            best_match = name

    print("Similarity:", max_sim, "Match:", best_match)

    return best_match if max_sim > 0.6 else "Unknown"