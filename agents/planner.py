# agents/planner.py

def plan(user_goal: str) -> list:
    """
    Analyzes the goal and returns a sequence of agent names.
    """
    # A simple static planner (you can use NLP later)
    if "spacex" in user_goal.lower() and "weather" in user_goal.lower():
        return ["spacex_agent", "weather_agent", "summary_agent"]
    return []
