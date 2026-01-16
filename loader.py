# loader.py
import os
import pandas as pd
from pdf_parser import parse_gradecard

def load_all_pdfs(folder="./pdfs"):
    """Load all pdfs and return long & wide dataframes."""

    records_long = []  # multiple rows per student
    summary = []       # one row per student

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            data = parse_gradecard(os.path.join(folder, file))

            # create long-format rows
            for s in data["Subjects"]:
                records_long.append({
                    "Roll": data["Roll"],
                    "Name": data["Name"],
                    "SubjectCode": s["Code"],
                    "Subject": s["Subject"],
                    "Grade": s["Grade"],
                    "Credit": s["Credit"],
                    "CreditPoints": s["CreditPoints"],
                    "SGPA": data["SGPA"],
                    "Result": data["Result"]
                })

            # create wide summary
            summary.append({
                "Roll": data["Roll"],
                "Name": data["Name"],
                "SGPA": data["SGPA"],
                "Result": data["Result"],
                "TotalSubjects": len(data["Subjects"]),
                "TotalCredits": sum(s["Credit"] for s in data["Subjects"]),
                "TotalCreditPoints": sum(s["CreditPoints"] for s in data["Subjects"])
            })

    df_long = pd.DataFrame(records_long)
    df_wide = pd.DataFrame(summary)

    return df_long, df_wide
