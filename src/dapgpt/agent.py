import json
import os

import openai
import pandas as pd
from dotenv import load_dotenv


class DataAnalysisAgent:
    def __init__(self):
        # Make sure to set your OpenAI API key in streamlit secrets
        load_dotenv()
        openai_key = os.getenv("OPENAI_KEY")

    def _create_system_prompt(self, df: pd.DataFrame) -> str:
        """Create system prompt with dataset context"""
        columns_info = {col: str(df[col].dtype) for col in df.columns}

        return f"""You are a data analysis expert. \
            You will be provided with a dataset that has the following columns:
            {json.dumps(columns_info, indent=2)}

            Analyze the data based on the user's query and provide insights.
            Include relevant statistics and explanations in your response."""

    def _prepare_data_context(self, df: pd.DataFrame) -> str:
        """Prepare dataset context for the API call"""
        return f"""Dataset Summary:
            - Shape: {df.shape}
            - Column Statistics:
            {df.describe().to_string()}

            Sample of data (first 5 rows):
            {df.head().to_string()}"""

    def analyze(self, df: pd.DataFrame, query: str) -> str:
        """Analyze the dataset based on user query"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._create_system_prompt(df)},
                    {"role": "user", "content": f"Data Context:\n{self._prepare_data_context(df)}\n\nQuery: {query}"},
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during analysis: {e!s}"
