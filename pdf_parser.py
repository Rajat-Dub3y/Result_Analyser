import fitz
import re

def parse_gradecard(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    def find(pattern):
        m = re.search(pattern, text, flags=re.I)
        return m.group(1).strip() if m else None

    name = find(r"NAME\s*:\s*(.*?)\s*ROLL")
    roll = find(r"ROLL\s*NO\.\s*:\s*(\d+)")
    reg = find(r"REGISTRATION\s*NO\s*:\s*(.*?)\s+COLLEGE")
    result = find(r"RESULT.*?SEMESTER\s*:\s*([A-Z]+)") or find(r"RESULT\s*:\s*([A-Z]+)")

    # robust SGPA handling
    sgpa = (
        find(r"SGPA.*?SEMESTER\s*:\s*([0-9.]+)") or
        find(r"SGPA\s*:\s*([0-9.]+)") or
        find(r"SGPA\s*-\s*([0-9.]+)") or
        find(r"SGPA\s*([0-9.]+)") or
        find(r"CGPA\s*:\s*([0-9.]+)")
    )
    sgpa = float(sgpa) if sgpa else None

    rows = []
    pattern = r"([A-Z-]+\s*\d+)\s+(.*?)\s+([A-Z])\s+(\d+)\s+([0-9.]+)\s+([0-9.]+)"
    for m in re.finditer(pattern, text):
        code, subject, grade, points, credit, cpoints = m.groups()
        rows.append({
            "Code": code.strip(),
            "Subject": subject.strip(),
            "Grade": grade,
            "Points": float(points),
            "Credit": float(credit),
            "CreditPoints": float(cpoints)
        })

    return {
        "Name": name,
        "Roll": roll,
        "Registration": reg,
        "SGPA": sgpa,
        "Result": result,
        "Subjects": rows
    }
