"""
app.py
Streamlit Dashboard for Automated Resume Screening Tool
Run with: streamlit run app.py
"""

import os
import sys
import time
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from io import StringIO

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from extractor import extract_all_resumes, extract_text_from_pdf, extract_text_from_docx
from cleaner import clean_text, extract_skills, load_skills_list
from scorer import (
    calculate_tfidf_scores,
    calculate_skill_score,
    compute_final_score,
    shortlist_candidates,
)
from reporter import generate_report
from resume_generator import generate_sample_resumes

# ── Page Config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Screening Tool",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
/* Main background */
.stApp { background-color: #0f1117; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1f2e 0%, #16213e 100%);
    border-right: 1px solid #2d3561;
}

/* Header banner */
.hero-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #2d3561;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 4px 30px rgba(83, 92, 236, 0.2);
}
.hero-banner h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #535cec, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-banner p {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 0.5rem;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1e2235, #252b43);
    border: 1px solid #2d3561;
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-card .metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #535cec, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card .metric-label {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Status badges */
.badge-shortlisted {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid #10b981;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
}
.badge-rejected {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid #ef4444;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
}

/* Section headers */
.section-header {
    color: #e2e8f0;
    font-size: 1.2rem;
    font-weight: 700;
    border-left: 4px solid #535cec;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem 0;
}

/* Rank table */
.rank-table {
    background: #1e2235;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #2d3561;
}

