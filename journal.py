import os
import json
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime, timedelta
from collections import defaultdict

API_KEY = os.getenv("GEMINI_API_KEY")

# Load transactions
with open("transactions.json") as f:
    transactions = json.load(f)

# Streamlit page config
st.set_page_config(page_title="Financial Journal", layout="centered")
st.title("📖 Your Weekly Financial Journal")
st.subheader("Narrating your financial life, one week at a time")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

def get_week_start(date_str):
    """Get the start of the week (Monday) for a given date"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    start_of_week = date_obj - timedelta(days=date_obj.weekday())
    return start_of_week

def calculate_week_stats(week_transactions):
    """Calculate spending statistics for a week"""
    if not week_transactions:
        return {"total": 0, "categories": {}, "transaction_count": 0}
    
    total_spent = sum(t["amount"] for t in week_transactions)
    categories = defaultdict(float)
    
    for t in week_transactions:
        # Extract category from description (before the "—" separator)
        category = t["description"].split(" — ")[0] if " — " in t["description"] else "Other"
        categories[category] += t["amount"]
    
    return {
        "total": total_spent,
        "categories": dict(categories),
        "transaction_count": len(week_transactions)
    }

def clean_text(text):
    """Remove LaTeX formatting and mathematical symbols from text, format financial amounts"""
    import re
    
    # Remove LaTeX math delimiters
    text = re.sub(r'\$\$[^$]*\$\$', '', text)  # Remove $$...$$
    text = re.sub(r'\$[^$]*\$', '', text)      # Remove $...$ (but preserve dollar signs)
    
    # Remove LaTeX commands
    text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', text)  # Remove \command{...}
    text = re.sub(r'\\[a-zA-Z]+', '', text)           # Remove \command
    
    # Remove mathematical symbols that aren't dollar signs
    text = re.sub(r'[+=*/\\\[\]\{\}\^_]', '', text)
    
    # Clean up extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Format financial amounts with dollar signs - multiple patterns to catch various formats
    # Pattern 1: "spending 20" -> "spending $20"
    text = re.sub(r'\b(spending|spent|cost|costs|total of|for)\s+(\d+)\b', r'\1 $\2', text, flags=re.IGNORECASE)
    
    # Pattern 2: "20 dollars" -> "$20"
    text = re.sub(r'\b(\d+)\s*dollars?\b', r'$\1', text, flags=re.IGNORECASE)
    
    # Pattern 3: Standalone numbers that are likely money amounts (10-9999 range)
    # Look for contexts where numbers are likely money
    text = re.sub(r'\b(at|for|of)\s+(\d{2,4})\b(?!\s*(?:years?|months?|days?|times?|percent|%|people|items?))', r'\1 $\2', text, flags=re.IGNORECASE)
    
    # Pattern 4: Numbers after merchant names that are likely amounts
    text = re.sub(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+for\s+(\d+)\b', r'\1 for $\2', text)
    
    # Pattern 5: "total 150" -> "total $150"
    text = re.sub(r'\b(total|totaling)\s+(\d+)\b', r'\1 $\2', text, flags=re.IGNORECASE)
    
    # Pattern 6: Numbers in spending contexts without prepositions
    text = re.sub(r'\b(\d{2,4})\s+(on\s+[a-z]+|at\s+[A-Z])', r'$\1 \2', text)
    
    return text

def generate_persona_and_story(week_stats, week_transactions, week_start, week_end):
    """Generate a financial persona and weekly story using Gemini"""
    
    # Create the prompt for persona and story generation
    prompt = f"""
    You are a creative financial storyteller who turns spending data into engaging weekly personas and narratives.

    WEEK DATA ({week_start} to {week_end}):
    - Total spent: ${week_stats['total']}
    - Transaction count: {week_stats['transaction_count']}
    - Category breakdown: {week_stats['categories']}
    - Raw transactions: {json.dumps(week_transactions, indent=2)}

    TASK: Create a weekly financial persona and story with these exact components:

    1. PERSONA_NAME: A creative 2-3 word persona based on spending patterns (examples: "Foodie Adventurer", "Thrifty Saver", "Generous Giver", "Coffee Connoisseur", "Utility Warrior", "Shopping Explorer")

    2. EMOJI: A single emoji that represents the persona (🍕🛡️💝☕🏠🛍️ etc.)

    3. STORY: A 2-3 sentence engaging narrative that:
    - Tells their spending like a story with personality
    - Mentions specific amounts and interesting patterns
    - Includes a friendly tip or insight for next week
    - Keeps it fun and relatable, not judgmental

    FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
    PERSONA_NAME: [persona name]
    EMOJI: [single emoji]
    STORY: [2-3 sentence story with amounts and tip]

    STYLE GUIDELINES:
    - CRITICAL: Use only plain text. NO LaTeX, NO math symbols, NO equations, NO code formatting
    - ALWAYS write financial amounts with dollar signs: "$65", "$150", "$20" - NEVER write bare numbers like "65" or "150" when referring to money
    - Every money amount must have a $ symbol: "spent $50 at Starbucks", "total of $200 on groceries"
    - Never use mathematical symbols like +, =, *, /, or parentheses for calculations
    - Don't show math work or breakdowns - just state the final amounts with $ signs
    - Use simple, conversational language like you're texting a friend
    - Be encouraging and fun, not preachy
    - Focus on the most interesting spending patterns
    - Include specific merchants or categories when relevant
    - End with a forward-looking tip or encouragement

    If there are no transactions for the week, create a "Financial Hermit 🏠" persona with a story about staying in and saving money.
    
    IMPORTANT: Your response must be readable as plain text in a messaging app. No formatting, no equations, no symbols except basic punctuation and dollar signs.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                temperature=0.7,  # Lower temperature for more consistent formatting
                candidate_count=1,
                max_output_tokens=200  # Limit output to keep responses concise
            )
        )
        
        # Parse the response
        response_text = response.text.strip()
        lines = response_text.split('\n')
        
        persona_name = "Financial Explorer"
        emoji = "📊"
        story = "Had an interesting week with your finances!"
        
        for line in lines:
            if line.startswith("PERSONA_NAME:"):
                persona_name = clean_text(line.replace("PERSONA_NAME:", "").strip())
            elif line.startswith("EMOJI:"):
                emoji = line.replace("EMOJI:", "").strip()  # Don't clean emojis
            elif line.startswith("STORY:"):
                story = clean_text(line.replace("STORY:", "").strip())
        
        # Clean the full story text one more time to be sure
        story = clean_text(story)
        persona_name = clean_text(persona_name)
        
        return persona_name, emoji, story
        
    except Exception as e:
        # Fallback persona if AI fails
        return "Financial Explorer", "📊", f"This week you spent ${week_stats['total']:.0f} across {week_stats['transaction_count']} transactions. Keep up the tracking!"

