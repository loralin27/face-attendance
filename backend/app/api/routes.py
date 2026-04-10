from fastapi import APIRouter, UploadFile, File
import shutil

from ..services.face_service import recognize_from_image
from ..services.attendance_service import mark_attendance, get_all_attendance

router = APIRouter()

TEMP_PATH = "temp.jpg"


@router.post("/mark-attendance")
async def mark(file: UploadFile = File(...)):
    try:
        with open(TEMP_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        name = recognize_from_image(TEMP_PATH)

        if name == "Unknown" or name == "No face detected":
            return {
            "status": "fail",
            "message": f"⚠️ {name}"
            }

        record = mark_attendance(name)

        return {
            "status": "success",
            "data": record
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/attendance")
def get_attendance():
    return {
        "status": "success",
        "data": get_all_attendance()
    }