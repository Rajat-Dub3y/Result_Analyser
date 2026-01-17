import pandas as pd
from config import SEM_COUNT

def build_analytics(class_data):
    summary_rows = []
    sgpa_rows = []
    subject_rows = {}
    grade_list = []

    for roll, st in class_data.items():
        row = {
            "Roll": roll,
            "Name": st["Name"],
            "CGPA": st["CGPA"]
        }

        # SGPA per semester
        for sem in range(1, SEM_COUNT + 1):
            sem_data = st["Semester"].get(sem)
            row[f"SGPA{sem}"] = sem_data["SGPA"] if sem_data else None

        summary_rows.append(row)

        # SGPA matrix
        for sem, sem_data in st["Semester"].items():
            if sem_data:
                sgpa_rows.append({
                    "Roll": roll,
                    "Semester": sem,
                    "SGPA": sem_data["SGPA"]
                })

                # subject matrix
                if roll not in subject_rows:
                    subject_rows[roll] = {"Roll": roll}

                for subj in sem_data["Subjects"]:
                    subject_rows[roll][subj["Code"]] = subj["Points"]
                    grade_list.append(subj["Grade"])

    return {
        "summary": pd.DataFrame(summary_rows),
        "sgpa_matrix": pd.DataFrame(sgpa_rows),
        "subject_matrix": pd.DataFrame(subject_rows.values()),
        "grade_distribution": pd.DataFrame({"Grade": grade_list}) \
            .value_counts().reset_index(name="Count")
    }
