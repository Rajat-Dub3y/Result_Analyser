# compare.py
import pandas as pd

def compute_cgpa_ranks(summary_df):
    df = summary_df.copy()

    df_with = df[df["CGPA"].notna()].copy()
    df_without = df[df["CGPA"].isna()].copy()

    df_with["Rank"] = df_with["CGPA"].rank(ascending=False, method="min").astype(int)
    df_without["Rank"] = None

    return pd.concat([df_with, df_without], ignore_index=True) \
             .sort_values(["Rank", "CGPA"], ascending=[True, False], na_position="last")


def compute_sgpa_ranks(sgpa_df):
    df = sgpa_df.copy()

    df_with = df[df["SGPA"].notna()].copy()
    df_without = df[df["SGPA"].isna()].copy()

    df_with["Rank"] = df_with.groupby("Semester")["SGPA"] \
                             .rank(ascending=False, method="min").astype(int)
    df_without["Rank"] = None

    return pd.concat([df_with, df_without], ignore_index=True) \
             .sort_values(["Semester","Rank","SGPA"], na_position="last")


def failed_students(long_df):
    return long_df[long_df["Grade"].isin(["F", "FAIL", "P"])]


def subject_topper(long_df):
    return long_df.sort_values(["SubjectCode","CreditPoints"], ascending=[True, False]) \
                  .groupby("SubjectCode").head(1)


def subject_stats(long_df):
    return long_df.groupby("SubjectCode").agg({
        "CreditPoints": ["mean","max","min","count"],
        "Grade": lambda x: x.value_counts().index[0]
    }).reset_index()

def to_long_subject_df(class_data):
    rows = []
    for roll, st in class_data.items():
        for sem, sem_data in st["Semester"].items():
            if sem_data is None:
                continue
            for subj in sem_data["Subjects"]:
                rows.append({
                    "Roll": roll,
                    "Semester": sem,
                    "SubjectCode": subj["Code"],
                    "Grade": subj["Grade"],
                    "Credit": subj["Credit"],
                    "CreditPoints": subj["CreditPoints"]
                })
    return pd.DataFrame(rows)
