# agents/summary_agent.py

def run(previous_data: dict) -> dict:
    """
    Analyzes weather to check for possible launch delay.
    """
    weather = previous_data.get("weather", {})
    wind = weather.get("wind_speed", 0)
    clouds = weather.get("clouds", 0)

    delay = wind > 30 or clouds > 70
    summary = "Launch might be delayed due to weather conditions." if delay else "Launch is likely to proceed as planned."

    previous_data.update({"summary": summary})
    return previous_data
