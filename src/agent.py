import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from src.automation_functions import open_chrome_tool, open_calculator_tool
from src.vector_db import query_function

def create_agent():

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY must be set")

    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model="gpt-4o-mini",
        temperature=0
    )

    tools = [open_chrome_tool(), open_calculator_tool()]

    agent = create_react_agent(
        llm,
        tools
    )

    return agent

