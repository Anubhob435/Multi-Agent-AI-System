# Multi-Agent AI System Roadmap

## Goal
Build a multi-agent AI system that:

- Accepts a natural-language goal
- Uses agents (modular code units) that depend on each other
- Plans and routes data from agent to agent
- Refines the result iteratively until the goal is satisfied
- Uses Google ADK (Assumed as an Android-based hardware interface or SDK-like agent wrapper)
- Uses 2–3 public APIs for enrichment (e.g., SpaceX, OpenWeatherMap, NewsAPI)

## 🔧 Tools Needed

| Tool/Tech           | Purpose                                         |
|---------------------|-------------------------------------------------|
| Python 3.12         | Language for agent logic                        |
| Flask       |         backend to simulate ADK routing agent-to-agent |
| Gemini API |          for summarizing or planning logic    |
| .env file           | Store API keys securely                         |
| APIs                | SpaceX, OpenWeatherMap, NewsAPI, CoinGecko, etc.|
| Google ADK emulator | Simulate Android ADK environment for agent chaining |
| Unit test / Pytest  | For evaluation & test trajectories              |
| NetworkX / Diagrams | Visualize agent flows                           |
| Markdown    | Documentation and test results                  |

## Roadmap: What To Do Step-by-Step

### Phase 1: Planning & Setup

1. **Define the system goal** – e.g., "Find the next SpaceX launch, check weather, analyze delay chances."

2. **Decide the agents:**
    - **Planner Agent** – Takes user goal, plans agent sequence
    - **Launch Info Agent** – Gets SpaceX data
    - **Weather Agent** – Uses location from previous to get weather
    - **Summary Agent** – Determines delay possibility

3. **Create a project folder structure:**
    ```
    multi-agent-system/
    │
    ├── agents/
    │   ├── planner.py
    │   ├── spacex_agent.py
    │   ├── weather_agent.py
    │   └── summary_agent.py
    │
    ├── main.py
    ├── .env
    ├── requirements.txt
    ├── README.md
    ├── evals/
    │   └── test_goals.json
    └── docs/
        ├── flow_diagram.png
        └── agent_logic.md
    ```

### Phase 2: Coding the Agents

- **Planner Agent:**  
  NLP-based or keyword-based goal parsing.  
  Maps task to sequence: e.g., [SpaceX → Weather → Summary]

- **SpaceX Agent:**  
  Calls SpaceX API → Gets next launch info (location, time).

- **Weather Agent:**  
  Uses OpenWeatherMap API → Uses launch site coordinates.

- **Summary Agent:**  
  Evaluates wind, cloud cover, etc. → Summarizes delay risk.

### Phase 3: Enrichment and Routing

- Each agent takes previous output as input.
- Ensure response objects pass essential data forward.
- Track agent logs or JSON messages between agents.

### Phase 4: Evaluation & Testing

- Create goal prompts (e.g., in `evals/test_goals.json`).
- Simulate:
    - Success on 1st pass
    - Failure → retry route → goal satisfied
- Log agent interactions for review.

### Phase 5: Documentation

- Diagram the flow.
- Document agent behavior.
- Add API usage instructions.
- Write a clear README.
