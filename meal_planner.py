import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
import re
import json

load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))

def calculate_calories (height, weight, age, gender, activity_level, goal):
    # Implements 
    if gender == "Male":
        bmr = 13.397 * weight + 4.799 *height - 5.677 * age + 88.362
    else:
        bmr = 9.247 * weight+ 3.098 * height - 4.330 * age  + 447.593
    
    activity_factors = {
        "Sedentary: little or no exercise": 1.2,
        "Light: exercise 1-3 times/week": 1.375,
        "Moderate: exercise 4-5 times/week": 1.55,
        "Active: daily exercise": 1.725,
        "Very Active: very intense exercise daily": 1.9
    }
    
    tdee = bmr * activity_factors[activity_level]
    
    match goal:
        case "Maintain Weight": 
            calories = tdee
        case "Weight loss":
            calories = tdee * 0.83
        case "Extreme weight loss":
            calories = tdee * 0.65
        case "Gain Weight":
            calories = tdee * 1.17
        case "Fast Weight gain":
            calories = tdee * 1.35

    return int(calories)

def meal_planner():
        st.sidebar.header("Your Information")
        age = st.sidebar.number_input("Age *", 9, 80, 18)
        gender = st.sidebar.selectbox("Gender *", ["Male", "Female"])
        height = st.sidebar.slider("Height (cm) *", min_value=100, max_value=250
                                , step=1, value=180)
        weight = st.sidebar.slider("Weight (kg) *", min_value=30, max_value=150, step=1, value=84)
        protien_goal = st.sidebar.number_input("Protien Goal (g)", 50, 250, weight)
        activity_level = st.sidebar.selectbox("Activity Level *", 
                                ["Sedentary: little or no exercise",
                                "Light: exercise 1-3 times/week", 
                                "Moderate: exercise 4-5 times/week",
                                "Active: daily exercise",
                                "Very Active: very intense exercise daily"])

        goal = st.sidebar.selectbox("Goal", ["Maintain Weight", "Weight loss","Extreme weight loss", "Gain Weight","Fast Weight gain"])
        
        # Additional preferences
        st.sidebar.header("Dietary Preferences")
        diet_type = st.sidebar.multiselect("Diet Type", ["Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean", "No Preference"])
        allergies = st.sidebar.text_input("Allergies/Restrictions")
        medical_conditions = st.sidebar.text_input("medical conditions")
        favorite_foods = st.sidebar.text_input("Additonal Preferences")

        st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: center;
        }
        .spinner-container {
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255,255,255,0.7);
            z-index: 9999;
        }
        </style>
        """, unsafe_allow_html=True)


        tab_titles = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
        tabs = st.tabs(tab_titles)
        st.write("")
        


        if st.button("Generate Meal Plan"):
            spinner_container = st.empty()
            with spinner_container.container():
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    with st_lottie_spinner(logo, key="meal_plan_spinner", height=400, width=400,loop= True,speed= 0.1):
                        # Calculate calories
                        calories = calculate_calories(height, weight, age, gender, activity_level, goal)
                        
                        # Generate meal plan
                        response  = generate_meal_plan(calories, protien_goal, diet_type, allergies, medical_conditions, favorite_foods)
                        
                        # Split the text into days
                        days_data = re.split(r'\^(\w+)', response)[1:]  # Skip the first empty string

                        
                        # Create a dictionary to store the meal plans
                        meal_plan = {}

                        st.write(meal_plan)

                        # Iterate through the split data and create key-value pairs
                        for i in range(0, len(days_data), 2):
                            day = days_data[i].upper()
                            plan = days_data[i+1].strip()
                            meal_plan[day] = plan
                    
            spinner_container.empty()

            for tab, day in zip(tabs, tab_titles):
                with tab:
                    plan = meal_plan.get(day, "")
                    if plan:
                        st.write(plan)
                    else:
                        st.write(f"Couldn't generate meal plan for {day}. Please generate the Meal Plan again.")

            

def load_lottiefile(filepath:str):
        with open(filepath,"r") as f:
            return json.load(f)

logo = load_lottiefile("assets/spinner.json")


def generate_meal_plan(calories, protien_goal, diet_type, allergies, medical_conditions, favorite_foods):
    prompt = prompt = f"""
    Generate a 7-day personalized meal plan for someone As a professional nutritionist with the following details given about the patient:
    - Daily calorie target: {calories} calories
    - Protein Goal: {protien_goal} grams
    - Diet type: {', '.join(diet_type) if diet_type else 'No specific preference'}
    - Allergies: {allergies if allergies else 'None'}
    - Medical Conditions: {medical_conditions if medical_conditions else 'None'}
    - Additonal Preferences: {favorite_foods if favorite_foods else 'No specific preferences'}


    For each day, provide a structured meal plan in the following format:

    ^DAY_NAME('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')\n

    Breakfast:
    - Meal: [Meal Name]
    - Calories: [Calorie Count]
    - Protein: [Protein Amount] g
    - Recipe: [Brief recipe or preparation instructions]

    Lunch:
    - Meal: [Meal Name]
    - Calories: [Calorie Count]
    - Protein: [Protein Amount] g
    - Recipe: [Brief recipe or preparation instructions]

    Dinner:
    - Meal: [Meal Name]
    - Calories: [Calorie Count]
    - Protein: [Protein Amount] g
    - Recipe: [Brief recipe or preparation instructions]

    Snacks:
    - Snack 1: [Snack Name] ([Calorie Count] calories, [Protein Amount] g protein)

    Total:
    - Calories: [Total Calories for the Day]
    - Protein: [Total Protein for the Day] g

    Repeat this structure for all 7 days ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'). Ensure each day starts with '^DAY_NAME' (e.g., ^MONDAY).
    Adhere to the specified calorie target, protein goal, diet type, and account for allergies, medical conditions, and favorite foods.
    """


    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

