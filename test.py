import streamlit as st

# --- Hardcoded credentials (replace with secure store later) ---
USER_CREDENTIALS = {
    "admin": "password123",
    "avik": "gt2025",
    "guest": "welcome"
}

# Initialize session state for auth
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- Login form if not authenticated ---
if not st.session_state["authenticated"]:
    st.title("🔐 Login Page")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.success(f"✅ Welcome, {username}!")
            st.rerun()  # refresh so login form disappears
        else:
            st.error("❌ Invalid username or password")

# --- Main content if authenticated ---
else:
    st.sidebar.success("You are logged in ✅")
    st.title("My App Content")

    # 👇 replace this with your existing app code
    st.write("Here is the content of the app that only shows after login.")
    
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
