import streamlit as st
import pandas as pd
from user_pages import user1, user2, user3


# ---- PAGE CONFIG ----
st.set_page_config(page_title="Dropdown Navigation", page_icon="📑", layout="wide")

# Keep track of selection
if "page" not in st.session_state:
    st.session_state.page = "Home"

page = st.selectbox("Go to page:", ["Home", "About", "Contact"], index=["Home","About","Contact"].index(st.session_state.page))

st.session_state.page = page

# Load the right page
if st.session_state.page == "User1":
    user1
elif st.session_state.page == "User2":
    user2
elif st.session_state.page == "User3":
    user3


# ---- HEADER ----
st.title("🚀 Welcome to My App")
st.subheader("A streamlined landing page built with Streamlit")

# ---- HERO SECTION ----
st.markdown(
    """
    ### Why you'll love this:
    - ✅ Budgetting App  
    - ✅ Save Money
    - ✅ Spend more Money 
    """
)

# ---- CALL TO ACTION ----
st.markdown("---")
st.header("Get Started Today!")

name = st.text_input("Enter your name:")
email = st.text_input("Enter your email:")

if st.button("Sign Up"):
    if name and email:
        st.success(f"Thanks {name}! We'll reach out at {email}.")
    else:
        st.error("Please enter both your name and email.")

# ---- FOOTER ----
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
