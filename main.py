from model import load_class_data
from analytics import build_analytics
from exporter import export_all
from Compare import (
    compute_cgpa_ranks,
    compute_sgpa_ranks,
    failed_students,
    subject_topper,
    subject_stats,
    to_long_subject_df
)
import os
from config import OUTPUT_DIR

def main():
    print("[*] Loading class data...")
    class_data = load_class_data()

    print("[*] Building analytics tables...")
    analytics = build_analytics(class_data)

    print("[*] Exporting base CSVs...")
    export_all(analytics)

    print("[*] Computing comparison analytics...")
    summary_df = analytics["summary"]
    sgpa_df = analytics["sgpa_matrix"]

    long_df = to_long_subject_df(class_data)
    cgpa_rank_df = compute_cgpa_ranks(summary_df)
    sgpa_rank_df = compute_sgpa_ranks(sgpa_df)
    fail_df = failed_students(long_df)
    topper_df = subject_topper(long_df)
    stats_df = subject_stats(long_df)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cgpa_rank_df.to_csv(f"{OUTPUT_DIR}/cgpa_rank.csv", index=False)
    sgpa_rank_df.to_csv(f"{OUTPUT_DIR}/sgpa_rank.csv", index=False)
    fail_df.to_csv(f"{OUTPUT_DIR}/failed_subjects.csv", index=False)
    topper_df.to_csv(f"{OUTPUT_DIR}/subject_toppers.csv", index=False)
    stats_df.to_csv(f"{OUTPUT_DIR}/subject_stats.csv", index=False)

    print("[✔] Comparison analytics exported to /output")

if __name__ == "__main__":
    main()
