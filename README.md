# 🎯 AI-Powered Career Recommendation and Skill Gap Analysis System

<div align="center">

**An intelligent, fully Streamlit application that maps your skills to the right career and shows you exactly what to learn next.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#-license)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

[Overview](#overview) • [Features](#features) • [Tech Stack](#tech-stack) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots) • [Roadmap](#future-improvements) • [License](#license)

</div>

---

<a id="overview"></a>
## 📖 Overview

The **AI-Powered Career Recommendation and Skill Gap Analysis System** is an interactive, data-driven web application built with Streamlit that helps students and early-career professionals discover the career paths best suited to their existing skill set.

Instead of generic career advice, the system takes a quantitative approach: it compares a user's skills against **188 curated career profiles** (backed by a dataset of **2,400+ distinct skills**), calculates compatibility scores, identifies precise skill gaps, and generates a **personalized, month-by-month learning roadmap** complete with course recommendations to get the user career-ready.

Built as a college data science project, it combines practical data engineering (skill/course/career JSON datasets), applied statistics (NumPy-based scoring), and an intuitive multi-panel dashboard to turn "what career should I pursue?" into a structured, actionable plan.

> 💡 All matching, scoring, and recommendation logic runs locally against local JSON datasets, no AI/ML API calls required for the core analysis.

---

<a id="features"></a>
## ✨ Features

### 🎯 Career Matching Engine
- Matches user skills against every career profile in the dataset using NumPy-vectorized scoring.
- Calculates a compatibility percentage for each career path.
- Surfaces the **Top 5 best-fit careers**, ranked and visualized with an interactive horizontal bar chart.

### 📉 Skill Gap Analysis
- Instantly identifies which required skills are missing for a chosen career.
- Presents gaps in a clean, scannable checklist.
- Helps users prioritize what to learn instead of guessing.

### 📊 Career Readiness Score
- Converts skill overlap into a single, intuitive **readiness percentage**.
- Displayed via a live **Plotly gauge chart**.
- Contextual feedback (Excellent / On track / Significant gaps) based on score thresholds.

### 📚 Course Recommendation Engine
- Cross-references missing skills against a curated course database.
- Recommends specific courses per missing skill, complete with provider name and direct clickable links.
- Rendered as an interactive, sortable data table.

### 🛣️ Personalized Learning Roadmap
- Auto-generates a **month-wise roadmap** (up to 5 focus months).
- Assigns one target skill per stage for a structured, non-overwhelming learning journey.
- Displayed as clean roadmap cards, one per "Month."

### 📈 Career Insights Dashboard
- Compares the top-matched careers side-by-side across **Match Score**, **Difficulty**, and **Learning Time**.
- Difficulty-coded bar chart (green → red) for at-a-glance comparison.
- Highlights the single **Best Career Match** in a dedicated summary card.

### 📄 Resume Parsing
- Upload a PDF resume and skills are **automatically extracted** via `pdfplumber` text parsing and keyword matching against the master skills list.
- Manual skill entry is also fully supported as an alternative input path.
- Graceful handling of resumes with no detectable technical skills.

---

## 🔄 Workflow

```
Resume Upload / Manual Skill Input
              ↓
        Career Matching
              ↓
        Career Selection
              ↓
       Skill Gap Analysis
              ↓
     Career Readiness Score
              ↓
     Course Recommendation
              ↓
   Career Insights Dashboard
              ↓
       Learning Roadmap
```

---

<a id="tech-stack"></a>
## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python 3.9+ |
| **Frontend / App Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Plotly |
| **Resume Parsing** | pdfplumber |
| **Data Storage** | JSON (`careers.json`, `skills.json`, `career_info.json`, `courses.json`) |
| **Dev Tools** | Jupyter Lab, Anaconda, Git, GitHub |

### Project Structure

```
CareerRecommendationSystem/
│
├── app.py                     # Main Streamlit application (UI + workflow orchestration)
├── modules/
│   └── helpers.py             # Core logic: matching, scoring, gap analysis, parsing
├── data/
│   ├── careers.json           # 188 careers with required skills
│   ├── skills.json            # Master skills taxonomy (2,400+ skills)
│   ├── career_info.json       # Difficulty ratings & learning time per career
│   └── courses.json           # Course catalog mapped to individual skills
├── requirements.txt
└── README.md
```

---

<a id="installation"></a>
## ⚙️ Installation

**Prerequisites:** Python 3.9 or higher, pip, Git

```bash
# 1. Fork the repository
#    Click the "Fork" button at the top-right of this repo on GitHub
#    to create your own copy under your account.

# 2. Clone your fork
git clone https://github.com/yourusername/CareerRecommendationSystem.git
cd CareerRecommendationSystem

# 3. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Launch the app
streamlit run app.py
```

> 🍴 Forking is recommended if you plan to customize the datasets, add features, or contribute back via a pull request. If you just want to run the app locally, cloning directly also works.

The app will open automatically in your browser at `http://localhost:8501`.

---

<a id="usage"></a>
## 🚀 Usage

1. **Provide your skills**
   - Choose **Manual Skills** and type a comma-separated list, *or*
   - Choose **Resume Upload** and upload a PDF resume skills are auto-extracted.
2. **Pick your target career** from the dropdown of 188 available career paths.
3. Click **Analyze**.
4. Explore your results:
   - Missing skills for the chosen career
   - Your career readiness score (gauge chart)
   - Your top 5 best-matched careers overall
   - A side-by-side comparison of match score, difficulty, and learning time
   - Recommended courses for each missing skill, with direct links
   - A month-by-month learning roadmap to close the gap

---

<a id="screenshots"></a>
## 📸 Screenshots

### Dashboard
<img width="1918" height="912" alt="Dashboard" src="https://github.com/user-attachments/assets/838296c3-25dc-4d93-b983-3c0e57b0243e" />

### Career Matching · Skill Gap Analysis · Readiness Score
<img width="1918" height="916" alt="Career Matching, Skill Gap Analysis, Readiness Score" src="https://github.com/user-attachments/assets/f29e3c0c-ce35-4e92-a3c3-08ff5ae27acc" />

### Recommended Courses · Matched Career Insights · Best Career Match
<img width="1918" height="977" alt="Recommended Courses, Career Insights, Best Match" src="https://github.com/user-attachments/assets/39eb53e1-90e9-4574-9297-cb95fcba8ef4" />

### Learning Roadmap
<img width="1918" height="977" alt="Learning Roadmap" src="https://github.com/user-attachments/assets/c19f0a55-e0ba-429a-9cea-4ed4627383ff" />

---

<a id="future-improvements"></a>
## 🔮 Future Improvements

- [ ] 🤖 Machine Learning–based career prediction (beyond rule-based scoring)
- [ ] 💬 AI Career Mentor Chatbot for interactive guidance
- [ ] 📊 Resume Score Analysis
- [ ] 💼 Internship Recommendation System
- [ ] 📄 Downloadable PDF Career Report generation
- [ ] 🔐 User Authentication & saved profiles
- [ ] 🗄️ Database Integration (replacing static JSON storage)

---

## 👤 Author

**Abhinav Jha**
B.Tech Computer Science & Engineering
Jaypee University of Information Technology, Solan

---

<a id="license"></a>
## 📜 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Abhinav Jha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

⭐ If you found this project useful, consider giving it a star on GitHub!

</div>
