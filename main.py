"""
main.py
Main execution script for Automated Resume Screening Tool.
Run this file to screen all resumes and generate report.
"""

import os
import sys

# Add src/ to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from extractor import extract_all_resumes
from cleaner import clean_text, extract_skills, load_skills_list
from scorer import (
    calculate_tfidf_scores,
    calculate_skill_score,
    compute_final_score,
    rank_resumes,
    shortlist_candidates,
)
from reporter import generate_report
from resume_generator import generate_sample_resumes


def load_job_description(jd_path):
    """Load job description from text file."""
    try:
        with open(jd_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"  [ERROR] Cannot load job description: {e}")
        return ""


def main():
    print("=" * 60)
    print("   🤖 AUTOMATED RESUME SCREENING TOOL")
    print("=" * 60)

    # ── Step 0: Generate sample resumes if folder is empty ──────────
    resume_folder = "resumes"
    if not os.path.exists(resume_folder) or not os.listdir(resume_folder):
        print("\n[SETUP] No resumes found. Generating sample resumes...")
        generate_sample_resumes(resume_folder)

    # ── Step 1: Load Job Description ────────────────────────────────
    print("\n[1/6] Loading job description...")
    jd_path = os.path.join("data", "job_description.txt")
    job_description_raw = load_job_description(jd_path)
    if not job_description_raw:
        print("  [ERROR] Job description is empty. Check data/job_description.txt")
        return
    job_description_clean = clean_text(job_description_raw)
    print(f"  ✅ Job description loaded ({len(job_description_raw)} chars)")

    # ── Step 2: Load Required Skills ────────────────────────────────
    print("\n[2/6] Loading required skills...")
    skills_path = os.path.join("data", "required_skills.txt")
    required_skills = load_skills_list(skills_path)
    print(f"  ✅ {len(required_skills)} required skills loaded: {required_skills[:5]}...")

    # ── Step 3: Extract Resume Texts ────────────────────────────────
    print("\n[3/6] Extracting text from resumes...")
    raw_resumes = extract_all_resumes(resume_folder)
    if not raw_resumes:
        print("  [ERROR] No resumes extracted.")
        return

    # ── Step 4: Clean resume texts ──────────────────────────────────
    print("\n[4/6] Cleaning and preprocessing texts...")
    cleaned_resumes = {
        name: clean_text(text) for name, text in raw_resumes.items()
    }

    # ── Step 5: Score each resume ───────────────────────────────────
    print("\n[5/6] Calculating similarity scores...")
    tfidf_scores = calculate_tfidf_scores(cleaned_resumes, job_description_clean)

    all_data = []
    for filename in cleaned_resumes:
        raw_text = raw_resumes[filename]
        tfidf_score = tfidf_scores.get(filename, 0.0)
        matched_skills = extract_skills(raw_text, required_skills)
        skill_score = calculate_skill_score(matched_skills, len(required_skills))
        final_score = compute_final_score(tfidf_score, skill_score)

        all_data.append({
            "filename":      filename,
            "tfidf_score":   tfidf_score,
            "skill_score":   skill_score,
            "final_score":   final_score,
            "matched_skills": matched_skills,
        })

    # Sort by final score
    all_data.sort(key=lambda x: x["final_score"], reverse=True)

    # ── Step 6: Shortlist and Report ────────────────────────────────
    print("\n[6/6] Generating report...")
    ranked_simple = [(d["filename"], d["final_score"]) for d in all_data]
    shortlisted, rejected = shortlist_candidates(ranked_simple, threshold=50.0)

    report_path, df = generate_report(all_data, shortlisted, rejected, output_folder="outputs")

    # ── Print Summary ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("   📊 SCREENING RESULTS SUMMARY")
    print("=" * 60)
    print(f"\n  Total Resumes Screened : {len(all_data)}")
    print(f"  ✅ Shortlisted         : {len(shortlisted)}")
    print(f"  ❌ Rejected            : {len(rejected)}")
    print(f"\n  {'Rank':<5} {'Resume':<35} {'Score':<8} {'Status'}")
    print("  " + "-" * 60)

    for idx, entry in enumerate(all_data, start=1):
        status = "✅ SHORTLISTED" if entry["filename"] in [s[0] for s in shortlisted] else "❌ REJECTED"
        print(f"  {idx:<5} {entry['filename']:<35} {entry['final_score']:<8} {status}")

    print(f"\n  📁 Full report saved to: {report_path}")
    print("=" * 60)
    print("\n  Run: streamlit run app.py  →  for visual dashboard")
    print("=" * 60)


if __name__ == "__main__":
    main()