# compare.py
import pandas as pd

def compute_ranks(df_wide):
    df = df_wide.copy()

    # separate missing SGPA
    df_with = df[df["SGPA"].notna()].copy()
    df_without = df[df["SGPA"].isna()].copy()

    # rank only those with SGPA values
    df_with["Rank"] = df_with["SGPA"].rank(ascending=False, method="min").astype(int)

    # merge back (no ranks for missing)
    df_without["Rank"] = None

    return pd.concat([df_with, df_without], ignore_index=True) \
             .sort_values(["Rank", "SGPA"], na_position="last")


def failed_students(df_long):
    return df_long[df_long["Grade"].isin(["F", "P", "FAIL"])]

def subject_topper(df_long):
    return df_long.sort_values(["SubjectCode","CreditPoints"], ascending=[True, False]) \
                  .groupby("SubjectCode").head(1)

def subject_stats(df_long):
    return df_long.groupby("SubjectCode").agg({
        "CreditPoints": ["mean","max","min"],
        "Grade": lambda x: x.value_counts().index[0]
    })
