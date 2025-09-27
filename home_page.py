import streamlit as st
import pandas as pd


# ---- PAGE CONFIG ----
st.set_page_config(page_title="SMART-BUDGETING-APP", layout="wide",)

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
