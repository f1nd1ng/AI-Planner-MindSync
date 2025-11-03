# rag_index.py
class RAGAgent:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
        return "RAG connected."

    def status(self):
        return "Active" if self.connected else "Inactive"
