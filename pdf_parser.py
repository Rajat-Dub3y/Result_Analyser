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
    result = find(r"RESULT.*?SEMESTER\s*:\s*([A-Z]+)")

    # detect SGPA
    odd_sgpa = find(r"SGPA\s*ODD.*?SEMESTER\s*:\s*([0-9.]+)")
    even_sgpa = find(r"SGPA\s*EVEN.*?SEMESTER\s*:\s*([0-9.]+)")
    ygpa = find(r"YGPA\s*[:\-]?\s*([0-9.]+)")

    # convert to float when found
    odd_sgpa = float(odd_sgpa) if odd_sgpa else None
    even_sgpa = float(even_sgpa) if even_sgpa else None
    ygpa = float(ygpa) if ygpa else None

    # final SGPA rule:
    # odd semesters → use odd_sgpa
    # even semesters → use even_sgpa
    sgpa = odd_sgpa
    if even_sgpa is not None:
        sgpa = even_sgpa

    # subjects extraction
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

    # calculate totals
    credit_sum = sum(row["Credit"] for row in rows)
    credit_points_sum = sum(row["CreditPoints"] for row in rows)

    return {
        "Name": name,
        "Roll": roll,
        "Registration": reg,
        "OddSGPA": odd_sgpa,
        "EvenSGPA": even_sgpa,
        "YGPA": ygpa,
        "SGPA": sgpa,
        "Result": result,
        "Subjects": rows,
        "CreditSum": credit_sum,
        "CreditPointsSum": credit_points_sum
    }
