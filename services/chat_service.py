# Basic
from typing import List

# LLM
from openai import OpenAI

# Custom modules
from database import DatabaseOperations



OPENAI_KEY = ""
client = OpenAI(api_key=OPENAI_KEY)

database = DatabaseOperations()



def get_answer(question: str, enable_history: bool) -> List[dict]:

    messages = []

    if OPENAI_KEY:
        # Generate system insruction for LLM
        for instruction in database.select_llm_instructions():
            messages.append({"role": "system", "content": instruction})
        
        # Retrieve relative context and provide for LLM as system insruction
        response = client.embeddings.create(
            model="text-embedding-3-small",
            dimensions=512,
            input=question,
        )
        embedding = response["data"][0]["embedding"]

        context = database.retrive_context(embedding)
        if context:
            sys_context = f'''<CONТEXT>\n{context}\n</CONТEXT>'''
            messages.append({"role": "system", "content": sys_context})

        if enable_history:
            # Get chat use history and add to chat
            history = database.select_history()
            messages.extend(history)
            print(history) 

    # Add user question to chat and DB User Table
    messages.append({"role": "user", "content": question})
    database.insert_message(messages[-1])
    
    if OPENAI_KEY:
        # Send to LLM for proceed answer
        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages,
            temperature = 0.05,
            max_tokens = 512)
        
        answer = completion.choices[0].message.content
    else:
        context = database.retrive_context()
        answer = f"<b>Assistant answered your question with CONTEXT:</b> \n{context}"
    
    result = {"role": "assistant", "content": answer}
    database.insert_message(result)
    return result


def get_user_history() -> List[dict]:
    return database.select_history()