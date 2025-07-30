from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from fastapi import FastAPI
from langserve import add_routes
import os
import dotenv

dotenv.load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("ERROR: GROQ_API_KEY environment variable not found. ")

    exit("Exiting due to missing GROQ_API_KEY.")
else:
    print("GROQ_API_KEY loaded successfully.")
 

model = None 
try:
    print(f"Attempting to initialize ChatGroq with model: gemma2-9b-it")
    model = ChatGroq(model="gemma2-9b-it", api_key=groq_api_key)
    print("ChatGroq model initialized successfully.")
except Exception as e:
    print(f"ERROR: Failed to initialize ChatGroq model: {e}")
    print("Possible reasons: Invalid API key, incorrect model name, or network issues.")
    exit("Exiting due to LLM initialization failure.")


# --- Define the prompt template, parser, and chain ---
Gen_template = "Translate the following input text to {language}. The response should only be the translated text." 
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", Gen_template),
        ("human", "{input_text}")
    ]
)
parser = StrOutputParser()

chain = prompt | model | parser

app = FastAPI(
    title="Simple LLM App",
    description="A simple app that uses a LLM to translate text",
    version="1.0.0"
)

try:
    print("Adding LangServe routes...")
    add_routes(
        app,
        chain,
        path="/chain"
    )
    print("LangServe routes added successfully at /chain.")
except Exception as e:
    print(f"ERROR: Failed to add LangServe routes: {e}")
    exit("Exiting due to LangServe setup failure.")


if __name__ == "__main__":
    import uvicorn
    print("Starting Uvicorn server...")
    uvicorn.run(app, host="localhost", port=8000)
    print("Uvicorn server started. Access API at http://localhost:8000")
    print("Access LangServe playground at http://localhost:8000/chain/playground")