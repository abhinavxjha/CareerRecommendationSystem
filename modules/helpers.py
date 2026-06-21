import json

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
    