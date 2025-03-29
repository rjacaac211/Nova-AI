import os
import webbrowser
import subprocess
from langchain_core.tools import tool

@tool
def open_chrome_tool(query: str) -> str:
    """Open the Google Chrome browser."""
    webbrowser.open("https://www.google.com/")
    return "Chrome opened successfully."

@tool
def open_calculator_tool(query: str) -> str:
    """Open the system calculator."""
    os.system("calc")
    return "Calculator launched successfully."

@tool
def open_notepad_tool(query: str) -> str:
    """Open the Notepad application."""
    os.system("notepad")
    return "Notepad has been opened successfully."

@tool
def get_cpu_usage_tool(query: str) -> str:
    """Retrive the current CPU usage percentage."""
    import psutil
    usage = psutil.cpu_percent(interval=1)
    return f"Current CPU usage is {usage}%."

@tool
def get_ram_usage_tool(query: str) -> str:
    """Retrive the current RAM usage and available memory."""
    import psutil
    mem = psutil.virtual_memory()
    available_md = mem.available / (1024 ** 2)
    return f"Current RAM usage is {mem.percent}% with {available_md:.2f} MB available."

@tool
def run_shell_command_tool(query:str) -> str:
    """Execute a shell command and return its output."""
    try:
        result = subprocess.run(query, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip() or "Command executed successfully."
        else:
            output = result.stderr.strip() or "Command execution failed."
        return output
    except Exception as e:
        return f"Error executing command: {str(e)}"