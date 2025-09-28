import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Finn - Smart Budgeting",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
with open('styles_landing.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Main content container
st.markdown("""
<div class="main-container">
    <div class="accent-dot top-left"></div>
    <div class="accent-dot top-right"></div>
    <div class="accent-dot bottom-left"></div>
    <div class="accent-dot bottom-right"></div>
    
    <div class="company-name">Finn</div>
    <div class="tagline">Smart Budgeting, Simplified</div>
    
    <div class="description">
        We provide a budgeting system with an integrated AI-chatbot to help personalize your budgeting experience compared to a bland Excel file.
    </div>
</div>
""", unsafe_allow_html=True)

# Create some space and add the button
st.markdown("<br>", unsafe_allow_html=True)

# Center the button and handle navigation
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("Get Started", key="get_started_button"):
        st.switch_page("home_page.py")

st.markdown("<br><br>", unsafe_allow_html=True)