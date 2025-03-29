import os
import webbrowser
from langchain.tools import tool

@tool
def open_chrome_tool(query: str) -> str:
    webbrowser.open("https.//www.google.com")
    return "Chrome opened successfully."

@tool
def open_calculator_tool(query: str) -> str:
    os.system("calc")
    return "Calculator launched successfully."

