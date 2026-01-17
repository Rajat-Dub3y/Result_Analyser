import fitz  # PyMuPDF
import re
import csv

def parse_marks(text):
    marks = {}
    for line in text.split("\n"):
        match = re.search(r"(.*)\s-\s(\d{2,3})", line)
        if match:
            subject = match.group(1).strip()
            score = int(match.group(2))
            marks[subject] = score
    
    sgpa_match = re.search(r"SGPA[:\s]+([\d.]+)", text)
    if sgpa_match:
        marks["SGPA"] = float(sgpa_match.group(1))

    return marks

def save_csv(data, filename="results.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll", "Subject", "Marks"])
        for roll, results in data.items():
            for subject, marks in results.items():
                writer.writerow([roll, subject, marks])
import re

def parse_result_text(text):
    data = {}

    # Basic info
    name = re.search(r"NAME\s*:\s*(.+)", text)
    roll = re.search(r"ROLL NO\.\s*:\s*(\d+)", text)
    sgpa = re.search(r"SGPA.*?SEMESTER\s*:\s*([\d.]+)", text)

    data["name"] = name.group(1).strip() if name else None
    data["roll"] = roll.group(1).strip() if roll else None
    data["sgpa"] = float(sgpa.group(1)) if sgpa else None

    # Extract subject rows
    subjects = []
    pattern = r"([A-Z\-]+\s*\d+)\s+(.+?)\s+([A-Z]{1})\s+(\d+)\s+([\d.]+)\s+([\d.]+)"
    rows = re.findall(pattern, text)

    for row in rows:
        subjects.append({
            "code": row[0].strip(),
            "subject": row[1].strip(),
            "grade": row[2].strip(),
            "points": int(row[3]),
            "credit": float(row[4]),
            "credit_points": float(row[5])
        })

    data["subjects"] = subjects
    return data

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

text = extract_text("./downloads/10331723001/sem2.pdf")
print(text)
