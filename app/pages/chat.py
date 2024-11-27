import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


def init_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content="You are a helpful AI data analysis assistant.")]


def display_chat_history():
    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)


def chat_page():
    st.title("Chat with AI Data Analyst")

    # Initialize chat history
    init_chat()

    # Display chat history
    display_chat_history()

    # Chat input
    if prompt := st.chat_input("Ask me anything about data analysis..."):
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
                response = llm(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))
                st.markdown(response.content)


if __name__ == "__main__":
    chat_page()
