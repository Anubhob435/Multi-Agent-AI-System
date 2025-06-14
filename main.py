# main.py

import importlib
from agents import planner
from agents.google_adk_agent import GoogleADKCoordinator
from dotenv import load_dotenv

load_dotenv()

def load_agent(name: str):
    return importlib.import_module(f"agents.{name}")

def run_goal(user_goal: str):
    # Use Google ADK for intelligent planning
    try:
        adk = GoogleADKCoordinator()
        sequence = adk.plan_agent_sequence(user_goal)
        print(f"🧠 Google ADK Planner decided the sequence: {sequence}")
    except Exception as e:
        print(f"⚠️ Falling back to basic planner due to: {e}")
        sequence = planner.plan(user_goal)
        print(f"🧠 Basic Planner decided the sequence: {sequence}")
    
    data = {"goal": user_goal}
    print(f"📋 Starting execution with {len(sequence)} agents")

    for i, agent_name in enumerate(sequence, 1):
        print(f"🔄 [{i}/{len(sequence)}] Executing {agent_name}...")
        agent = load_agent(agent_name)
        data = agent.run(data)
        print(f"✅ {agent_name} completed successfully")

    # Add Google ADK validation at the end
    try:
        print("🔍 Running Google ADK validation...")
        adk_agent = load_agent("google_adk_agent")
        data = adk_agent.run(data)
        validation = data.get('adk_validation', {})
        print(f"� ADK Validation - Confidence: {validation.get('confidence', 0)}%, Quality: {validation.get('quality_score', 0)}%")
    except Exception as e:
        print(f"⚠️ ADK validation failed: {e}")

    print("\n🎯 Final Result:")
    print(data.get("summary", "No summary available."))
    
    return data

if __name__ == "__main__":
    goal = input("Enter your goal: ")
    run_goal(goal)
