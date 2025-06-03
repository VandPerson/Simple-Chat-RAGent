# Full-Stack & AI-Enabled Web Application

A FastAPI-based backend with Jinja2 frontend (server-rendered templates) for an AI assistant whom capable of contextual retrieval.

![alt text](assets/chat_example.png)

---

## Setup Instructions

1) **Clone the Repository**
```bash
git clone https://github.com/VandPerson/Simple-AI-Enabled-Web-Application.git
cd Simple-AI-Enabled-Web-Application
```
2) **Create a Virtual Environment**
On Linux:
```bash
python3 -m venv venv
source .venv/bin/activate
```
On Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```
3) **Install Dependencies**
```bash
pip install -r requirements.txt
```
Or if are planning to do some development and testing:
```bash
pip install -r requirements-dev.txt
```

## Execution Instructions

**Start the FastAPI Server**
```bash
uvicorn main:app --reload
```
The Chat UI will be available at:  
http://127.0.0.1:8000

For observe all available APIs visit:  
'http://127.0.0.1:8000/docs' for Swagger UI or 'http://127.0.0.1:8000/redoc'

## Testing

Run All Tests with `pytest`:
On Linux:
```bash
python3 -m pytest tests/
```
On Windows:
```powershell
python -m pytest tests/
```

## Approach Explanation

### **Functionality:**
Using FastAPI, two APIs were implemented.  
The first, `/api/ask`, is for answering questions, and the second, `/api/history`, is for displaying previously asked user questions.

As a frontend, Jinja2 server-rendered templates were used.  
On the first page load, the history is automatically rendered in HTML.

New questions are sent through `/api/ask` to the backend, where an answer is generated using a Retrieval-Augmented Generation approach with `gpt-4o-mini`.

### **Database:**
For now, the app uses flat files to simulate database tables.  
The `database/context_data.json` file contains relevant company information with generated vectors.  
The `.dev` folder contains an ETL procedure to collect data from a list of files and generate relevant embeddings using `text-embedding-3-small`.  
The `database/user_data.json` file contains the history of user asked questions.  
The `database/database.py` file includes a class *DatabaseOperations* that simulates a connection to a database.  
If inherit from this class and override its methods with a real database connection, all functionality will work the same way.

### **Retrieval-Augmented Generation:**  
For retrieval, a vector cosine similarity approach is used.  
This allows semantically relevant results even when the query does not exactly match the keywords.  
With this approach, the prompt includes the top-2 context chunks.

### **Language Model:**  
The prompt sent to the LLM includes both the instructions and context chunks.  
If `enable_history` is `True`, previous user messages are also included in the prompt.  
By default, this is set to `False`, but it can be changed as parameter when calling the `/api/ask` endpoint.

### **Modular Design:**  
Services and schemas are isolated from the route logic for clean separation of concerns and easier testability.

## Known Limitations/Trade-Offs

- Generated vectors are faked and were not actually created by OpenAI, as they were numpy random numbers instead of sent to the real LLM. This is because I don't have a real API key. As a result, the app working with faked vectors when retrieving context chunks.
In theory, with a valid API key, everything should work as expected.  
But first, need to regenerate `context_data.json` using `ETL.py`.  
It will create the new `context_data.json` file in the `.dev` folder. The next step is to move it to the `database/` folder and replace the old one.  
Then, provide the OpenAI API key in `chat_service.py` so the OpenAI API will function correctly.
- Timestamps are not fully implemented.
- There is no config file, so some settings are hardcoded.
- There is no error handling.
- There is no logging.
- Testing is limited by three test cases.
- There are some UI issues that can be improved.
- If need delete history, need to delete `user_data.json` file.
- Not all functions, modules, classes, etc. are properly documented.