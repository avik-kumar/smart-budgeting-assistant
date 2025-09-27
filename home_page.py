import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Smart Budgeting Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for sleek design
st.markdown("""
<style>
/* Main background and typography */
.main {
    background: linear-gradient(135deg, #FFDAB9 0%, 
#FFE5B4 100% }
);


/* Header styling */
.header-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Feature cards */
.feature-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin: 1rem 0;
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

/* Navigation bar */
.nav-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 999;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1rem;
    border-radius: 25px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #ff9a7b, #ffb07b);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

/* Stats styling */
.metric-card {
    background: rgba(255, 255, 255, 0.15);
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom title */
.custom-title {
    font-size: 3.5rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #8B4513, #654321);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    font-size: 1.3rem;
    text-align: center;
    opacity: 0.9;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Navigation
col1, col2 = st.columns([4, 1])
with col2:
    page = st.selectbox(
        "",
        ["Dashboard", "Analytics", "Settings", "Profile"],
        label_visibility="collapsed"
    )

# Main header section
st.markdown("""
<div class="header-container">
    <div class="custom-title">Smart Budgeting Assistant</div>
    <div class="subtitle">AI-powered financial insights with Capital One integration</div>
</div>
""", unsafe_allow_html=True)

# Key metrics section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>$2,450</h3>
        <p>Monthly Budget</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>$1,890</h3>
        <p>Spent This Month</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>$560</h3>
        <p>Remaining Budget</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3>23%</h3>
        <p>Budget Remaining</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Spending Overview")
    
    # Sample spending data
    categories = ['Groceries', 'Transportation', 'Entertainment', 'Utilities', 'Dining']
    amounts = [450, 320, 280, 180, 350]
    
    fig = px.bar(
        x=categories, 
        y=amounts,
        color=amounts,
        color_continuous_scale=['#ff9a7b', '#ffb07b'],
        title="Monthly Spending by Category"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(255,255,255,0.1)',
        font_color='#333',
        title_font_size=16,
        showlegend=False
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(139,69,19,0.2)')
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### AI Assistant")
    
    # Chat interface preview
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

# Features section
st.markdown("### Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>Real-time Tracking</h4>
        <p>Connect your Capital One accounts for automatic transaction monitoring and categorization.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>Smart Analytics</h4>
        <p>Get personalized insights and spending patterns powered by advanced AI algorithms.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>Budget Optimization</h4>
        <p>Receive tailored recommendations to maximize your savings and reach financial goals.</p>
    </div>
    """, unsafe_allow_html=True)

# Call to action section
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="header-container" style="text-align: center;">
        <h3>Ready to take control of your finances?</h3>
        <p>Connect your Capital One account and start your journey to smarter budgeting.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("Connect Account", key="connect_button"):
            st.balloons()
            st.success("Account connection feature coming soon!")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; opacity: 0.6; padding: 2rem;">
    <p>Powered by Capital One API | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)