##################################################
#                   IMPORTS                      #
##################################################


import pandas as pd
import matplotlib.pyplot as plt
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
from modules.helpers import *

required_skills_data = load_skills("data/careers.json")
courses_data = load_courses("data/courses.json")
career_info_data = load_career("data/career_info.json")
skills_data=load_skills("data/skills.json")

##################################################
#                     TITLE                      #
##################################################


st.markdown(
"<h1 style='text-align: center;' id='#skill-gap'>CAREER RECOMMENDATION SYSTEM</h1>",
unsafe_allow_html=True, 
)



##################################################
#                 SKILLS INPUT                   #
##################################################


st.subheader("Upload Resume or Enter Skills")
input_method=st.radio("Choose Input Method", ["Manual Skills", "Resume Upload"])

if input_method == "Manual Skills":
    skills=st.text_area("Enter Your Skills")
    if skills:
        user_skills = [ skill.strip() for skill in skills.split(",") if skill.strip()]
        st.success("Skills Entered Successfully")
        
elif input_method == "Resume Upload":
    uploaded_file=st.file_uploader("Upload Resume", type=["pdf"], max_upload_size=10, accept_multiple_files=False)
    if uploaded_file:
        st.success("Resume Uploaded")
        resume_text = text_from_pdf(uploaded_file)
        all_skills = skills_list(skills_data)
        user_skills = extract_skills(resume_text, all_skills)



##################################################
#                 CAREER INPUT                   #
##################################################


st.subheader("Which Career You Want to Opt?")
career_names=[]
for career in required_skills_data:
    career_names.append(career['career'])
selected_career=st.selectbox("Select Your Target Career", career_names, index=None)
if selected_career:
    st.success(f"Your Selected Career is {selected_career}")


##################################################
#              SKILL GAP ANALYSIS                #
##################################################


if st.button("Analyze"):
    missing_skills=skill_gap_analysis(required_skills_data, selected_career, user_skills)

    st.markdown(
    "<h2 style='text-align: center;' id='home'>SKILL GAP ANALYSIS</h2>",
    unsafe_allow_html=True)

    with st.expander("View Missing Skills"):
        for skill in missing_skills:
            st.write(f"• {skill}")

    st.divider()
##################################################
#             CAREER READINESS SCORE             #
##################################################


    career_readiness_score=readiness_score(required_skills_data, selected_career, user_skills)

    st.markdown(
    "<h2 style='text-align: center;'>CAREER READINESS SCORE</h2>",
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
#                MATCHING CAREER                 #
##################################################

    results = matching_score(required_skills_data, user_skills)
    rec_career=career_matching(results)

    st.markdown(
    "<h2 style='text-align: center;'>TOP 5 MATCHED CAREER</h2>",
    unsafe_allow_html=True)

    
    df=pd.DataFrame(rec_career, columns=["Rank","Career","Match Score"])
    st.bar_chart(df, x="Career", y="Match Score")
    st.divider()

    ##################################################
    #             COURSE RECOMMENDATION              #
    ##################################################

    st.markdown(
    "<h2 style='text-align: center;'>RECOMMENDED COURSES</h2>",
    unsafe_allow_html=True)

    required_skills=get_required_skills(required_skills_data, selected_career)
    courses=course_recommendation(missing_skills, courses_data)
    recommend_courses=fcourse_recommend(required_skills, courses_data)

    for skill, course, provider, link in recommend_courses:
        df2=pd.DataFrame(recommend_courses, columns=["Skills","Course","Provider","Link"])
    st.dataframe(df2, hide_index=True, use_container_width=True, column_config={
        "Link": st.column_config.LinkColumn(
            "Course Link",
            display_text="Open Course 🔗",
            width="small"
        )
        }
    )



