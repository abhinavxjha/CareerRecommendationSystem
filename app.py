"""Legacy Streamlit implementation retained for reference only.

The Flask application begins after this block.
"""

LEGACY_STREAMLIT_SOURCE = r'''
##################################################
#                   IMPORTS                      #
##################################################


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit as st
import plotly.graph_objects as go
from modules.helpers import (
    load_skills,
    career_selection,
    course_recommendation,
    skills_input,
    load_career,
    load_courses,
    matching_score,
    skill_gap_analysis,
    readiness_score,
    fcourse_recommend,
    get_required_skills,
    roadmap_generator,
    final_roadmap,
    get_career_info,
    career_comparison,
    career_comparison_table,
    resume_input,
    text_from_pdf,
    skills_list,
    extract_skills,
    career_matching
)

required_skills_data = load_skills("data/careers.json")
courses_data = load_courses("data/courses.json")
career_info_data = load_career("data/career_info.json")
skills_data=load_skills("data/skills.json")


##################################################
#                     TITLE                      #
##################################################


st.set_page_config(
    page_title="Career Recommendation System",
    page_icon="🎯",
    layout="wide"
)

st.markdown(
"<h1 style='text-align: center; margin-top: -25px; margin-bottom: 50px;' id='#skill-gap'>CAREER RECOMMENDATION SYSTEM</h1>",
unsafe_allow_html=True, 
)


##################################################
#                 SKILLS INPUT                   #
##################################################


user_skills = []
uploaded_file = None
col2, col3 = st.columns(2)
with col2:
        with st.container(height=300,border=True):

            st.subheader("Upload Resume or Enter Skills")
            input_method=st.radio("Choose Input Method", ["Manual Skills", "Resume Upload"])

            if input_method == "Manual Skills":
                skills = st.text_area("Enter Your Skills", placeholder="Enter skills separated by commas.\nExample:\nPython, SQL, Pandas, NumPy, Machine Learning")
                user_skills = [ skill.strip() for skill in skills.split(",") if skill.strip()]
                if user_skills:
                    st.success("Skills Entered Successfully")
                         
            elif input_method == "Resume Upload":
                uploaded_file=st.file_uploader("Upload Resume", type=["pdf"], max_upload_size=10, accept_multiple_files=False)
                if uploaded_file:
                    resume_text = text_from_pdf(uploaded_file)
                    all_skills = skills_list(skills_data)
                    user_skills = extract_skills(resume_text, all_skills)



##################################################
#                 CAREER INPUT                   #
##################################################


with col3:
        with st.container(height=300, border=True):

            st.subheader("Which Career You Want to Opt?")
            st.write("")
            career_names=[]
            for career in required_skills_data:
                career_names.append(career['career'])
            selected_career=st.selectbox("Select Your Target Career", career_names, index=None)

            if selected_career:
                st.success(f"Your Selected Career is {selected_career}")
            analyze=st.button("Analyze", use_container_width=True)
st.divider()


##################################################
#              SKILL GAP ANALYSIS                #
##################################################


if analyze:
    try:
        errors = []

        if input_method == "Resume Upload":
            if uploaded_file is None:
                errors.append("Upload your resume.")
            elif len(user_skills) == 0:
                st.warning("No relevant technical skills were found in this resume. Please upload a valid resume or enter skills manually.")
                st.stop()

        if input_method == "Manual Skills" and not user_skills:
            errors.append("Enter your skills.")

        if selected_career is None:
            errors.append("Select your target career.")

        if errors:
            st.warning("Please complete the following before analyzing:\n\n" + "\n".join(f"- {e}" for e in errors))

        else:
            st.markdown(
            "<h2 style='text-align: center;' id='#skill-gap'>RESULTS</h2>",
            unsafe_allow_html=True, 
            )

            st.divider()

            missing_skills=skill_gap_analysis(required_skills_data, selected_career, user_skills)
            col1, col2, col3 = st.columns(3)
            with col1:
                with st.container(height=470,border=True):

                    st.markdown(
                    "<h3 style='text-align: center;' id='home'>SKILL GAP ANALYSIS</h3>",
                    unsafe_allow_html=True)

                    for skill in missing_skills:
                            st.write(f"• {skill}")

                    st.divider()


##################################################
#             CAREER READINESS SCORE             #
##################################################
        

            with col2:
                with st.container(height=470,border=True):

                    career_readiness_score=readiness_score(required_skills_data, selected_career, user_skills)

                    st.markdown(
                    "<h3 style='text-align: center;'>CAREER READINESS SCORE</h3>",
                    unsafe_allow_html=True)

                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=career_readiness_score,
                        gauge={"axis": {"range": [0, 100]}}
                        )
                    )

                    st.plotly_chart(fig)
                        
                    if career_readiness_score >= 80:
                        st.success("Excellent readiness for this career!")
                    elif career_readiness_score >= 50:
                        st.warning("You are on the right track. Keep learning.")
                    else:
                        st.error("Significant skill gaps detected.")
                    st.divider()


##################################################
#              TOP 5 MATCHED CAREER              #
##################################################


            with col3:
                with st.container(height=470, border=True):

                    results = matching_score(required_skills_data, user_skills)
                    rec_career=career_matching(results)

                    st.markdown(
                    "<h3 style='text-align: center;'>TOP 5 MATCHED CAREER</h3>",
                    unsafe_allow_html=True)

                    df=pd.DataFrame(rec_career, columns=["Rank","Career","Match Score"])

                    plt.figure(figsize=(4,4), facecolor="#0E1117")
                    ax = plt.gca()              
                    ax.set_facecolor("#0E1117") 
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)                
                    plt.barh(df["Career"], df["Match Score"])
                    plt.xlabel("Match Score (%)", color="white")
                    plt.ylabel("", color="white")
                    plt.xticks(color="white")
                    plt.yticks(color="white")
                    st.pyplot(plt)


##################################################
#                 CAREER INSIGHTS                #
##################################################


            col2, col3 = st.columns(2)
            with col2:
                with st.container(height=445,border=True):
                    st.markdown(
                    "<h3 style='text-align: center;'>MATCHED CAREER INSIGHTS</h3>",
                    unsafe_allow_html=True)

                    get_career_info(career_info_data, selected_career)
                    comp_rows=career_comparison(results, career_info_data)
                    df3=career_comparison_table(comp_rows)
                    df3=df3.iloc[0:5]
                    df3["Learning Time"]=(
                    df3["Learning Time"]
                    .str.replace(" Months", "", regex=False)
                    .astype(int)
                    )

                    def convert_time(time):                         #helped by ai
                        if "Months" in time:
                            return int(time.replace(" Months", ""))
                        elif "Years" in time:
                            return int(time.replace(" Years", "")) * 12
                        df3["Learning Time"] = df3["Learning Time"].apply(convert_time)    


                    career_labels = [name[:12] + "..." if len(name) > 12 else name for name in df3["Career"]]


        #matplotlib
    #------graph colors--------

                    plt.figure(figsize=(8,4), facecolor="#0E1117")
                    colors=[]
                    for i in df3["Difficulty"]:
                        if i=="Low":
                            colors.append("green")
                        elif i=="Medium":
                            colors.append("gold")
                        elif i=="High":
                            colors.append("orange")
                        else:
                            colors.append("red")

    #------graph lines-------

                    ax = plt.gca()              
                    ax.set_facecolor("#0E1117") 
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)     

    #-------for graph--------

                    plt.bar(career_labels, df3["Learning Time"], color=colors)
                    plt.xlabel("Career", color="white")
                    plt.ylabel("Learning Time (Months)", color="white")
                    plt.xticks(color="white")
                    plt.yticks(color="white")
                    plt.tight_layout()

    #-------for legend--------

                    low = mpatches.Patch(color="green", label="Low")
                    medium = mpatches.Patch(color="gold", label="Medium")
                    high = mpatches.Patch(color="orange", label="High")
                    very_high = mpatches.Patch(color="red", label="Very High")
                    plt.legend(
                        handles=[low, medium, high, very_high],
                        loc="upper right",
                        facecolor="#0E1117",
                        edgecolor="#0E1117",
                        labelcolor="white"
                    )
                    st.pyplot(plt)
                    

            with col3:
                with st.container(height=445, border=True):
                    st.markdown(f"""
                    <div style="
                    text-align:center;
                    padding:15px;
                    border:1px;
                    border-radius:10px;
                    ">
                    <h3 style="margin:0;">BEST CAREER MATCH</h3>
                    <h1 style="margin:50px 0;">{df3.iloc[0]["Career"]}</h1>
                    <h3 style="color:#22c55e;">{df3.iloc[0]["Match Score"]:.2f}% Match</h3>
                    </div>
        """, unsafe_allow_html=True)


##################################################
#             COURSE RECOMMENDATION              #
##################################################


            st.write("")
            st.write("")
            st.markdown(
            "<h3 style='text-align: center;'>RECOMMENDED COURSES</h3>",
            unsafe_allow_html=True)

            required_skills=get_required_skills(required_skills_data, selected_career)
            courses=course_recommendation(missing_skills, courses_data)
            recommend_courses=fcourse_recommend(missing_skills, courses_data)
            df2=pd.DataFrame(recommend_courses, columns=["Skills","Course","Provider","Link"])
            if len(df2) == 0:
                st.info("No courses found.")
            else:
                st.dataframe(df2, hide_index=True, use_container_width=True, column_config={
                    "Link": st.column_config.LinkColumn(
                        "Course Link",
                        display_text="Open Course 🔗",
                        width="small"
                    )
                    }
                )


##################################################
#                    ROADMAP                     #
##################################################


            st.write("")
            st.write("")
            st.markdown(
            "<h3 style='text-align: center;'>ROADMAP</h3>",
            unsafe_allow_html=True)

            mskills=skill_gap_analysis(required_skills_data, selected_career, user_skills)
            courses=course_recommendation(mskills, courses_data)
            roadmap_generator(mskills, courses)
            columns = st.columns(min(len(mskills), 5))
            
            for i, col in enumerate(columns):
                with col:
                    with st.container(height=175, border=True):
                        st.markdown(f"#### 📅 Month {i+1}")
                        st.write("")
                        st.success(mskills[i])


##################################################
#                   exception                    #
##################################################                
    except Exception:
        st.error("Unable to analyze this document. Please upload a valid resume PDF.")
        st.stop()
'''

