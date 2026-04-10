from datetime import datetime

attendance_db = []

def mark_attendance(name):
    # prevent duplicate entry
    for record in attendance_db:
        if record["name"] == name:
            return record

    record = {
        "name": name,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    attendance_db.append(record)
    return record


def get_all_attendance():
    return attendance_db