class MemoryManager:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.conversations = {}  # Mapping from session_id to list of messages

    def load_conversation(self, session_id: str):
        """Return the conversation histroy for the given session."""
        return self.conversations.get(session_id, [])
    
    def save_message(self, session_id: str, role: str, content: str):
        """Append a message to the conversation for the given session."""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        self.conversations[session_id].append({"role": role, "content": content})
        # Keep onlt the most recent window_size messages
        if len(self.conversations[session_id]) > self.window_size:
            self.conversations[session_id] = self.conversations[session_id][-self.window_size:]

    def clear_conversation(self, session_id: str):
        """Clear the conversation history for the given session."""
        self.conversations[session_id] = []