"""Web server for the Career Recommendation System.

Run ``python app.py`` and open http://127.0.0.1:5000.
"""

import json
from pathlib import Path

import pdfplumber
from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


def load_json(filename: str):
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


CAREERS = load_json("careers.json")
COURSES = load_json("courses.json")
CAREER_INFO = load_json("career_info.json")
SKILLS_DATA = load_json("skills.json")
CAREERS_BY_NAME = {item["career"]: item["skills"] for item in CAREERS}
CAREER_INFO_BY_NAME = {item["career"]: item for item in CAREER_INFO}
ALL_SKILLS = [skill for group in SKILLS_DATA.values() for skill in group]


def normalise(value: str) -> str:
    return " ".join(value.strip().lower().split())


def unique_skills(skills: list[str]) -> list[str]:
    seen, result = set(), []
    for skill in skills:
        cleaned = skill.strip()
        if cleaned and normalise(cleaned) not in seen:
            seen.add(normalise(cleaned))
            result.append(cleaned)
    return result


def score_careers(user_skills: list[str]) -> list[dict]:
    user_set = {normalise(skill) for skill in user_skills}
    results = []
    for career, required in CAREERS_BY_NAME.items():
        matched = [skill for skill in required if normalise(skill) in user_set]
        score = round(100 * len(matched) / len(required), 2) if required else 0
        results.append({"career": career, "skills": required, "matched_skills": matched, "score": score})
    return sorted(results, key=lambda item: item["score"], reverse=True)


