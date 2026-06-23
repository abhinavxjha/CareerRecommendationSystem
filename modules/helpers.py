import json


#######################################
#SKILL GAP ANALYSIS & READINESS SCORE
#######################################


def load_json(filename):
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

def career_selection():
    career=input("Which Career You Want To Opt :: ")
    return career

def skills_input():
    skills=input("Enter Your Skills :: ")
    user_skills=skills.split()
    return user_skills


#######################################
#COURSE RECOMMENDATION
#######################################


def course_recommendation(final_missing_skills, courses_data):
    recommended_courses=[]
    for course in courses_data:
        if course['skill'] in final_missing_skills:
            recommended_courses.append(course)
    return recommended_courses
    
def values(required_skills_data, selected_career, user_skills):
    required_skills = get_required_skills(required_skills_data, selected_career)
    missing_skills=list(set(required_skills)-set(user_skills))
    final_missing_skills=sorted(missing_skills)
    return final_missing_skills
    

#######################################
#CAREER MATCHING
#######################################


def calculate_match_percentage(career_skills,  user_skills):
    match=len(set(career_skills).intersection(set(user_skills)))
    total=len(career_skills)
    score=(match/total)*100
    return score

def matching_score(required_skills_data, user_skills):
    career_score=[]
    for skill in required_skills_data:
        career_name=skill['career']
        career_skills=skill['skills']
        score=calculate_match_percentage(career_skills, user_skills)
        career_score.append((career_name, score))
    return career_score


#######################################
#CAREER COMPARISON
#######################################


def get_career_info(career_info_data, career_name):
    for ccareer in career_info_data:
        if ccareer["career"]==career_name:
            return ccareer
    return None

def load_career(filename):
    with open(filename,"r") as f:
        career_info_data=json.load(f)
        return career_info_data