import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langsmith import traceable

from src.automation_functions import (
    open_chrome_tool,
    open_calculator_tool,
    open_notepad_tool,
    get_cpu_usage_tool,
    get_ram_usage_tool,
    run_shell_command_tool
)
from src.vector_db import query_function
from src.memory_manager import MemoryManager

# Load environment variables from .env file
load_dotenv()

# Initialize an in-memory conversation manager with a window size of 10 messages
memory_manager = MemoryManager(window_size=10)

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

    # Define the system prompt for the agent
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

# @traceable
# def process_query(query: str) -> str:
#     """
#     Process a single-turn query without memory.
#     """
#     agent = create_agent()
#     # Optionally, check which tool the vector DB matched (for debugging)
#     matched_function = query_function(query)
#     print("Vector DB Matched Function:", matched_function)

#     # Build the input payload as a message list
#     inputs = {
#         "messages": [
#             {"role": "user", "content": query}
#         ]
#     }
#     # Invoke the agent and extract the final message content
#     result = agent.invoke(inputs)
#     return result["messages"][-1].content

@traceable
def run_agent(session_id:str, user_message: str) -> str:
    """
    Process a user message using the agent and store conversation history in memory.
    :param session_id: Unique identifier for the user/session.
    :param user_message: The latest user message.
    :return: The agent's final text response.
    """
    agent = create_agent()

    # Append the new user message
    memory_manager.save_message(session_id, "user", user_message)

    # Load conversation history from memory
    conversation_history = memory_manager.load_conversation(session_id)

    # Invoke the agent with the conversation history
    inputs = {"messages": conversation_history}
    result = agent.invoke(inputs)
    assistant_message = result["messages"][-1].content

    # Save the assistant's response in memory
    memory_manager.save_message(session_id, "assistant", assistant_message)
    return assistant_message

def clear_session(session_id: str):
    """Clear conversation history for a given session."""
    memory_manager.clear_conversation(session_id)

