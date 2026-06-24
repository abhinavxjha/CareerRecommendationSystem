import json
import pandas as pd    
import numpy as np
import pdfplumber as pf

#######################################
#          INPUT FUNCTIONS            #
#######################################


def load_skills(filename):
    with open(filename,"r") as f:
        required_skills_data=json.load(f)
        return required_skills_data


def get_required_skills(required_skills_data, selected_career):
    for career in required_skills_data:
        if career['career'] == selected_career:
            return career['skills']
    return []


def load_courses(filename):
    with open(filename,"r") as f:
        courses=json.load(f)
        return courses
    

def load_career(filename):
    with open(filename,"r") as f:
        career_info_data=json.load(f)
        return career_info_data


def career_selection():
    career=input("Which Career You Want To Opt :: ")
    return career


def skills_input():
    skills=input("Enter Your Skills :: ")
    user_skills=skills.split()
    return user_skills


##################################################
#   SKILL GAP ANALYSIS & COURSE RECOMMENDATION   #
##################################################


def skill_gap_analysis(required_skills_data, selected_career, user_skills):
    required_skills = get_required_skills(required_skills_data, selected_career)
    missing_skills=list(set(required_skills)-set(user_skills))
    final_missing_skills=sorted(missing_skills)
    return final_missing_skills


##################################################
#               READINESS SCORE                  #
##################################################


def readiness_score(required_skills_data, selected_career, user_skills):
    required_skills = get_required_skills(required_skills_data, selected_career)
    total=len(required_skills)
    have=len(set(required_skills).intersection(set(user_skills)))
    score=(have/total)*100 
    print("You are",score,"% ready to become",selected_career)


##################################################
#               CAREER MATCHING                  #
##################################################

def career_matching(results):
    filtered_results = [(career, score) for career, score in results if score > 0 ]
    scores = np.array([score for career, score in filtered_results])
    ranking = np.argsort(scores)[::-1]
    rank = 1
    for index in ranking[:5]:
        career_name = filtered_results[index][0]
        score = filtered_results[index][1]
        print(f"{rank}. {career_name} : {score:.2f}%")
        rank += 1


##################################################
#             COURSE RECOMMENDATION              #
##################################################


def course_recommendation(final_missing_skills, courses_data):
    recommended_courses=[]
    for course in courses_data:
        if course['skill'] in final_missing_skills:
            recommended_courses.append(course)
    return recommended_courses


def fcourse_recommend(required_skills, courses_data):
    courses=course_recommendation(required_skills, courses_data)
    print("RECOMMENDED COURSES FOR YOUR MISSING SKILL","\n")
    for course in courses:
        print("Skill :", course["skill"])
        print("Course :", course["course"])
        print("Provider :", course["provider"])
        print("Link :", course["link"])
        print("-" * 50)


def get_required_skills(required_skills_data, selected_career):
    for career in required_skills_data:
        if career['career'] == selected_career:
            return career['skills']
    return []


##################################################
#               ROADMAP GENERATOR                #
##################################################


def roadmap_generator(mskills, courses):
    roadmap={}
    for month, skill in enumerate(mskills, start=1):
        roadmap[f"Month {month}"]={"skill":skill}
        if month==3:
            break
    return roadmap


def final_roadmap(mskills, courses):
    frmap=roadmap_generator(mskills, courses)
    for i,j in frmap.items():
        print(i ,"-", j)
        print("-" * 50)


##################################################
#               CAREER COMPARISON                #
##################################################


def get_career_info(career_info_data, career_name):
    for ccareer in career_info_data:
        if ccareer["career"]==career_name:
            return ccareer
    return None


def matching_score(required_skills_data, user_skills):
    career_score=[]
    for skill in required_skills_data:
        career_name=skill['career']
        career_skills=skill['skills']
        score=calculate_match_percentage(career_skills, user_skills)
        career_score.append((career_name, score))
    return career_score


def career_comparison(results, career_file):
    comparison_rows=[]
    for career,score in results:
        info=get_career_info(career_file, career)
        if score > 0:
            if info is None:
                continue
            row = {"Career": career, "Match Score": score, "Difficulty": info["difficulty"], "Learning Time": info["learning_time"]}
            comparison_rows.append(row)
    return comparison_rows


def calculate_match_percentage(career_skills,  user_skills):
    match=len(set(career_skills).intersection(set(user_skills)))
    total=len(career_skills)
    score=(match/total)*100
    return score


def career_comparison_table(comp_rows):
    df=pd.DataFrame(comp_rows)
    df["Match Score"] = df["Match Score"].round(2)
    df=df.sort_values(by="Match Score", ascending=False)
    return df


##################################################
#                  RESUME PARSER                 #
##################################################


def resume_input():
    filename = input("Enter Resume PDF Path : ")
    return filename


def text_from_pdf(filename):    
    with pf.open(filename) as pdf:
        text=""
        for i in pdf.pages:
            page_text=i.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def skills_list(skills_data):
    all_skills=[]
    for category in skills_data:
        all_skills.extend(skills_data[category])
    return all_skills


def extract_skills(filename, all_skills):
    common_skills=[]
    for skill in all_skills:
        if skill.lower() in filename.lower():
            common_skills.append(skill)
    return common_skills