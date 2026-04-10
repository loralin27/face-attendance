import cv2
import os
import numpy as np
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8000/mark-attendance"
# same logic as your face_service
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KNOWN_DIR = os.path.join(BASE_DIR, "data", "known_faces")

def load_known_faces():
    known_faces = {}

    for file in os.listdir(KNOWN_DIR):
        path = os.path.join(KNOWN_DIR, file)

        img = cv2.imread(path)
        img = cv2.resize(img, (100, 100))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        known_faces[file.split(".")[0]] = img.flatten()

    return known_faces


def recognize_face(frame, known_faces):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (100, 100))
    input_face = gray.flatten()

    min_dist = float("inf")
    best_match = "Unknown"

    for name, face in known_faces.items():
        dist = np.linalg.norm(input_face - face)

        if dist < min_dist:
            min_dist = dist
            best_match = name
            

    return best_match if min_dist < 15000 else "Unknown"


# 🔥 MAIN FUNCTION
def start_webcam():
    known_faces = load_known_faces()

    cap = cv2.VideoCapture(0)

    marked = set()  # avoid duplicate attendance

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        name = recognize_face(frame, known_faces)

        if name != "Unknown" and name not in marked:
            marked.add(name)

            print(f"{name} detected → sending to backend...")

        try:
            # send image to backend
            with open("temp.jpg", "wb") as f:
                cv2.imwrite("temp.jpg", frame)

            with open("temp.jpg", "rb") as f:
                response = requests.post(
                    API_URL,
                    files={"file": f}
                )

            print("Backend response:", response.json())

        except Exception as e:
            print("Error sending to backend:", e)
        
        # display
        cv2.putText(frame, name, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

        cv2.imshow("Attendance Camera", frame)

        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_webcam()