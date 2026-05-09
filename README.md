# 🤖 Automated Resume Screening Tool

> AI-powered resume screening system that replicates real-world ATS (Applicant Tracking Systems)
> using Python, TF-IDF, Cosine Similarity, and NLP.



![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)




![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)




![NLP](https://img.shields.io/badge/NLP-TF--IDF-green?style=flat-square)




![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)



---

## 📌 Problem Statement

Companies receive hundreds of resumes per job posting. Manual screening is
time-consuming and error-prone. This tool automates the process using NLP and
machine learning to match resumes to job descriptions and rank candidates.

---

## 🚀 Features

- ✅ PDF, DOCX, and TXT resume parsing
- ✅ NLP text preprocessing (stopwords, lemmatization)
- ✅ TF-IDF vectorization + Cosine Similarity scoring
- ✅ Keyword/skill matching against required skills list
- ✅ Weighted scoring (TF-IDF + Skills)
- ✅ Candidate ranking and shortlisting
- ✅ CSV report generation
- ✅ Streamlit dark-themed dashboard with charts
- ✅ Upload your own resumes or use sample data

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.9+ |
| NLP | NLTK, Regex |
| ML | Scikit-learn (TF-IDF, Cosine Similarity) |
| Resume Parsing | PyPDF2, pdfplumber, python-docx |
| Data | Pandas, NumPy |
| Dashboard | Streamlit |
| Charts | Matplotlib, Seaborn |

---

## 📁 Project Structure

Automated-Resume-Screening-Tool/
├── resumes/              ← Sample resume files
├── data/                 ← Job description & skills list
├── src/                  ← Core Python modules
│   ├── extractor.py
│   ├── cleaner.py
│   ├── scorer.py
│   ├── reporter.py
│   └── resume_generator.py
├── outputs/              ← Generated CSV reports
├── images/               ← Screenshots
├── app.py                ← Streamlit dashboard
├── main.py               ← CLI execution
├── requirements.txt
└── README.md


---

## ⚙️ Installation

bash
git clone https://github.com/YOUR_USERNAME/Automated-Resume-Screening-Tool.git
cd Automated-Resume-Screening-Tool

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

--

## How to Run
# CLI mode
python main.py

--

# Dashboard mode
streamlit run app.py

--

## 🎓 Learning Outcomes
Resume parsing from PDF/DOCX using Python
NLP preprocessing pipeline
TF-IDF vectorization and cosine similarity
Weighted scoring and ranking algorithms
Streamlit dashboard development
Professional GitHub documentation

--

## 📄 License
MIT License — free to use and modify.
