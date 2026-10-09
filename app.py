
import streamlit as st
import google.generativeai as genai

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Smart School AI Tutor",
    page_icon="🎓",
    layout="centered",
)

MODEL_NAME = "gemini-3.5-flash-lite"

# -----------------------------
# Read API key securely
# -----------------------------
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "Gemini API key not found. "
        "Please add GEMINI_API_KEY to Streamlit Secrets."
    )
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# -----------------------------
# App heading
# -----------------------------
st.title("🎓 Smart School AI Tutor")
st.caption("Your friendly learning assistant for Classes 5–10")

st.info(
    "Choose your class, subject, and language. "
    "Then ask a question to learn step by step."
)

# -----------------------------
# Student settings
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    student_class = st.selectbox(
        "📚 Select your class",
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
        "📖 Select your subject",
        [
            "Mathematics",
            "Science",
            "English",
            "Social Studies",
        ],
        index=0,
    )

language = st.selectbox(
    "🌐 Response language",
    ["English", "Hindi", "Marathi"],
    index=0,
)

st.divider()

# -----------------------------
# Keep chat history in session
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat when the student changes learning settings
current_settings = (student_class, subject, language)

if "previous_settings" not in st.session_state:
    st.session_state.previous_settings = current_settings
elif st.session_state.previous_settings != current_settings:
    st.session_state.messages = []
    st.session_state.previous_settings = current_settings
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Student question input
# -----------------------------
question = st.chat_input(
    f"Ask your {subject} question here..."
)

if question:
    # Display and save the student's question
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Instructions tailored to the student's selections
    tutor_instructions = f"""
You are Smart School AI Tutor, a patient and encouraging school tutor.

Student class: {student_class}
Subject: {subject}
Required response language: {language}

Teaching rules:
1. Explain at the student's school level.
2. Use simple, age-appropriate language.
3. Solve problems step by step and show the working.
4. Explain why each step is taken.
5. Use familiar examples when helpful.
6. For maths, check the answer when possible.
7. For science, explain concepts accurately with examples.
8. For English, help with grammar, vocabulary, reading, and writing.
9. For Social Studies, explain historical, geographical, and civic
   concepts clearly.
10. If a question is unclear, ask a short clarifying question.
11. Encourage learning instead of just giving unexplained answers.
12. Reply in {language}.
13. Be respectful, safe, and supportive of school-age learners.

Answer the student's latest question.
"""

    # Build conversation context from recent messages
    recent_messages = st.session_state.messages[-10:]

    conversation = []
    for message in recent_messages:
        role = "Student" if message["role"] == "user" else "Tutor"
        conversation.append(f"{role}: {message['content']}")

    full_prompt = (
        tutor_instructions
        + "\nConversation:\n"
        + "\n\n".join(conversation)
        + "\n\nTutor:"
    )

    # Ask Gemini
    with st.chat_message("assistant"):
        with st.spinner("Your tutor is thinking..."):
            try:
                response = model.generate_content(full_prompt)
                answer = response.text

                if not answer:
                    answer = (
                        "I couldn't create an answer this time. "
                        "Please try asking in a different way."
                    )

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as error:
                st.error(
                    "The tutor couldn't answer just now. "
                    "Please wait a little and try again."
                )
                # Technical details can help with troubleshooting.
                st.caption(f"Technical details: {error}")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(
    "Smart School AI Tutor • Learn step by step • "
    "Always check important answers with your teacher or textbook."
)
