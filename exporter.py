import os
from config import OUTPUT_DIR

def export_all(analytics):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    analytics["summary"].to_csv(f"{OUTPUT_DIR}/students_summary.csv", index=False)

    # CGPA ranking
    rank_df = analytics["summary"].sort_values("CGPA", ascending=False)
    rank_df.insert(0, "Rank", range(1, len(rank_df) + 1))
    rank_df.to_csv(f"{OUTPUT_DIR}/cgpa_rank.csv", index=False)

    analytics["sgpa_matrix"].to_csv(f"{OUTPUT_DIR}/sgpa_matrix.csv", index=False)
    analytics["subject_matrix"].to_csv(f"{OUTPUT_DIR}/subject_matrix.csv", index=False)
    analytics["grade_distribution"].to_csv(f"{OUTPUT_DIR}/grade_distribution.csv", index=False)

    print("[✔] CSVs exported to /output")
