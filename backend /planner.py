# planner.py
from datetime import datetime, timedelta
from executor import ExecutorAgent
from advisor import AdvisorAgent
from emotion_model import EmotionModel
from mcp import MCPAgent
from rag_index import RAGAgent
from tools import ToolAgent

# =========================
# 🧩 Planner Agent
# =========================
class PlannerAgent:
    """Coordinates multi-agent planning with emotion awareness."""
    def __init__(self):
        self.strategies = {
            "joy": "You're in a great mood! Take advantage of it — handle creative or challenging tasks first.",
            "sadness": "Be kind to yourself today. Focus on light, rewarding tasks that help rebuild energy.",
            "fear": "Break things into smaller, actionable steps. Avoid overloading yourself.",
            "anger": "Direct your energy productively — quick, result-driven tasks work best now.",
            "neutral": "Steady and focused — a great time for consistent progress.",
        }

    def generate_plan(self, emotion, tasks, start_time=None, task_interval=60):
        if not tasks:
            return {"error": "No tasks provided."}

        motivation = self.strategies.get(emotion, self.strategies["neutral"])

        if start_time is None:
            start_time = datetime.now()

        plan = []
        current_time = start_time
        for i, task in enumerate(tasks):
            time_slot = current_time.strftime("%I:%M %p")
            plan.append({
                "time": time_slot,
                "task": task,
                "priority": self._assign_priority(i, emotion),
                "status": "Pending"
            })
            current_time += timedelta(minutes=task_interval)

        return {"emotion": emotion, "motivation": motivation, "plan": plan}

    def _assign_priority(self, index, emotion):
        if emotion in ["anger", "joy"]:
            return "High" if index < 2 else "Medium"
        elif emotion == "sadness":
            return "Low" if index > 1 else "Medium"
        return "High" if index == 0 else "Medium" if index < 3 else "Low"


# =========================
# 🔗 Coordinator Function
# =========================
def generate_emotion_aware_plan(user_text, tasks):
    emotion_model = EmotionModel()
    detected_emotion = emotion_model.detect_emotion(user_text)
    emotion = detected_emotion.get("emotion", "neutral")

    planner = PlannerAgent()
    executor = ExecutorAgent()
    advisor = AdvisorAgent()
    rag = RAGAgent()
    mcp = MCPAgent()
    tools = ToolAgent()

    # Generate base plan
    plan = planner.generate_plan(emotion, tasks)

    # Execute plan simulation
    executed_plan = executor.execute_plan(plan)

    # Advisor tips
    advice = advisor.generate_advice(emotion, tasks)

    # Integrations
    rag.connect()
    mcp.connect()
    tools.connect_tools(["calendar_api", "reminder_bot"])

    result = {
        "emotion": emotion,
        "motivation": plan["motivation"],
        "plan": executed_plan,
        "advisor_notes": advice,
        "integrations": {
            "RAG": rag.status(),
            "MCP": mcp.status(),
            "Tools": tools.status()
        },
        "execution_summary": executor.summary()
    }

    return result


# Example usage
if __name__ == "__main__":
    user_text = "I'm feeling quite motivated today but a bit nervous."
    tasks = ["Finish ML notes", "Workout", "Write blog"]
    from pprint import pprint
    pprint(generate_emotion_aware_plan(user_text, tasks))
