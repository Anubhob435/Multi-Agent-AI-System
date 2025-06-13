# 🧠 Multi-Agent AI System using Google ADK

## 📌 Overview

This is a modular, multi-agent AI system designed to accept natural language goals, plan execution routes, and pass data between cooperative agents to fulfill those goals using external APIs.

### 🧪 Example Goal
> “Find the next SpaceX launch, check weather at that location, then summarize if it may be delayed.”

---

## ⚙️ Architecture

### 👨‍💼 Agents

1. **Planner Agent**  
   Parses the user's goal and determines the routing sequence.

2. **SpaceX Agent**  
   Fetches details about the next launch using the [SpaceX API](https://github.com/r-spacex/SpaceX-API).

3. **Weather Agent**  
   Gets the weather at the launch location using [OpenWeatherMap API](https://openweathermap.org/api).

4. **Summary Agent**  
   Evaluates and summarizes whether weather might delay the launch.

---

## 🔁 Flow Diagram

