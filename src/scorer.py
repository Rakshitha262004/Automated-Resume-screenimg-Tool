"""
scorer.py
TF-IDF vectorization and cosine similarity scoring.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_tfidf_scores(resume_texts_dict, job_description_text):
    """
    Calculate cosine similarity between each resume and the job description
    using TF-IDF vectorization.

    Args:
        resume_texts_dict: { filename: cleaned_resume_text }
        job_description_text: cleaned job description string

    Returns:
        dict { filename: similarity_score (0.0 to 1.0) }
    """
    if not resume_texts_dict:
        return {}

    filenames = list(resume_texts_dict.keys())
    resume_texts = list(resume_texts_dict.values())

    # Combine job description + all resumes for TF-IDF fitting
    all_texts = [job_description_text] + resume_texts

    # Build TF-IDF matrix
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),      # unigrams and bigrams
        max_features=5000,        # limit vocabulary size
        sublinear_tf=True         # apply log normalization
    )
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Job description is index 0; resumes are 1 onwards
    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]

    # Calculate cosine similarity for each resume
    scores = cosine_similarity(resume_vectors, jd_vector).flatten()

    return dict(zip(filenames, scores))


def calculate_skill_score(matched_skills, total_skills):
    """
    Calculate skill match percentage.
    """
    if total_skills == 0:
        return 0.0
    return (len(matched_skills) / total_skills) * 100


def compute_final_score(tfidf_score, skill_score, tfidf_weight=0.6, skill_weight=0.4):
    """
    Weighted combination of TF-IDF score and skill match score.
    TF-IDF: 60% weight
    Skill match: 40% weight
    Final score out of 100.
    """
    tfidf_normalized = tfidf_score * 100  # convert 0-1 to 0-100
    final = (tfidf_weight * tfidf_normalized) + (skill_weight * skill_score)
    return round(final, 2)


def rank_resumes(scores_dict):
    """
    Sort candidates by score (highest first).
    Returns a sorted list of (filename, score) tuples.
    """
    ranked = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
    return ranked


def shortlist_candidates(ranked_list, threshold=50.0):
    """
    Separate candidates into shortlisted and rejected based on score threshold.
    Default threshold: 50 out of 100.
    """
    shortlisted = [(name, score) for name, score in ranked_list if score >= threshold]
    rejected = [(name, score) for name, score in ranked_list if score < threshold]
    return shortlisted, rejected