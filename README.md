# 🎯 AI Face Recognition Attendance System

An AI-powered attendance system that uses face recognition to automatically mark attendance using image upload or webcam capture.

---

## 🚀 Live Demo

🔗 https://face-attendance-x.streamlit.app/

---

## 📌 Features

* 📸 Upload image or use webcam for attendance
* 🧠 Face recognition using deep learning embeddings (ONNX)
* ⚡ FastAPI backend for processing
* 🎨 Streamlit frontend for interactive UI
* 📊 Attendance dashboard with visualization
* 📁 CSV download support
* 🌐 Deployed on Render & Streamlit Cloud

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* OpenCV
* NumPy
* ONNX Runtime

### Frontend

* Streamlit
* Pandas
* Requests

---

## ⚙️ How It Works

1. User uploads image or captures photo
2. Face is detected using OpenCV
3. Image is preprocessed (resize, normalize)
4. ONNX model extracts facial embeddings
5. Cosine similarity is used to match with known faces
6. Attendance is marked and stored

---

## 📁 Project Structure

```
face-recognition-attendance/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │
│   ├── data/
│   │   └── known_faces/
│
├── frontend/
│   └── app.py
│
└── README.md
```

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/loralin27/face-attendance.git
cd face-attendance
```

---

### 2. Backend Setup

```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### 3. Frontend Setup

```
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 API Endpoints

### 🔹 Mark Attendance

```
POST /mark-attendance
```

### 🔹 Get Attendance Records

```
GET /attendance
```

---

## 📈 Future Improvements

* 🔐 User authentication system
* 🗄️ Database integration (MongoDB)
* 🎥 Real-time video stream recognition
* 🤖 Improved accuracy using advanced models

---

## 👨‍💻 Author

**Loralin Sahoo**
CSE | Silicon Institute of Technology

---

## ⭐ Acknowledgements

* OpenCV
* FastAPI
* Streamlit
* ONNX Runtime

---
