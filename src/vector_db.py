from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Initilize OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

def get_chroma_collection():
    # Create or connect to a ChromaDB collection
    vectorstore = Chroma.from_texts(
        texts=[
            "Opens the Google Chrome browser.",
            "Opens the system calculator."
        ],
        embedding=embeddings,
        metadatas=[
            {"functino_name": "open_chrome_tool"},
            {"function_name": "open_calculator_tool"}   
        ],
        collection_name="automation_functions"
    )
    return vectorstore

def query_function(query: str):
    # Get the Chroma collection
    vectorstore = get_chroma_collection()
    
    # Query the collection for the most similar function
    results = vectorstore.similarity_search(query, k=1)
    
    # Extract the function name from the result
    if results:
        return results[0].metadata["function_name"]
    return None
