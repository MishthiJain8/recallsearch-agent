import streamlit as st
from dotenv import load_dotenv
from memory import save, history, clear
from agent import answer

load_dotenv()

st.set_page_config(page_title="RecallSearch", page_icon="🔎")

st.title("🔎 RecallSearch")
st.caption("Search smarter. Remember every question.")

with st.sidebar:
    st.header("Question History")
    questions = [
        (msg, time)
        for role, msg, time in history(100)
        if role == "user"
    ]

    if questions:
        for msg, timestamp in reversed(questions[-25:]):
            st.caption(f"{timestamp} UTC")
            st.write(msg)
    else:
        st.info("No questions yet.")

    if st.button("Clear History"):
        clear()
        st.rerun()

for role, message, timestamp in history(30):
    with st.chat_message(role):
        st.markdown(message)
        st.caption(timestamp + " UTC")

question = st.chat_input("Ask me anything...")

if question:
    previous = history(16)
    save("user", question)

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking and searching..."):
            try:
                text, sources = answer(question, previous)
                if sources:
                    text += "\n\nSources:\n"
                    for title, url in sources:
                        text += f"\n- [{title}]({url})"
            except Exception as error:
                text = f"Unable to answer: {error}"

            st.markdown(text)

    save("assistant", text)
    st.rerun()
