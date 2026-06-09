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

