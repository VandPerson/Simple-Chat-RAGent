# Basic
from typing import List
from pathlib import Path
import json

# Data Manipulation
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



MAIN_DIR = Path(__file__).parent.resolve()



class DatabaseOperations:
    """
    Simulates database operations to interact with data.

    Attributes:
        df_context_table (pd.DataFrame): DataFrame of context paragraphs and vectors.
        df_user_table (pd.DataFrame): DataFrame of user message history.
    """
    def __init__(self):
        self.df_context_table = pd.read_json(MAIN_DIR / "context_data.json", orient="records")
        try:
            self.df_user_table = pd.read_json(MAIN_DIR / "user_data.json", orient="records", lines=True)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["role", "content"])
            self.df_user_table = df
        
    def read_context_table(self) -> List[dict]:
        """
        Reads the context table and returns the data as a list of dictionaries.

        Returns:
            List[dict]: A list of dictionaries representing data used for RAG.
        """
        json_str = self.df_context_table.to_json(orient="records")
        return json.loads(json_str)
    
    def insert_message(self, row: dict) -> None:
        self.df_user_table.loc[len(self.df_user_table)] = row
        self.df_user_table.to_json(MAIN_DIR / "user_data.json",
                                   orient="records",
                                   lines=True)

    def select_history(self):
        return self.df_user_table.to_dict(orient="records")
    
    def select_llm_instructions(self) -> list:
        instructions = [
            "You are an artificial intelligence chatbot in company BrewNest. You follow these four instructions below in all your responses:",
            "1. Answer the user's question briefly and politely;",
            "2. Answer in the language of the user's question;",
            "3. You only know the information that is in the CONTEXT, otherwise, tell the user that it is not written in your manual, and that's it;"
            "4. You can use chat history as CONTEXT.",
        ]
        return instructions
    
    def retrive_context(self, vector: List[float] = None) -> str:
        """
        Retrieve the two most relevant context paragraphs based on cosine similarity.

        Args:
            vector (List[float], optional): A 512-dimensional embedding vector.
                If not provided, a random vector will be generated.

        Returns:
            str: Concatenated string of the top 2 most similar paragraphs.
        """
        if vector is None:
            emmbedding = np.array(np.random.rand(512).tolist()).reshape(1, -1)
        else:
            emmbedding = np.array(vector).reshape(1, -1)
        
        df_data = self.df_context_table

        vector_matrix = np.vstack(df_data["vector"].values)
        similarities = cosine_similarity(emmbedding, vector_matrix).flatten()

        df_data['similarity'] = similarities

        relevant_context = df_data.sort_values(
            by='similarity',
            ascending=False).head(2)

        return '\n\n'.join(relevant_context['paragraph'].astype(str).tolist())