import streamlit as st
import plotly.express as px
import pandas as pd
import json


# --- Page configuration ---
st.set_page_config(
    page_title="Smart Budgeting Assistant",
    page_icon="💰",
    layout="wide"
)

# --- Load external CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles.css")

# --- Header section ---
st.markdown("""
<div class="header-container">
    <div class="custom-title">Smart Budgeting Assistant</div>
    <div class="subtitle">AI-powered financial insights with Capital One integration</div>
</div>
""", unsafe_allow_html=True)

# --- Key metrics ---
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

def get_spreedsheet():
    df = pd.read_json("transactions.json")
    
    # --- Create category column ---
    def categorize(desc):
        desc = str(desc).lower()
        if 'grocery' in desc:
            return 'Groceries'
        elif 'uber' in desc or 'lyft' in desc:
            return 'Transportation'
        elif 'netflix' in desc or 'movie' in desc:
            return 'Entertainment'
        elif 'utility' in desc:
            return 'Utilities'
        elif 'restaurant' in desc or 'dining' in desc:
            return 'Dining'
        else:
            return 'Other'

    df['category'] = df['description'].apply(categorize)

    # --- Convert date ---
    df['date'] = pd.to_datetime(df['purchase_date'])

    # --- Sort descending ---
    df = df.sort_values(by='date', ascending=False)

    # --- Median per category ---
    category_medians = df.groupby('category')['amount'].median().to_dict()

    # --- Category colors ---

    # --- Build logs ---
    logs_html = []
    for _, row in df.iterrows():
        date_str = row['date'].strftime("%m/%d/%y")
        category = row['category']
        amount = row['amount']

        # Conditional text color
        text_color = 'red' if amount > category_medians[category] else 'green'

        logs_html.append(
            f"<div class='log-entry' style='color:{text_color}; padding:4px; margin-bottom:4px;'>"
            f"{date_str}: {row['description']} (${abs(amount):,.2f})"
            f"</div>"
        )

    # --- Render scrollable box ---
    log_html = "<div class='log-box'>" + "".join(logs_html) + "</div>"
    st.markdown(log_html, unsafe_allow_html=True)
    return log_html

get_spreedsheet()

# --- Main content area ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h3>Spending Overview</h3>', unsafe_allow_html=True)
    df = pd.read_json('transactions.json')
    df = df[['purchase_date', 'amount', 'description']]  # select needed columns
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    df = df.sort_values(by='purchase_date', ascending=False)
    #df['category'] = df['description'].apply(categorize)
    df['category'] = df['description'].fillna('').str.split().str[0]

    category_totals = df.groupby('category', as_index=False)['amount'].sum()

    fig = px.bar(
            category_totals,
            x='category', 
            y='amount',
            color='amount',
            color_continuous_scale=['#ff9a7b', '#ffb07b'],
            title="Monthly Spending by Category"
        )

    fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,0)',
            font_color='#333',
            title_font_size=16,
            showlegend=False
        )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(139,69,19,0.2)')    
    st.plotly_chart(fig, use_container_width=True)

# AI Assistant feature card
with col2:
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


# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; opacity: 0.6; padding: 2rem;">
    <p>Powered by Capital One API | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

