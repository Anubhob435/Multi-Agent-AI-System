# agents/planner.py

def plan(user_goal: str) -> list:
    """
    Enhanced planner that can handle more goal variations.
    This serves as a fallback when Google ADK is not available.
    """
    goal_lower = user_goal.lower()
    
    # SpaceX + Weather pattern
    if any(keyword in goal_lower for keyword in ["spacex", "launch", "rocket"]) and \
       any(keyword in goal_lower for keyword in ["weather", "climate", "condition"]):
        return ["spacex_agent", "weather_agent", "summary_agent"]
    
    # Weather only pattern  
    elif any(keyword in goal_lower for keyword in ["weather", "temperature", "climate", "forecast"]):
        return ["weather_agent", "summary_agent"]
        
    # SpaceX only pattern
    elif any(keyword in goal_lower for keyword in ["spacex", "launch", "rocket", "mission"]):
        return ["spacex_agent", "summary_agent"]
        
    # News pattern
    elif any(keyword in goal_lower for keyword in ["news", "article", "current events"]):
        return ["news_agent", "summary_agent"]
    
    # Default: try a comprehensive approach
    else:
        print("⚠️ Goal pattern not recognized, trying comprehensive agent sequence")
        return ["spacex_agent", "weather_agent", "summary_agent"]
