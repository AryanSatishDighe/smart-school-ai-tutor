
import streamlit as st
from google import genai

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Smart School AI Tutor",
    page_icon="🎓",
    layout="centered",
)

MODEL_NAME = "gemini-3.5-flash-lite"

# -----------------------------
# Secure API key
# -----------------------------
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "Gemini API key not found. "
        "Please add GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)

# -----------------------------
# Heading
# -----------------------------
st.title("🎓 Smart School AI Tutor")
st.caption("Your friendly learning assistant for Classes 5–10")

st.info(
    "Choose your class, subject, and language, "
    "then ask your question."
)

# -----------------------------
# Learning preferences
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    student_class = st.selectbox(
        "📚 Choose your class",
        [
            "Class 5",
            "Class 6",
            "Class 7",
            "Class 8",
            "Class 9",
            "Class 10",
        ],
        index=3,
    )

with col2:
    subject = st.selectbox(
        "📖 Choose your subject",
        [
            "Mathematics",
            "Science",
            "English",
            "Social Studies",
        ],
    )

language = st.selectbox(
    "🌐 Answer language",
    ["English", "Hindi", "Marathi"],
)

st.divider()

# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

settings = (student_class, subject, language)

if "last_settings" not in st.session_state:
    st.session_state.last_settings = settings
elif st.session_state.last_settings != settings:
    st.session_state.messages = []
    st.session_state.last_settings = settings
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Ask the tutor
# -----------------------------
question = st.chat_input("Type your question here...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    instructions = f"""
You are Smart School AI Tutor, a friendly and patient school tutor.

Student class: {student_class}
Subject: {subject}
Answer language: {language}

Teaching guidelines:
- Use simple language suitable for the student's class.
- Explain answers step by step.
- Show calculations clearly for mathematics.
- Explain science concepts with familiar examples.
- Help with grammar, vocabulary, reading, and writing in English.
- Explain Social Studies clearly and accurately.
- Check calculations when possible.
- Encourage understanding, not just memorization.
- If the question is unclear, ask a brief follow-up question.
- Respond in {language}.
- Be respectful and suitable for school-age learners.
"""

    recent_messages = st.session_state.messages[-10:]

    conversation = "\n\n".join(
        (
            "Student: " if message["role"] == "user" else "Tutor: "
        ) + message["content"]
        for message in recent_messages
    )

    prompt = (
        instructions
        + "\nConversation so far:\n"
        + conversation
        + "\n\nTutor:"
    )

    with st.chat_message("assistant"):
        with st.spinner("Your tutor is thinking..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                )

                answer = response.text

                if not answer:
                    answer = (
                        "I couldn't generate an answer. "
                        "Please try asking in a different way."
                    )

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as error:
                st.error(
                    "The tutor couldn't answer right now. "
                    "Please wait a moment and try again."
                )
                st.caption(f"Technical details: {error}")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(
    "Smart School AI Tutor • Learn step by step • "
    "Check important answers with your teacher or textbook."
)
