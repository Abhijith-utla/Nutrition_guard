
import streamlit as st
import base64


def show_home_screen():

    st.markdown("<h1 style='text-align: center;'>Nutrition Guard 🥗</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Your Personalized Nutrition Companion</h3>", unsafe_allow_html=True)


    st.divider()

    # Feature Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🧬 Personalized Profiles</h3>
        <p>Create a unique nutrition profile based on:</p>
        <ul>
            <li>Height & Weight</li>
            <li>Age & Sex</li>
            <li>Activity Level</li>
            <li>Diet Preferences</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>📊 Smart Meal Planning</h3>
        <p>Get weekly meal plans that:</p>
        <ul>
            <li>Match your health goals</li>
            <li>Consider dietary restrictions</li>
            <li>Optimize nutrition intake</li>
            <li>Easy to follow</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>💬 NutriChat AI</h3>
        <p>Interactive nutrition advisor that:</p>
        <ul>
            <li>Answers nutrition questions</li>
            <li>Provides personalized advice</li>
            <li>Supports your health journey</li>
            <li>Available 24/7</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()


    # How to Use Section
    st.header("🚀 How to Use Nutrition Guard")
    
    steps_col1, steps_col2, steps_col3 = st.columns(3)
    
    with steps_col1:
        st.markdown("""
        1. **Create Profile**
           - Input personal health metrics
           - Select dietary preferences""")
    
    with steps_col2:
        st.markdown("""
        2. **Generate Meal Plan**
           - Click "Generate Plan"
           - Review personalized recommendations
        """)
    
    with steps_col3:
        st.markdown("""
        3. **Explore NutriChat**
           - Ask nutrition questions
           - Get instant AI-powered advice
        
        """)


    # # API Key Input
    # st.header("🔑 Gemini API Key Setup")
    # api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    # if api_key:
    #     st.success("API Key successfully configured!")
    #     st.session_state['gemini_api_key'] = api_key

