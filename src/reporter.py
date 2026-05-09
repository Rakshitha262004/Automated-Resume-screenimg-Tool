"""
reporter.py
Generates the final screening report as a CSV file.
"""

import os
import pandas as pd
from datetime import datetime


def generate_report(ranked_data, shortlisted, rejected, output_folder="outputs"):
    """
    Create a detailed CSV screening report.

    Args:
        ranked_data: list of dicts with full candidate info
        shortlisted: list of (name, score) tuples
        rejected: list of (name, score) tuples
        output_folder: folder to save the CSV

    Returns:
        path to saved CSV file
    """
    os.makedirs(output_folder, exist_ok=True)

    shortlisted_names = [name for name, _ in shortlisted]

    rows = []
    for idx, entry in enumerate(ranked_data, start=1):
        status = "✅ SHORTLISTED" if entry["filename"] in shortlisted_names else "❌ REJECTED"
        rows.append({
            "Rank":             idx,
            "Resume File":      entry["filename"],
            "TF-IDF Score":     round(entry["tfidf_score"] * 100, 2),
            "Skill Match (%)":  round(entry["skill_score"], 2),
            "Final Score":      entry["final_score"],
            "Matched Skills":   ", ".join(entry["matched_skills"]),
            "Skills Count":     len(entry["matched_skills"]),
            "Status":           status,
            "Screened At":      datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    df = pd.DataFrame(rows)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screening_report_{timestamp}.csv"
    filepath = os.path.join(output_folder, filename)
    df.to_csv(filepath, index=False)

    print(f"\n  ✅ Report saved to: {filepath}")
    return filepath, df