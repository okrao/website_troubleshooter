import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load the hidden .env file so Python can read your API key
load_dotenv()

# Pull the key and strip any invisible line breaks/spaces
raw_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=raw_key.strip() if raw_key else None)

# --- UI CONFIGURATION ---
# This sets up the tab title and the main header on the page
st.set_page_config(page_title="Agent Assist Copilot", page_icon="🎧")
st.title("Tier 1 Agent Assist: Login Troubleshooting")
st.caption("Step-by-step guidance to reduce AHT and ensure SOP compliance.")

# --- MEMORY MANAGEMENT ---
# Streamlit reruns the script on every input. We use session_state to save the chat history.
if "messages" not in st.session_state:
    copilot_instructions = """You are an expert technical support copilot assisting a live customer service representative. 
    Your job is to guide the rep step-by-step to resolve a customer's website login issue.

    CRITICAL RULES:
    1. Only provide ONE troubleshooting question or step for the rep to take at a time.
    2. Never give the whole list at once. Wait for the rep to report the customer's answer.
    3. Keep responses under 3 sentences. The rep is on a live call and must read quickly.

    LOGIN TROUBLESHOOTING SOP:
    - Step 1 (Environment): Ask if they are on a mobile app or computer browser. If browser, verify they are at the official URL. If app, verify it is updated.
    - Step 2 (Credentials): Ask if the password is auto-filling. If yes, have them delete it and type manually.
    - Step 3 (Account State): Ask for the exact error message. If "Locked", initiate password reset. If "MFA error", check email/text delivery.
    - Step 4 (Technical): Have them open an Incognito/Private window. If that works, direct the rep to help them clear browser cache.
    """
    
    st.session_state.messages = [
        {"role": "system", "content": copilot_instructions}
    ]

# --- RENDER CHAT HISTORY ---
# Draw all previous messages to the screen (skipping the hidden system prompt)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- CHAT INPUT & AI GENERATION ---
# The st.chat_input creates the text box at the bottom of the screen
if rep_input := st.chat_input("Enter customer response here..."):
    
    # 1. Display the rep's input on the screen
    with st.chat_message("user"):
        st.markdown(rep_input)
    
    # 2. Save the rep's input to the background memory
    st.session_state.messages.append({"role": "user", "content": rep_input})
    
    # 3. Call Groq to generate the next troubleshooting step
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model="openai/gpt-oss-120b",
            temperature=0.3
        )
        
        ai_response = chat_completion.choices[0].message.content
        
        # Display the AI's response on the screen
        message_placeholder.markdown(ai_response)
        
    # 4. Save the AI's response to the background memory
    st.session_state.messages.append({"role": "assistant", "content": ai_response})