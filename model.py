import os
from config import DOWNLOAD_DIR, SEM_COUNT
from pdf_parser import parse_gradecard

def load_student(roll):
    roll_path = os.path.join(DOWNLOAD_DIR, roll)
    if not os.path.isdir(roll_path):
        return None

    student = {
        "Roll": roll,
        "Name": None,
        "Semester": {},
        "TotalCredits": 0.0,
        "TotalCreditPoints": 0.0,
        "CGPA": None
    }

    for sem in range(1, SEM_COUNT + 1):
        pdf_path = os.path.join(roll_path, f"sem{sem}.pdf")
        if not os.path.exists(pdf_path):
            student["Semester"][sem] = None
            continue

        parsed = parse_gradecard(pdf_path)

        if student["Name"] is None:
            student["Name"] = parsed["Name"]

        student["Semester"][sem] = parsed

        # accumulate credits (works even if some sem = None)
        student["TotalCredits"] += parsed["CreditSum"]
        student["TotalCreditPoints"] += parsed["CreditPointsSum"]

    if student["TotalCredits"] > 0:
        student["CGPA"] = round(student["TotalCreditPoints"] / student["TotalCredits"], 2)

    return student


def load_class_data():
    class_data = {}

    for roll in os.listdir(DOWNLOAD_DIR):
        if os.path.isdir(os.path.join(DOWNLOAD_DIR, roll)):
            st = load_student(roll)
            if st:
                class_data[roll] = st

    return class_data
