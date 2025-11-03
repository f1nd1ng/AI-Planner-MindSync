# mcp.py
"""
Multi-Agent Controller for MindSync: Emotion-Aware AI Task Planner

This module coordinates Planner, Advisor, and Executor agents in sequence:
    1. Planner → generates structured task plan.
    2. Advisor → reviews and adjusts based on emotional context.
    3. Executor → produces final schedule or calendar events.
"""

from planner import generate_emotion_aware_plan
from advisor import generate_advice
from executor import execute_plan

def run_multi_agent_plan(user_mood: str, user_tasks: list, user_context: str = ""):
    """
    Orchestrates all 3 agents to produce a coherent emotion-aware plan.
    
    Args:
        user_mood (str): Detected or input emotion.
        user_tasks (list): List of task names or dicts.
        user_context (str): Optional background info (stress level, deadlines, etc.)
    
    Returns:
        dict: Final output with plan, advice, and execution summary.
    """

    result = {}

    # 🧩 Step 1 — Planner
    try:
        print("[MCP] Running Planner Agent...")
        plan = generate_emotion_aware_plan(user_mood, user_tasks)
        result["plan"] = plan
    except Exception as e:
        print("[MCP] Planner failed:", e)
        result["error"] = f"Planner failed: {e}"
        return result

    # 💬 Step 2 — Advisor
    try:
        print("[MCP] Running Advisor Agent...")
        advice = generate_advice(user_mood, plan, user_context)
        result["advice"] = advice
    except Exception as e:
        print("[MCP] Advisor failed:", e)
        result["advice"] = f"Advisor failed: {e}"

    # ⚙️ Step 3 — Executor
    try:
        print("[MCP] Running Executor Agent...")
        execution_result = execute_plan(plan)
        result["execution"] = execution_result
    except Exception as e:
        print("[MCP] Executor failed:", e)
        result["execution"] = f"Executor failed: {e}"

    print("[MCP] Multi-agent pipeline completed successfully.")
    return result


# Optional: quick test hook
if __name__ == "__main__":
    sample_tasks = ["Finish report", "Study ML paper", "Go for a walk"]
    out = run_multi_agent_plan("stressed", sample_tasks)
    print(out)
