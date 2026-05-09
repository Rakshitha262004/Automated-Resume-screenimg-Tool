"""
cleaner.py
Text preprocessing and cleaning functions.
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (silent if already downloaded)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("punkt", quiet=True)

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def clean_text(text):
    """
    Full NLP preprocessing pipeline:
    1. Lowercase
    2. Remove URLs
    3. Remove email addresses
    4. Remove punctuation and special characters
    5. Remove extra whitespace
    6. Remove stopwords
    7. Lemmatize words
    """
    if not text:
        return ""

    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Step 3: Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)

    # Step 4: Remove phone numbers
    text = re.sub(r"\+?\d[\d\s\-]{8,}\d", "", text)

    # Step 5: Remove punctuation and special chars, keep alphanumeric + spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Step 6: Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Step 7: Tokenize
    tokens = text.split()

    # Step 8: Remove stopwords and short tokens
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]

    # Step 9: Lemmatize
    tokens = [LEMMATIZER.lemmatize(t) for t in tokens]

    return " ".join(tokens)


def extract_skills(text, skills_list):
    """
    Find which skills from the required list appear in the resume text.
    Returns a list of matched skills.
    """
    text_lower = text.lower()
    matched = []
    for skill in skills_list:
        # Use word boundary matching for accuracy
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            matched.append(skill)
    return matched


def load_skills_list(skills_file_path):
    """
    Load required skills from a text file (one skill per line).
    """
    skills = []
    try:
        with open(skills_file_path, "r", encoding="utf-8") as f:
            for line in f:
                skill = line.strip()
                if skill:
                    skills.append(skill)
    except Exception as e:
        print(f"  [ERROR] Could not load skills file: {e}")
    return skills