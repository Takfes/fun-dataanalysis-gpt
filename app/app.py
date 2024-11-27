import pandas as pd
import streamlit as st

from dapgpt.agent import DataAnalysisAgent

# from src.agent import DataAnalysisAgent

st.set_page_config(page_title="AI Data Analyst", layout="wide")


def main():
    st.title("AI Data Analysis Assistant")

    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read and display the data
        df = pd.read_csv(uploaded_file)
        st.subheader("Data Preview")
        st.dataframe(df.head())

        # User query input
        user_query = st.text_area(
            "What would you like to know about your data?",
            height=100,
            placeholder="e.g., 'What are the main trends in this dataset?' or 'Create a summary of the key statistics'",
        )

        if st.button("Analyze"):
            if user_query:
                with st.spinner("Analyzing your data..."):
                    # Initialize agent and get response
                    agent = DataAnalysisAgent()
                    response = agent.analyze(df, user_query)

                    # Display response
                    st.subheader("Analysis Results")
                    st.write(response)
            else:
                st.warning("Please enter a query about your data.")


if __name__ == "__main__":
    main()
