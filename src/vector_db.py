import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_vectorstore():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY must be set")

    # Initialize the OpenAI embeddings model
    embedding_model = OpenAIEmbeddings(
        api_key=openai_api_key,
        model="text-embedding-ada-002"
    )

    # Define the function description and corresponding metadata
    texts = [
        "Open the Google Chrome browser.",
        "Open the system calculator.",
        "Open the Notepad application.",
        "Retrieve the current CPU usage percentage.",
        "Retrieve the current RAM usage and available memory.",
        "Execute a shell command and return its output."
    ]
    metadatas = [
        {"function_name": "open_chrome_tool"},
        {"function_name": "open_calculator_tool"},
        {"function_name": "open_notepad_tool"},
        {"function_name": "get_cpu_usage_tool"},
        {"function_name": "get_ram_usage_tool"},
        {"function_name": "run_shell_command_tool"}
    ]

    # Create (or connect to) a ChromaDB collection with your function data]
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas,
        collection_name="automation_functions",
    )
    return vectorstore

def query_function(query: str):
    """
    Perform a similarity search in the vectorstore to find the most relevant function
    based on the user's query.
    """
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=1)
    if results:
        return results[0].metadata["function_name"]
    return None
