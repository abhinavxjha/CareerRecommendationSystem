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


outer = st.container(border=True)
with outer:
    col2, col3 = st.columns(2)
    with col2:
        with st.container(height=300,border=True):

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
                    #st.success("Resume Uploaded")
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
            analyze=st.button("Analyze")


##################################################
#              SKILL GAP ANALYSIS                #
##################################################


if analyze:
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
#                MATCHING CAREER                 #
##################################################


    with col3:
        with st.container(height=470, border=True):

            results = matching_score(required_skills_data, user_skills)
            rec_career=career_matching(results)

            st.markdown(
            "<h3 style='text-align: center;'>TOP 5 MATCHED CAREER</h3>",
            unsafe_allow_html=True)

            df=pd.DataFrame(rec_career, columns=["Rank","Career","Match Score"])
            st.bar_chart(df, x="Career", y="Match Score", )



##################################################
#               CAREER COMPARISON                #
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
            df3["Learning Time"] = (
            df3["Learning Time"]
            .str.replace(" Months", "", regex=False)
            .astype(int)
            )
            st.bar_chart(df3, x="Career", y="Learning Time")
        
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