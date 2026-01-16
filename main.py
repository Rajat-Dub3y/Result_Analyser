# main.py
from loader import load_all_pdfs
from Compare import compute_ranks, failed_students, subject_topper, subject_stats

df_long, df_wide = load_all_pdfs("./downloads")

df_long.to_csv("gradecard_long.csv", index=False)
df_wide.to_csv("gradecard_summary.csv", index=False)

print("\n--- RANK LIST ---\n")
print(compute_ranks(df_wide)[["Roll","Name","SGPA","Rank"]])
rank_df = compute_ranks(df_wide)
print(rank_df.to_string(index=False))

print("\n--- FAILED STUDENTS ---\n")
print(failed_students(df_long)[["Roll","Name","Subject","Grade"]])

print("\n--- SUBJECT TOPPERS ---\n")
print(subject_topper(df_long)[["SubjectCode","Subject","Name","Grade","CreditPoints"]])

print("\n--- SUBJECT STATS ---\n")
print(subject_stats(df_long))
