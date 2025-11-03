# advisor.py
class AdvisorAgent:
    def generate_advice(self, emotion, tasks):
        tips = {
            "joy": "You're full of energy! Start with creative work first.",
            "sadness": "Try a walk or music between tasks to lift your mood.",
            "fear": "Focus on easy wins first to rebuild confidence.",
            "anger": "Take breaks often; redirect that fire into results.",
            "neutral": "Perfect time for consistent progress."
        }
        return f"Advice: {tips.get(emotion, 'Stay balanced today.')} You have {len(tasks)} tasks ahead."
