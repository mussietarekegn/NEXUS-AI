
import streamlit as st
import requests

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🤖",
    layout="centered"
)

API_URL = "http://127.0.0.1:8000/ask"

st.title("🤖 NEXUS AI")
st.subheader("Intelligent Support & Knowledge System")

st.write(
    "Ask a question about accounts, payments, "
    "deliveries, or technical problems."
)

st.divider()


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                st.caption("Knowledge sources:")

                for source in sources:
                    st.write(f"- {source}")


question = st.chat_input(
    "How can I reset my password?"
)

if question:

    # Display the customer's question

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Call the backend

    with st.chat_message("assistant"):

        with st.spinner("NEXUS AI is thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=180
                )

                response.raise_for_status()

                result = response.json()

                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:

                    st.caption("Knowledge sources:")

                    for source in sources:
                        st.write(f"- {source}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except requests.exceptions.RequestException as error:

                error_message = (
                    "I could not connect to the NEXUS AI backend. "
                    "Please make sure the FastAPI server is running."
                )

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                })
