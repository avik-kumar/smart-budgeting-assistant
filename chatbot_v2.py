import random 
import json
import os
# hard-coded the API key as an environment variable instead
# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
from google import genai
from google.genai import types

# API_KEY = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=API_KEY)

# open transactions.json and store it
with open("transactions.json") as f:
    transactions = json.load(f)

# layout - need to edit after integration
st.set_page_config(page_title="Smart Budgeting Assistant",layout="centered")
st.title("Smart Budgeting Assistant")
st.subheader("Engage with your very own chatbot to learn essential financial literacy and budgeting skills!")

# Initialize Google client once
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

# Initialize Gemini chat history 
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")

# Initialize chat history for UI 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hi! I'm your financial assistant. Ask me anything about general financial literacy or for information regarding your transactions. How can I help you today?"
        }
    ]

def display_messages():
# Display all messages in the chat history
    for msg in st.session_state.messages:
        author = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(author):
            st.write(msg["content"])

def friendly_wrap(raw_text):
    responses = [
        "Great question!",
        "Nice question.",
        "Excellent question!",
        "That’s a good question."
    ]
# Add a friendly tone to the AI responses at the beginning and end of the AI response
    return (
        random.choice(responses) + "\n\n"
        f"{raw_text.strip()}\n\n"
        "Would you like me to elaborate on any part of this, or do you have other questions?"
    )

# Display existing messages
display_messages()

# Accept user's question and display following prompt in the user input bar
prompt = st.chat_input("Ask me about financial literacy, your transaction history, or anything else on your mind!")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user message
    with st.chat_message("user", avatar = "👤"):
        st.write(prompt)

    # Show thinking indicator while processing
    with st.chat_message("assistant", avatar = "🤖"):
        placeholder = st.empty()
        placeholder.write("🤔 Thinking...")

        # Call Gemini API
        try:
            '''
            client = genai.Client()
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                # Prompt for gemini to consider in its response
                contents = f"""You are a helpful, certified financial expert and advisor interacting with a user 
                through a chatbot. Keep your responses clear, understandable, and professional. Do not provide filler information. 
                Organize your response cleanly into sections when appropriate, but keep it very brief and as much to the point as possible 
                (try not exceed around 200 words, unless more detail is needed). Additionally, here are the user's 
                personal expenditures in JSON format: {transactions}. Use this if the user has any specific questions 
                regarding their transactions, including budgeting advice and total expenditure by category. 
                If the user asks a question related to their transaction history, ensure your response is definitely accurate and based on 
                the data available. If you do not have the neccessary data, politely inform the user. Please provide an accurate 
                and helpful response to this prompt from the user: {prompt}.""",
                # Comment this out to enable thinking: 
                config = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=0)) 
            )
            '''
            response = st.session_state.chat.send_message(
                # Prompt for gemini to consider in its response
                f"""You are a helpful, certified financial expert and advisor interacting with a user 
                through a chatbot. Keep your responses clear, understandable, and professional. Do not provide filler information. 
                Organize your response cleanly into sections when appropriate, but keep it very brief and as much to the point as possible 
                (try not exceed around 200 words, unless more detail is needed). Additionally, here are the user's 
                personal expenditures in JSON format: {transactions}. Use this if the user has any specific questions 
                regarding their transactions, including budgeting advice and total expenditure by category. 
                If the user asks a question related to their transaction history, ensure your response is definitely accurate and based on 
                the data available. If you do not have the neccessary data, politely inform the user. Please provide an accurate 
                and helpful response to this prompt from the user: {prompt}.""",
                config = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=0)) # Comment this out to enable thinking
            )
            answer = response.text
            friendly_answer = friendly_wrap(answer) 
            placeholder.write(friendly_answer)
        except Exception as e:
            # friendly_answer = f"I'm sorry, I encountered an error. Please try asking your question again."
            placeholder.write("I'm sorry, I encountered an error. Please try asking your question again.")

        # placeholder.write(friendly_answer)

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": friendly_answer})

        # Refresh the page to show updated chat
        st.rerun()  