from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr

# =========================
# LOAD ENV
# =========================

load_dotenv(override=True)

# =========================
# PUSH NOTIFICATION
# =========================

def push(text):

    print("PUSH FUNCTION CALLED")
    print("MESSAGE:", text)

    print("TOKEN:", os.getenv("PUSHOVER_TOKEN"))
    print("USER:", os.getenv("PUSHOVER_USER"))

    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

    print("STATUS CODE:", response.status_code)
    print("RESPONSE:", response.text)

# =========================
# TOOLS
# =========================

def record_user_details(
    email,
    name="Name not provided",
    notes="not provided"
):

    push(
        f"Recording {name} with email {email} and notes {notes}"
    )

    return {"recorded": "ok"}


def record_unknown_question(question):

    push(f"Unknown question: {question}")

    return {"recorded": "ok"}

# =========================
# MAIN CHATBOT CLASS
# =========================

class Me:

    def __init__(self):

        # =========================
        # GROQ CLIENT
        # =========================

        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        # =========================
        # MODEL
        # =========================

        self.model = "llama-3.1-8b-instant"

        self.name = "Debajyoti"

        # =========================
        # READ LINKEDIN PDF
        # =========================

        reader = PdfReader("me/linkedin.pdf")

        self.linkedin = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                self.linkedin += text

        # =========================
        # READ SUMMARY
        # =========================

        with open(
            "me/summary.txt",
            "r",
            encoding="utf-8"
        ) as f:

            self.summary = f.read()

    # =========================
    # SYSTEM PROMPT
    # =========================

    def system_prompt(self):

        return f"""
You are acting as {self.name}.

You are answering questions on {self.name}'s website,
particularly questions related to career,
background, skills and experience.

Be professional and engaging.

You are given:
1. LinkedIn profile
2. Professional summary

Use them to answer accurately.

IMPORTANT RULES:

1. If user provides an email or asks to connect,
respond ONLY in valid JSON:

{{
    "tool": "record_user_details",
    "email": "user_email",
    "name": "user_name",
    "notes": "extra notes"
}}

2. If you don't know the answer,
respond ONLY in valid JSON:

{{
    "tool": "record_unknown_question",
    "question": "user question"
}}

3. Otherwise respond normally.

4. Never explain the JSON.

5. Output ONLY JSON when calling a tool.

## SUMMARY:
{self.summary}

## LINKEDIN:
{self.linkedin}
"""

    # =========================
    # HANDLE TOOL CALLS
    # =========================

    def handle_tool_call(self, data):

        tool_name = data.get("tool")

        # =========================
        # RECORD USER DETAILS
        # =========================

        if tool_name == "record_user_details":

            record_user_details(
                email=data.get("email"),
                name=data.get("name", ""),
                notes=data.get("notes", "")
            )

            return "Thanks! Your details have been recorded."

        # =========================
        # RECORD UNKNOWN QUESTION
        # =========================

        elif tool_name == "record_unknown_question":

            record_unknown_question(
                question=data.get("question")
            )

            return (
                "I don't have that information "
                "right now, but the question "
                "has been recorded."
            )

        return None

    # =========================
    # CHAT FUNCTION
    # =========================

    def chat(self, message, history):

        # =========================
        # INITIAL SYSTEM MESSAGE
        # =========================

        messages = [
            {
                "role": "system",
                "content": self.system_prompt()
            }
        ]

        # =========================
        # ADD CHAT HISTORY
        # =========================

        for item in history:

            if item["role"] == "user":

                messages.append({
                    "role": "user",
                    "content": item["content"]
                })

            elif item["role"] == "assistant":

                messages.append({
                    "role": "assistant",
                    "content": item["content"]
                })

        # =========================
        # CURRENT USER MESSAGE
        # =========================

        messages.append({
            "role": "user",
            "content": message
        })

        # =========================
        # GROQ API CALL
        # =========================

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )

        # =========================
        # EXTRACT REPLY
        # =========================

        reply = response.choices[0].message.content

        # =========================
        # TRY TOOL PARSING
        # =========================

        try:

            data = json.loads(reply)

            if "tool" in data:

                tool_response = self.handle_tool_call(data)

                if tool_response:
                    return tool_response

        except Exception:
            pass

        return reply.strip()

# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    me = Me()

    gr.ChatInterface(
        fn=me.chat,
        title="Career Conversation Chatbot"
    ).launch()