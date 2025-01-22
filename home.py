import streamlit as st
from display_home import show_home_screen 
from meal_planner import meal_planner
from streamlit_option_menu import option_menu
from rag_functions import nutri_chat_setup, initialize_nutrichat

st.set_page_config(page_title="Personalized Meal Planner", layout="wide")

def main():
    if not st.session_state.nutrichat_initialized:
        initialize_nutrichat()

    # Horizontal navigation menu
    selected = option_menu(
        menu_title=None,
        options=["Home", "Meal Planner", "NutriChat"],
        icons=["house", "book", "chat-dots"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Home":
        show_home_screen()
        st.logo("/Users/abhijithutla/projects/AIMD_nutritionguard/assets/logo.jpg",size="large")
        

    elif selected == "Meal Planner":
        st.divider()
        meal_planner()

    elif selected == "NutriChat":
        st.divider()
        nutri_chat_setup()



if __name__ == "__main__":
    main()