/* Score bar container */
.score-bar-wrap {
    background: #2d3561;
    border-radius: 8px;
    height: 8px;
    width: 100%;
    margin-top: 4px;
}
.score-bar-fill-green {
    background: linear-gradient(90deg, #10b981, #34d399);
    border-radius: 8px;
    height: 8px;
}
.score-bar-fill-red {
    background: linear-gradient(90deg, #ef4444, #f87171);
    border-radius: 8px;
    height: 8px;
}

/* Upload area styling */
[data-testid="stFileUploader"] {
    border: 2px dashed #2d3561;
    border-radius: 12px;
    padding: 1rem;
    background: #1a1f2e;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #535cec, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.6rem 2rem;
    font-size: 1rem;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(83, 92, 236, 0.4);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(83, 92, 236, 0.6);
}

/* Info box */
.info-box {
    background: rgba(83, 92, 236, 0.08);
    border: 1px solid #535cec;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #c7d2fe;
    font-size: 0.92rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1f2e;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #94a3b8;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #535cec, #7c3aed) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:3rem;'>🤖</div>
        <div style='font-size:1.1rem; font-weight:800;
                    background:linear-gradient(90deg,#535cec,#a78bfa);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            Resume Screener
        </div>
        <div style='color:#64748b; font-size:0.78rem; margin-top:4px;'>
            AI-Powered ATS System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### ⚙️ Screening Settings")

    threshold = st.slider(
        "Shortlist Threshold (%)",
        min_value=10, max_value=90, value=50, step=5,
        help="Candidates scoring above this are shortlisted"
    )

    tfidf_weight = st.slider(
        "TF-IDF Weight",
        min_value=0.1, max_value=0.9, value=0.6, step=0.1,
        help="Weight given to TF-IDF similarity score"
    )
    skill_weight = round(1.0 - tfidf_weight, 1)
    st.markdown(f"<div style='color:#94a3b8; font-size:0.82rem;'>Skill Match Weight: {skill_weight}</div>",
                unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📁 Mode")
    mode = st.radio(
        "Select Mode",
        ["🧪 Use Sample Data", "📤 Upload Your Files"],
        index=0
    )

    st.markdown("---")
    st.markdown("""
    <div style='color:#475569; font-size:0.78rem; text-align:center;'>
        Built with Python + Streamlit<br>
        TF-IDF · Cosine Similarity · NLP
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# HERO BANNER
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <h1>🤖 Automated Resume Screening Tool</h1>
    <p>AI-Powered ATS · TF-IDF Matching · NLP Skill Extraction · Instant Shortlisting</p>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ════════════════════════════════════════════════════════════════════
col_jd, col_skills = st.columns([3, 2])

with col_jd:
    st.markdown('<div class="section-header">📋 Job Description</div>', unsafe_allow_html=True)
    default_jd = open("data/job_description.txt").read() if os.path.exists("data/job_description.txt") else ""
    job_description_input = st.text_area(
        "Paste job description here:",
        value=default_jd,
        height=200,
        placeholder="Enter the job description...",
        label_visibility="collapsed"
    )

with col_skills:
    st.markdown('<div class="section-header">🎯 Required Skills</div>', unsafe_allow_html=True)
    default_skills = open("data/required_skills.txt").read() if os.path.exists("data/required_skills.txt") else ""
    skills_input = st.text_area(
        "One skill per line:",
        value=default_skills,
        height=200,
        placeholder="Python\nPandas\nMachine Learning\n...",
        label_visibility="collapsed"
    )

# Upload mode
uploaded_files = []
if "Upload" in mode:
    st.markdown('<div class="section-header">📤 Upload Resumes</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
    else:
        st.markdown('<div class="info-box">📎 Upload one or more resume files above to begin screening.</div>',
                    unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# SCREEN BUTTON
# ════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
col_btn = st.columns([1, 2, 1])[1]
with col_btn:
    run_screening = st.button("🚀 Start Screening", use_container_width=True)


# ════════════════════════════════════════════════════════════════════
# SCREENING LOGIC
# ════════════════════════════════════════════════════════════════════
if run_screening:
    if not job_description_input.strip():
        st.error("❌ Please enter a job description before screening.")
        st.stop()

    # Progress bar
    progress_bar = st.progress(0, text="Initializing...")
    status_placeholder = st.empty()

    # ── Step 1: Parse skills ─────────────────────────────────────────
    progress_bar.progress(10, text="Loading skills...")
    required_skills = [s.strip() for s in skills_input.strip().split("\n") if s.strip()]

    # ── Step 2: Get resume texts ─────────────────────────────────────
    progress_bar.progress(25, text="Extracting resume texts...")
    raw_resumes = {}

    if "Upload" in mode and uploaded_files:
        import tempfile
        for uf in uploaded_files:
            suffix = os.path.splitext(uf.name)[1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uf.read())
                tmp_path = tmp.name
            if suffix == ".pdf":
                text = extract_text_from_pdf(tmp_path)
            elif suffix == ".docx":
                text = extract_text_from_docx(tmp_path)
            else:
                text = uf.getvalue().decode("utf-8", errors="ignore")
            if text.strip():
                raw_resumes[uf.name] = text
            os.unlink(tmp_path)
    else:
        # Sample data
        if not os.path.exists("resumes") or not os.listdir("resumes"):
            generate_sample_resumes("resumes")
        raw_resumes = extract_all_resumes("resumes")

    if not raw_resumes:
        st.error("❌ No resume text could be extracted.")
        st.stop()

    # ── Step 3: Clean texts ──────────────────────────────────────────
    progress_bar.progress(45, text="Cleaning and preprocessing...")
    time.sleep(0.3)
    cleaned_resumes = {name: clean_text(text) for name, text in raw_resumes.items()}
    jd_clean = clean_text(job_description_input)

    # ── Step 4: Score ────────────────────────────────────────────────
    progress_bar.progress(65, text="Calculating TF-IDF similarity scores...")
    time.sleep(0.3)
    tfidf_scores = calculate_tfidf_scores(cleaned_resumes, jd_clean)

    all_data = []
    for filename in cleaned_resumes:
        ts = tfidf_scores.get(filename, 0.0)
        matched = extract_skills(raw_resumes[filename], required_skills)
        ss = calculate_skill_score(matched, len(required_skills)) if required_skills else 0
        fs = compute_final_score(ts, ss, tfidf_weight, skill_weight)
        all_data.append({
            "filename": filename,
            "tfidf_score": ts,
            "skill_score": ss,
            "final_score": fs,
            "matched_skills": matched,
        })

    all_data.sort(key=lambda x: x["final_score"], reverse=True)

    # ── Step 5: Shortlist ────────────────────────────────────────────
    progress_bar.progress(80, text="Shortlisting candidates...")
    ranked_simple = [(d["filename"], d["final_score"]) for d in all_data]
    shortlisted, rejected = shortlist_candidates(ranked_simple, threshold=threshold)
    shortlisted_names = [s[0] for s in shortlisted]

    # ── Step 6: Report ───────────────────────────────────────────────
    progress_bar.progress(95, text="Generating report...")
    report_path, df_report = generate_report(all_data, shortlisted, rejected)

    progress_bar.progress(100, text="✅ Screening complete!")
    time.sleep(0.5)
    progress_bar.empty()
    status_placeholder.empty()

    st.success(f"✅ Screening complete! {len(all_data)} resumes processed.")

    # ════════════════════════════════════════════════════════════════
    # METRICS ROW
    # ════════════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)

    metrics = [
        (m1, len(all_data), "Total Resumes"),
        (m2, len(shortlisted), "✅ Shortlisted"),
        (m3, len(rejected), "❌ Rejected"),
        (m4, f"{max(d['final_score'] for d in all_data):.1f}%", "Top Score"),
        (m5, f"{np.mean([d['final_score'] for d in all_data]):.1f}%", "Avg Score"),
    ]
    for col, val, label in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════
    # TABS
    # ════════════════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Rankings", "📊 Analytics", "🔍 Resume Details", "📥 Export"
    ])

    # ── TAB 1: Rankings ──────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">🏆 Candidate Rankings</div>',
                    unsafe_allow_html=True)

        for idx, entry in enumerate(all_data, start=1):
            is_short = entry["filename"] in shortlisted_names
            border_color = "#10b981" if is_short else "#ef4444"
            badge = '<span class="badge-shortlisted">✅ SHORTLISTED</span>' if is_short \
                    else '<span class="badge-rejected">❌ REJECTED</span>'
            bar_class = "score-bar-fill-green" if is_short else "score-bar-fill-red"
            score_pct = min(entry["final_score"], 100)

            skills_str = ", ".join(entry["matched_skills"][:6])
            if len(entry["matched_skills"]) > 6:
                skills_str += f" +{len(entry['matched_skills'])-6} more"

            st.markdown(f"""
            <div style="background:#1e2235; border:1px solid {border_color};
                        border-radius:12px; padding:1.2rem 1.4rem;
                        margin-bottom:0.8rem; box-shadow:0 2px 10px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="color:#94a3b8; font-size:0.82rem; font-weight:700;">
                            #{idx}
                        </span>
                        <span style="color:#e2e8f0; font-size:1rem; font-weight:700;
                                     margin-left:0.6rem;">
                            {entry['filename']}
                        </span>
                    </div>
                    <div style="display:flex; align-items:center; gap:1rem;">
                        <span style="color:#a78bfa; font-size:1.3rem; font-weight:800;">
                            {entry['final_score']}%
                        </span>
                        {badge}
                    </div>
                </div>
                <div class="score-bar-wrap" style="margin:0.6rem 0;">
                    <div class="{bar_class}" style="width:{score_pct}%;"></div>
                </div>
                <div style="display:flex; gap:2rem; margin-top:0.4rem;">
                    <span style="color:#64748b; font-size:0.8rem;">
                        📊 TF-IDF: {entry['tfidf_score']*100:.1f}%
                    </span>
                    <span style="color:#64748b; font-size:0.8rem;">
                        🎯 Skills: {entry['skill_score']:.1f}%
                        ({len(entry['matched_skills'])}/{len(required_skills)})
                    </span>
                    <span style="color:#64748b; font-size:0.8rem;">
                        🔑 {skills_str if skills_str else 'No skills matched'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 2: Analytics ─────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">📊 Screening Analytics</div>',
                    unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        # Chart 1: Score Distribution Bar
        with col_a:
            fig1, ax1 = plt.subplots(figsize=(6, 4.5))
            fig1.patch.set_facecolor("#1e2235")
            ax1.set_facecolor("#1e2235")

            names = [d["filename"].replace(".txt","").replace("resume_","")
                     for d in all_data]
            scores = [d["final_score"] for d in all_data]
            colors = ["#10b981" if d["filename"] in shortlisted_names
                      else "#ef4444" for d in all_data]

            bars = ax1.barh(names, scores, color=colors, edgecolor="#0f1117",
                            linewidth=0.5, height=0.6)
            ax1.axvline(x=threshold, color="#f59e0b", linestyle="--",
                        linewidth=1.5, label=f"Threshold ({threshold}%)")
            ax1.set_xlabel("Final Score (%)", color="#94a3b8", fontsize=9)
            ax1.set_title("Candidate Score Distribution", color="#e2e8f0",
                          fontsize=11, fontweight="bold", pad=10)
            ax1.tick_params(colors="#94a3b8", labelsize=8)
            for spine in ax1.spines.values():
                spine.set_edgecolor("#2d3561")
            ax1.set_xlim(0, 105)
            for bar, score in zip(bars, scores):
                ax1.text(score + 1, bar.get_y() + bar.get_height()/2,
                         f"{score:.1f}%", va="center", color="#e2e8f0",
                         fontsize=8, fontweight="bold")
            legend = ax1.legend(facecolor="#2d3561", edgecolor="#535cec",
                                labelcolor="#e2e8f0", fontsize=8)
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close()

        # Chart 2: Shortlisted vs Rejected Pie
        with col_b:
            fig2, ax2 = plt.subplots(figsize=(5, 4.5))
            fig2.patch.set_facecolor("#1e2235")
            ax2.set_facecolor("#1e2235")

            pie_vals = [len(shortlisted), len(rejected)]
            pie_labels = ["Shortlisted", "Rejected"]
            pie_colors = ["#10b981", "#ef4444"]
            explode = (0.05, 0)

            wedges, texts, autotexts = ax2.pie(
                pie_vals, labels=pie_labels, colors=pie_colors,
                autopct="%1.0f%%", startangle=90, explode=explode,
                wedgeprops={"edgecolor": "#0f1117", "linewidth": 2},
                textprops={"color": "#e2e8f0", "fontsize": 9}
            )
            for at in autotexts:
                at.set_fontweight("bold")
                at.set_fontsize(10)
            ax2.set_title("Shortlist Breakdown", color="#e2e8f0",
                          fontsize=11, fontweight="bold", pad=10)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()

        # Chart 3: TF-IDF vs Skill Score Scatter
        col_c, col_d = st.columns(2)

        with col_c:
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            fig3.patch.set_facecolor("#1e2235")
            ax3.set_facecolor("#1e2235")

            for d in all_data:
                color = "#10b981" if d["filename"] in shortlisted_names else "#ef4444"
                ax3.scatter(d["tfidf_score"] * 100, d["skill_score"],
                            c=color, s=120, zorder=5,
                            edgecolors="#e2e8f0", linewidth=0.5)
                short_name = d["filename"].replace(".txt","").replace("resume_","")
                ax3.annotate(short_name,
                             (d["tfidf_score"]*100, d["skill_score"]),
                             textcoords="offset points", xytext=(6, 4),
                             color="#94a3b8", fontsize=7)

            ax3.set_xlabel("TF-IDF Score (%)", color="#94a3b8", fontsize=9)
            ax3.set_ylabel("Skill Match (%)", color="#94a3b8", fontsize=9)
            ax3.set_title("TF-IDF vs Skill Match", color="#e2e8f0",
                          fontsize=11, fontweight="bold")
            ax3.tick_params(colors="#94a3b8", labelsize=8)
            for spine in ax3.spines.values():
                spine.set_edgecolor("#2d3561")

            green_patch = mpatches.Patch(color="#10b981", label="Shortlisted")
            red_patch = mpatches.Patch(color="#ef4444", label="Rejected")
            ax3.legend(handles=[green_patch, red_patch],
                       facecolor="#2d3561", edgecolor="#535cec",
                       labelcolor="#e2e8f0", fontsize=8)
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close()

        # Chart 4: Skills frequency heatmap-style bar
        with col_d:
            all_matched = []
            for d in all_data:
                all_matched.extend(d["matched_skills"])

            if all_matched:
                from collections import Counter
                skill_counts = Counter(all_matched).most_common(10)
                sk_names = [s[0] for s in skill_counts]
                sk_counts = [s[1] for s in skill_counts]

                fig4, ax4 = plt.subplots(figsize=(6, 4))
                fig4.patch.set_facecolor("#1e2235")
                ax4.set_facecolor("#1e2235")

                cmap_colors = plt.cm.plasma(
                    np.linspace(0.3, 0.9, len(sk_names))
                )
                ax4.barh(sk_names, sk_counts, color=cmap_colors,
                         edgecolor="#0f1117", linewidth=0.5, height=0.6)
                ax4.set_xlabel("Times Mentioned", color="#94a3b8", fontsize=9)
                ax4.set_title("Top Skills Across All Resumes",
                              color="#e2e8f0", fontsize=11, fontweight="bold")
                ax4.tick_params(colors="#94a3b8", labelsize=8)
                for spine in ax4.spines.values():
                    spine.set_edgecolor("#2d3561")
                plt.tight_layout()
                st.pyplot(fig4)
                plt.close()

    # ── TAB 3: Resume Details ────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">🔍 Individual Resume Analysis</div>',
                    unsafe_allow_html=True)

        selected = st.selectbox(
            "Select a resume to inspect:",
            [d["filename"] for d in all_data]
        )

        selected_data = next(d for d in all_data if d["filename"] == selected)
        is_selected_short = selected in shortlisted_names

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.metric("Final Score", f"{selected_data['final_score']}%")
        with sc2:
            st.metric("TF-IDF Score", f"{selected_data['tfidf_score']*100:.1f}%")
        with sc3:
            st.metric("Skill Match", f"{selected_data['skill_score']:.1f}%")

        status_color = "#10b981" if is_selected_short else "#ef4444"
        status_text = "✅ SHORTLISTED" if is_selected_short else "❌ REJECTED"
        st.markdown(f"""
        <div style="border:1px solid {status_color}; border-radius:10px;
                    padding:0.8rem 1.2rem; background:rgba(0,0,0,0.2);
                    color:{status_color}; font-weight:700; font-size:1rem;
                    text-align:center; margin:1rem 0;">
            {status_text}
        </div>
        """, unsafe_allow_html=True)

        # Matched skills
        if selected_data["matched_skills"]:
            st.markdown("**✅ Matched Skills:**")
            skills_html = " ".join([
                f'<span style="background:#1e3a2e; color:#10b981; border:1px solid #10b981; '
                f'border-radius:20px; padding:3px 10px; font-size:0.8rem; '
                f'margin:3px; display:inline-block;">{s}</span>'
                for s in selected_data["matched_skills"]
            ])
            st.markdown(skills_html, unsafe_allow_html=True)

        # Missing skills
        missing = [s for s in required_skills
                   if s not in selected_data["matched_skills"]]
        if missing:
            st.markdown("<br>**❌ Missing Skills:**", unsafe_allow_html=True)
            missing_html = " ".join([
                f'<span style="background:#3a1e1e; color:#ef4444; border:1px solid #ef4444; '
                f'border-radius:20px; padding:3px 10px; font-size:0.8rem; '
                f'margin:3px; display:inline-block;">{s}</span>'
                for s in missing
            ])
            st.markdown(missing_html, unsafe_allow_html=True)

        # Raw text preview
        with st.expander("📄 View Raw Resume Text"):
            st.text(raw_resumes.get(selected, "No text available"))

    # ── TAB 4: Export ────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">📥 Export Screening Report</div>',
                    unsafe_allow_html=True)

        st.dataframe(
            df_report,
            use_container_width=True,
            hide_index=True
        )

        csv_data = df_report.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV Report",
            data=csv_data,
            file_name="screening_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-box">
            📁 Report also auto-saved to: <code>outputs/</code> folder<br>
            📌 Report includes: Rank, Scores, Matched Skills, Status, Timestamp
        </div>
        """, unsafe_allow_html=True)