# executor.py
import random

class ExecutorAgent:
    def __init__(self):
        self.completed_tasks = []

    def execute_plan(self, plan):
        for task in plan["plan"]:
            task["status"] = random.choice(["✅ Completed", "⏳ In Progress", "🔜 Pending"])
            if "Completed" in task["status"]:
                self.completed_tasks.append(task["task"])
        return plan

    def summary(self):
        return {
            "completed": len(self.completed_tasks),
            "tasks_completed": self.completed_tasks
        }
