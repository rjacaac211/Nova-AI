import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langsmith import traceable
from src.automation_functions import open_chrome_tool, open_calculator_tool, open_notepad_tool, get_cpu_usage_tool, get_ram_usage_tool, run_shell_command_tool
from src.vector_db import query_function

# Load environment variables from .env file
load_dotenv()

def create_agent():

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY must be set")

    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model="gpt-4o-mini",
        temperature=0
    )

    tools = [
        open_chrome_tool,
        open_calculator_tool,
        open_notepad_tool,
        get_cpu_usage_tool,
        get_ram_usage_tool,
        run_shell_command_tool
    ]

    system_prompt = """
        You are Nova, an intelligent automation agent designed to execute system tasks. 
        Your available tools are:
        1. open_chrome_tool: Opens the Google Chrome browser.
        2. open_calculator_tool: Opens the system calculator.
        3. open_notepad_tool: Opens Notepad.
        4. get_cpu_usage_tool: Retrieves current CPU usage percentage.
        5. get_ram_usage_tool: Retrieves current RAM usage and available memory.
        6. run_shell_command_tool: Executes a shell command and returns its output.

        When a user sends a query, select and execute the appropriate tool.
        Always return only the final result of the executed tool without any extra commentary.
        If the query is ambiguous, choose the best matching tool based on its description.
    """

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )

    return agent

@traceable
def process_query(query: str) -> str:
    """
    Process the query using the agent and return the response.
    """
    agent = create_agent()
    # Build the input payload as a message list
    inputs = {
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }

    # Optionally, use ChromaDB to perform a similarity search on the function descriptions
    matched_function = query_function(query)
    print("Vector DB Matched Function:", matched_function)

    # Invoke the agent and extract the final message content
    result = agent.invoke(inputs)
    return result["messages"][-1].content