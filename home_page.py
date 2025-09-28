import streamlit as st
import plotly.express as px
import pandas as pd
from get_transactions import fetch_trans

# --- Hardcoded credentials ---
USER_CREDENTIALS = {
    "admin": "password123",
    "avik": "gt2025",
    "guest": "welcome"
}

# Page configuration
st.set_page_config(
    page_title="Finn - Smart Budgeting",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize session state ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- Load CSS ---
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"⚠️ CSS file '{file_name}' not found.")

# --- Unauthenticated: Landing + Login ---
if not st.session_state.authenticated:
    load_css("styles.css")  # Combined landing + login styles

    # Landing container
    st.markdown("""
    <div style="text-align:center;">
        <h1 class="company-name">Finn</h1>
        <h3 class="tagline">Smart Budgeting, Simplified</h3>
        <p class="description">
            We provide a budgeting system with an integrated AI-chatbot 
            to help personalize your budgeting experience compared to a bland Excel file.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Login form (simplified without glossy container)
    st.subheader("🔐 Login to Continue")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --- Authenticated: Dashboard ---
else:
    load_css("styles.css")

    st.sidebar.success("You are logged in ✅")
    st.markdown("""
<div class="header-container">
    <div class="custom-title">Smart Budgeting Assistant</div>
    <div class="subtitle">AI-powered financial insights with Capital One integration</div>
</div>
    """, unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("$2,450", "Monthly Budget"),
        ("$1,890", "Spent This Month"),
        ("$560", "Remaining Budget"),
        ("23%", "Budget Remaining")
    ]
    for col, (value, label) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f'<div class="metric-card"><h3>{value}</h3><p>{label}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Transactions
    df = pd.DataFrame(fetch_trans(2))
    df['category'] = df['description'].fillna('').str.split().str[0]
    df['date'] = pd.to_datetime(df['purchase_date'])
    df = df.sort_values(by='date', ascending=False)

    logs_html = []
    for _, row in df.iterrows():
        date_str = row['date'].strftime("%m/%d/%y")
        amount = row['amount']
        logs_html.append(
            f"<div class='log-entry'>{date_str}: {row['description']} (${abs(amount):,.2f})</div>"
        )

    category_totals = df.groupby('category', as_index=False)['amount'].sum()
    fig = px.bar(category_totals, x='category', y='amount',
                 labels={"category": "Spending Category", "amount": "Amount ($)"},
                 title="Monthly Spending by Category")
    fig.update_traces(hoverinfo='skip')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font_color='#333',
        title_font_size=16,
        showlegend=False
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(139,69,19,0.2)')

    # Layout with enhanced containers
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("""
        <div class="transaction-container">
            <h3 style="margin-top: 0; margin-bottom: 1.5rem; text-align: center; color: rgba(255, 255, 255, 0.95); font-size: 1.4rem;">Transaction Log</h3>
            <div class='log-box'>""" + "".join(logs_html) + """</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        # Use HTML container approach that works with Streamlit
        st.markdown("""
        <div class="chart-container-outer">
            <h3 style="margin-top: 0; margin-bottom: 1.5rem; text-align: center; color: rgba(255, 255, 255, 0.95); font-size: 1.4rem;">Spending Overview</h3>
        """, unsafe_allow_html=True)
        
        # Create a Streamlit container for the chart
        with st.container():
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
<div class="feature-card">
    <p><strong>💬 Ask me anything about your finances:</strong></p>
    <p style="opacity: 0.8;">• "How much did I spend on dining last month?"</p>
    <p style="opacity: 0.8;">• "What's my biggest expense category?"</p>
    <p style="opacity: 0.8;">• "Help me create a savings plan"</p>
</div>
    """, unsafe_allow_html=True)

    if st.button("Start Chat", key="chat_button"):
        st.success("Chat feature coming soon!")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
<div style="text-align: center; opacity: 0.6; padding: 2rem;">
    <p>Powered by Capital One API | Built with Streamlit</p>
</div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