def build_analysis(user_skills: list[str], target_career: str) -> dict:
    if target_career not in CAREERS_BY_NAME:
        raise ValueError("Please select a valid target career.")
    scores = score_careers(user_skills)
    target = next(item for item in scores if item["career"] == target_career)
    matched = {normalise(skill) for skill in target["matched_skills"]}
    missing = sorted((skill for skill in target["skills"] if normalise(skill) not in matched), key=str.lower)
    top_matches = [
        {"rank": rank, "career": item["career"], "score": item["score"]}
        for rank, item in enumerate((item for item in scores if item["score"] > 0), start=1)
    ][:5]
    insights = [{**item, **{key: value for key, value in CAREER_INFO_BY_NAME.get(item["career"], {}).items() if key != "career"}} for item in top_matches]
    missing_set = {normalise(skill) for skill in missing}
    courses = [course for course in COURSES if normalise(course["skill"]) in missing_set]
    return {
        "user_skills": user_skills, "target_career": target_career,
        "readiness_score": target["score"], "matched_skills": target["matched_skills"],
        "missing_skills": missing, "top_matches": top_matches,
        "best_match": top_matches[0] if top_matches else None,
        "career_insights": insights, "recommended_courses": courses,
        "roadmap": [{"month": month, "skill": skill} for month, skill in enumerate(missing[:5], start=1)],
    }


def skills_from_resume(resume) -> list[str]:
    text = ""
    with pdfplumber.open(resume) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    lowered = text.lower()
    return unique_skills([skill for skill in ALL_SKILLS if normalise(skill) in lowered])


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/api/careers")
def careers():
    return jsonify({"careers": sorted(CAREERS_BY_NAME)})


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    skills = payload.get("skills", [])
    if not isinstance(skills, list):
        return jsonify({"error": "Skills must be sent as a list."}), 400
    skills = unique_skills(skills)
    if not skills:
        return jsonify({"error": "Enter at least one skill before analyzing."}), 400
    try:
        return jsonify(build_analysis(skills, payload.get("target_career", "")))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.post("/api/resume-skills")
def resume_skills():
    resume = request.files.get("resume")
    if not resume or not resume.filename:
        return jsonify({"error": "Upload a PDF resume."}), 400
    if not resume.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF resumes are supported."}), 400
    try:
        return jsonify({"skills": skills_from_resume(resume)})
    except Exception:
        return jsonify({"error": "Unable to read this PDF. Upload a valid text-based resume."}), 400


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"error": "Resume size must be 10 MB or smaller."}), 413


if __name__ == "__main__":
    app.run(debug=True)
