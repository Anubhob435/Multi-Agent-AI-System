# main.py

import importlib
from agents import planner
from dotenv import load_dotenv

load_dotenv()

def load_agent(name: str):
    return importlib.import_module(f"agents.{name}")

def run_goal(user_goal: str):
    sequence = planner.plan(user_goal)
    data = {"goal": user_goal}

    print(f"🧠 Planner decided the sequence: {sequence}")

    for agent_name in sequence:
        agent = load_agent(agent_name)
        data = agent.run(data)
        print(f"✅ {agent_name} output: {data}")

    print("\n🎯 Final Result:")
    print(data.get("summary", "No summary available."))

if __name__ == "__main__":
    goal = input("Enter your goal: ")
    run_goal(goal)
