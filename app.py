import os
import streamlit as st
from google import genai
from google.genai import errors

# -------------------- Page setup --------------------
st.set_page_config(
    page_title="Smart School AI Tutor",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 Smart School AI Tutor")
st.caption("A friendly AI learning companion for Classes 5–10")

# -------------------- API key setup --------------------
def get_api_key():
    # Streamlit Cloud: add GEMINI_API_KEY in App settings > Secrets.
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key or os.getenv("GEMINI_API_KEY", "")

api_key = get_api_key()

if not api_key:
    st.error(
        "Gemini API key not found. For Streamlit Community Cloud, open "
        "your app's Settings → Secrets and add:\n\n"
        'GEMINI_API_KEY = "your_api_key_here"\n\n'
        "Do not put your real API key in app.py or upload it to GitHub."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# Change this if the model is not available for your API key.
MODEL_NAME = "gemini-3.5-flash"

# -------------------- Sidebar settings --------------------
with st.sidebar:
    st.header("Your learning settings")
    student_class = st.selectbox(
        "Choose your class",
        ["5", "6", "7", "8", "9", "10"],
        index=1,
    )
    st.caption("Ask questions from any school subject.")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -------------------- Conversation state --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- Chat input and answer --------------------
question = st.chat_input("Ask a question, e.g. What is photosynthesis?")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    with st.chat_message("user"):
        st.markdown(question)

    # Keep recent messages so follow-up questions have context.
    recent_messages = st.session_state.messages[-10:]
    conversation = "\n".join(
        ("Student: " if m["role"] == "user" else "Tutor: ") + m["content"]
        for m in recent_messages
    )

    prompt = f"""
You are Smart School AI Tutor, a kind and accurate tutor for students in
Classes 5 to 10.

The student's selected class is Class {student_class}.

Guidelines:
- Answer questions from school subjects including mathematics, science,
  English, history, geography, and other subjects.
- Use language suitable for the selected class.
- For mathematics, show the steps clearly.
- Give a simple example when it helps.
- Be encouraging and respectful.
- If a question is unclear, ask a brief clarifying question.
- Do not pretend to know something if you are uncertain.
- For important facts, encourage the student to check their textbook or teacher.

Recent conversation:
{conversation}

Write the tutor's next answer:
"""

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                )
                answer = response.text or (
                    "Sorry, I couldn't create an answer. Please try again."
                )
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except errors.APIError as exc:
                st.error(
                    "The Gemini API could not answer this request. "
                    "Please check your model access, API quota, and connection."
                )
                st.caption(f"Technical details: {exc}")
            except Exception as exc:
                st.error("Something went wrong. Please try again.")
                st.caption(f"Technical details: {exc}")

st.divider()
st.caption(
    "Learning note: AI can make mistakes. Check important answers with "
    "your textbook or teacher. Never enter private or sensitive information."
)
