"""
resume_generator.py
Generates synthetic sample resume .txt files for simulation.
Run this once to populate the resumes/ folder.
"""

import os

RESUMES = {
    "resume_alice_chen.txt": """
Alice Chen
Email: alice.chen@email.com | Phone: +1-555-0101
GitHub: github.com/alicechen | LinkedIn: linkedin.com/in/alicechen

OBJECTIVE
Passionate Python Developer with 2 years of experience in machine learning and data analysis.
Seeking a challenging role to apply NLP and deep learning expertise.

SKILLS
Python, Pandas, NumPy, Scikit-learn, TensorFlow, Machine Learning, Deep Learning,
Natural Language Processing, NLP, Data Analysis, Data Visualization, Matplotlib,
Seaborn, SQL, Git, GitHub, Flask, REST API, Docker

EXPERIENCE
Data Scientist Intern | TechCorp | 2022 - 2023
- Built machine learning models using Scikit-learn and TensorFlow
- Performed data analysis on large datasets using Pandas and NumPy
- Developed REST API endpoints using Flask
- Created data visualizations using Matplotlib and Seaborn
- Maintained code repositories using Git and GitHub

EDUCATION
Bachelor of Engineering - Computer Science
State University | 2020 - 2024 | GPA: 8.9/10

PROJECTS
- Resume Screening Tool using NLP and TF-IDF
- Sentiment Analysis using Deep Learning (LSTM)
- Sales Prediction using Machine Learning

CERTIFICATIONS
- Google Data Analytics Certificate
- AWS Machine Learning Specialty
""",

    "resume_bob_sharma.txt": """
Bob Sharma
Email: bob.sharma@email.com | Phone: +1-555-0102

SUMMARY
Frontend Developer with 3 years of experience in web development.
Skilled in React, JavaScript, HTML, CSS, and Node.js.

SKILLS
JavaScript, React, HTML, CSS, Node.js, MongoDB, Express.js,
jQuery, Bootstrap, Figma, Git, Photoshop, UI/UX Design

EXPERIENCE
Frontend Developer | WebAgency | 2021 - 2024
- Built responsive web applications using React and JavaScript
- Designed UI components with HTML, CSS, Bootstrap
- Worked with MongoDB for database management
- Used Git for version control

EDUCATION
Bachelor of Computer Applications
City College | 2018 - 2021

PROJECTS
- E-commerce Website (React + Node.js)
- Portfolio Website (HTML/CSS/JavaScript)
- Blog Platform (MERN Stack)
""",

    "resume_charlie_davis.txt": """
Charlie Davis
Email: charlie.davis@email.com
LinkedIn: linkedin.com/in/charliedavis

OBJECTIVE
Data Analyst with strong Python and SQL skills. Experienced in data visualization
and statistical analysis. Familiar with machine learning concepts.

SKILLS
Python, SQL, Pandas, NumPy, Data Analysis, Data Visualization,
Matplotlib, Seaborn, Excel, Tableau, Power BI, Statistics,
Git, Scikit-learn, Jupyter Notebook

EXPERIENCE
Data Analyst | Analytics Co. | 2022 - 2024
- Analyzed business datasets using Python and Pandas
- Created dashboards using Tableau and Power BI
- Wrote complex SQL queries for data extraction
- Produced data visualizations using Matplotlib and Seaborn
- Collaborated with teams using Git

EDUCATION
BSc Statistics | National University | 2019 - 2022

PROJECTS
- Customer Churn Analysis (Python + Scikit-learn)
- Sales Dashboard (Tableau)
- COVID-19 Data Analysis (Pandas + Matplotlib)
""",

    "resume_diana_patel.txt": """
Diana Patel
Email: diana.patel@email.com | GitHub: github.com/dianapatel

PROFILE
Machine Learning Engineer with 2 years hands-on experience.
Specialist in NLP, deep learning, and production ML pipelines.

SKILLS
Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, NLP,
Natural Language Processing, Scikit-learn, Pandas, NumPy, Keras,
SQL, Git, GitHub, Docker, Kubernetes, Flask, REST API,
Data Analysis, Feature Engineering, MLflow

EXPERIENCE
ML Engineer | AI Startup | 2022 - 2024
- Designed and deployed NLP models for text classification
- Built deep learning pipelines using TensorFlow and PyTorch
- Implemented REST APIs for model serving with Flask
- Used Git and GitHub for all version control
- Optimized models achieving 15% accuracy improvement

EDUCATION
M.Tech - Artificial Intelligence
Tech Institute | 2020 - 2022

PROJECTS
- Chatbot using NLP and Transformers
- Image Classification using Deep Learning
- Resume Screening System using TF-IDF and Cosine Similarity

CERTIFICATIONS
- TensorFlow Developer Certificate (Google)
- Deep Learning Specialization (Coursera)
""",

    "resume_edward_kim.txt": """
Edward Kim
Email: edward.kim@email.com

OBJECTIVE
Recent graduate looking for entry-level software developer position.
Basic knowledge of Java and C++.

SKILLS
Java, C++, HTML, CSS, Microsoft Office, Photoshop, Communication

EDUCATION
Bachelor of Arts - English Literature
Community College | 2019 - 2023

EXPERIENCE
Retail Associate | SuperMart | 2021 - 2023
- Assisted customers with product inquiries
- Managed inventory using Excel spreadsheets
- Trained 3 new employees

PROJECTS
- Personal Blog Website (HTML/CSS)
- College Newsletter (MS Word)
""",

    "resume_fiona_wright.txt": """
Fiona Wright
Email: fiona.wright@email.com | GitHub: github.com/fionawright

SUMMARY
Python Developer with 1.5 years of experience in automation and data science.
Proficient in machine learning, SQL, and REST API development.

SKILLS
Python, Pandas, NumPy, Scikit-learn, Machine Learning, SQL, Git,
GitHub, Flask, REST API, Data Analysis, Matplotlib, Automation,
BeautifulSoup, Selenium, PostgreSQL, Data Visualization

EXPERIENCE
Python Developer | DataTech | 2023 - 2024
- Automated data pipelines using Python and Pandas
- Built machine learning models for prediction tasks
- Developed REST API using Flask and PostgreSQL
- Web scraping automation using BeautifulSoup and Selenium
- Maintained code using Git and GitHub

EDUCATION
Bachelor of Engineering - Information Technology
Regional University | 2019 - 2023

PROJECTS
- Automated Data Pipeline (Python + SQL)
- Price Prediction Model (Scikit-learn)
- Web Scraper for job listings (Python + Selenium)

CERTIFICATIONS
- Python for Data Science (IBM)
""",

    "resume_george_lee.txt": """
George Lee
Email: george.lee@email.com

PROFILE
Graphic Designer with 4 years of creative design experience.
Expert in visual branding and print media design.

SKILLS
Adobe Illustrator, Photoshop, InDesign, Figma, CorelDRAW,
Typography, Color Theory, Branding, Print Design, Video Editing,
After Effects, Premiere Pro, Communication

EXPERIENCE
Senior Graphic Designer | Creative Studio | 2020 - 2024
- Designed logos and brand identities for 50+ clients
- Created marketing materials including brochures and banners
- Produced video content using After Effects and Premiere Pro

EDUCATION
Bachelor of Fine Arts - Graphic Design
Art College | 2016 - 2020
""",
}


def generate_sample_resumes(folder="resumes"):
    """Create sample resume text files in the resumes/ folder."""
    os.makedirs(folder, exist_ok=True)
    for filename, content in RESUMES.items():
        filepath = os.path.join(folder, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
    print(f"  ✅ Generated {len(RESUMES)} sample resumes in '{folder}/'")


if __name__ == "__main__":
    generate_sample_resumes()