import os
from dotenv import load_dotenv
from groq import Groq

# Load the hidden .env file so Python can read your API key
load_dotenv()

# Initialize the Groq client looking for your environment variable
# The .strip() command cleans off any invisible spaces or line breaks
raw_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=raw_key.strip() if raw_key else None)

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

chat_history = [
    {"role": "system", "content": copilot_instructions}
]

print("Copilot is ready. Type 'quit' to exit.\n")

while True:
    rep_input = input("Customer Update (or type 'quit'): ")
    
    if rep_input.lower() == 'quit':
        print("Closing copilot. Have a good shift!")
        break

    chat_history.append({"role": "user", "content": rep_input})

    chat_completion = client.chat.completions.create(
        messages=chat_history,
        model="openai/gpt-oss-120b",
        temperature=0.3
    )

    ai_response = chat_completion.choices[0].message.content
    
    print(f"\nCOPILOT SAYS: {ai_response}\n")

    chat_history.append({"role": "assistant", "content": ai_response})