def main():
    # Group transactions by week
    weeks = defaultdict(list)
    for transaction in transactions:
        week_start = get_week_start(transaction["purchase_date"])
        weeks[week_start].append(transaction)
    
    # Get the 4 most recent weeks
    sorted_weeks = sorted(weeks.keys(), reverse=True)[:4]
    
    if not sorted_weeks:
        st.error("No transaction data found!")
        return
    
    # Display each week's journal entry
    for i, week_start in enumerate(sorted_weeks):
        week_end = week_start + timedelta(days=6)
        week_transactions = weeks[week_start]
        week_stats = calculate_week_stats(week_transactions)
        
        # Generate persona and story
        with st.spinner(f"Crafting your story for week {i+1}..."):
            persona_name, emoji, story = generate_persona_and_story(
                week_stats, week_transactions, week_start, week_end
            )
        
        # Display the journal entry
        st.markdown("---")
        
        # Week header with persona
        col1, col2 = st.columns([1, 6])
        with col1:
            st.markdown(f"## {emoji}")
        with col2:
            st.markdown(f"## Week of {week_start.strftime('%B %d')}")
            st.markdown(f"**{persona_name}**")
        
        # Story content
        st.markdown(f"*{story}*")
        
        # Quick stats
        if week_stats['transaction_count'] > 0:
            with st.expander("📊 Week Details"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Spent", f"${week_stats['total']:.0f}")
                with col2:
                    st.metric("Transactions", week_stats['transaction_count'])
                
                if week_stats['categories']:
                    st.write("**Top Categories:**")
                    sorted_categories = sorted(week_stats['categories'].items(), 
                                             key=lambda x: x[1], reverse=True)[:3]
                    for category, amount in sorted_categories:
                        st.write(f"• {category}: ${amount:.0f}")
        
        st.markdown("")  # Add some spacing

if __name__ == "__main__":
    main()
