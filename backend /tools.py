# tools.py
class ToolAgent:
    def __init__(self):
        self.connected_tools = {}

    def connect_tools(self, tools):
        for t in tools:
            self.connected_tools[t] = "Connected"

    def status(self):
        return self.connected_tools
