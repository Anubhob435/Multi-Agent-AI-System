# agents/summary_agent.py

def run(previous_data: dict) -> dict:
    """
    Enhanced summary agent that can handle conversational inputs and data analysis.
    """
    goal = previous_data.get("goal", "").lower().strip()
    
    # Handle conversational/greeting inputs
    conversational_patterns = [
        "hi", "hello", "hey", "good morning", "good afternoon", "good evening",
        "how are you", "what's up", "help", "thanks", "thank you", "bye", "goodbye"
    ]
    
    if any(pattern in goal for pattern in conversational_patterns):
        if any(greeting in goal for greeting in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
            summary = "Hello! I'm the Multi-Agent AI System. I can help you with:\n\n• SpaceX launch information and schedules\n• Weather conditions and forecasts\n• Launch readiness analysis\n• Multi-agent coordination tasks\n\nJust tell me what you'd like to know!"
        elif "how are you" in goal or "what's up" in goal:
            summary = "I'm doing great! All my agents are online and ready to help. I'm equipped with SpaceX, Weather, and Summary agents, all coordinated by Google ADK. What can I help you with today?"
        elif "help" in goal or "what can you do" in goal:
            summary = "I'm a multi-agent AI system that can:\n\n🚀 **SpaceX Agent**: Get launch schedules, mission details, and rocket information\n🌍 **Weather Agent**: Provide weather conditions and forecasts\n📝 **Summary Agent**: Analyze data and provide insights\n🧠 **Google ADK**: Coordinate and validate multi-agent workflows\n\nTry asking me something like:\n• 'Find the next SpaceX launch and check weather conditions'\n• 'What's the weather like for rocket launches?'\n• 'Tell me about the next SpaceX mission'"
        elif any(thanks in goal for thanks in ["thanks", "thank you"]):
            summary = "You're welcome! I'm always here to help with your questions about SpaceX launches, weather data, or any multi-agent tasks. Feel free to ask me anything!"
        elif any(bye in goal for bye in ["bye", "goodbye"]):
            summary = "Goodbye! Come back anytime if you need help with SpaceX launches, weather analysis, or any other multi-agent tasks. Have a great day!"
        else:
            summary = "Hello! I'm your Multi-Agent AI assistant. I'm here to help with SpaceX launches, weather analysis, and coordinated AI tasks. What would you like to know?"
    
    # Handle "what can you do" or capability questions
    elif any(phrase in goal for phrase in ["what can you do", "what are you", "who are you", "capabilities"]):
        summary = "I'm a Multi-Agent AI System with specialized capabilities:\n\n🚀 **SpaceX Intelligence**: Real-time launch schedules, mission data, and rocket information\n🌍 **Weather Analysis**: Location-based weather conditions and forecasting\n📝 **Smart Summarization**: Data analysis and insights generation\n🧠 **ADK Coordination**: Intelligent workflow planning and validation\n\nI can handle complex multi-step tasks like analyzing launch readiness by checking both SpaceX schedules and weather conditions simultaneously!"
    
    # Handle data analysis (original functionality)
    else:
        weather = previous_data.get("weather", {})
        spacex_data = previous_data.get("spacex_data", {})
        
        if weather and spacex_data:
            # Multi-agent analysis
            wind = weather.get("wind_speed", 0)
            clouds = weather.get("clouds", 0)
            delay = wind > 30 or clouds > 70
            
            launch_info = spacex_data.get("next_launch", {})
            launch_name = launch_info.get("name", "Unknown Mission")
            
            if delay:
                summary = f"🚀 **{launch_name}** analysis:\n\n⚠️ **Weather Concern**: Current conditions show high winds ({wind} mph) or cloud cover ({clouds}%). Launch might be delayed due to weather conditions.\n\n📊 **Recommendation**: Monitor weather conditions closely before launch."
            else:
                summary = f"🚀 **{launch_name}** analysis:\n\n✅ **Weather Clear**: Conditions are favorable with manageable winds ({wind} mph) and cloud cover ({clouds}%). Launch is likely to proceed as planned.\n\n🎯 **Status**: Ready for launch!"
        
        elif weather:
            # Weather-only analysis
            wind = weather.get("wind_speed", 0)
            clouds = weather.get("clouds", 0)
            temp = weather.get("temperature", 0)
            
            summary = f"🌍 **Weather Analysis**:\n\n🌡️ Temperature: {temp}°F\n💨 Wind Speed: {wind} mph\n☁️ Cloud Cover: {clouds}%\n\n{'⚠️ Conditions may impact launch operations' if wind > 30 or clouds > 70 else '✅ Weather conditions are favorable'}"
        
        elif spacex_data:
            # SpaceX-only analysis
            launch_info = spacex_data.get("next_launch", {})
            summary = f"🚀 **SpaceX Mission Summary**:\n\n📅 Next Launch: {launch_info.get('name', 'Unknown')}\n🕐 Date: {launch_info.get('date', 'TBD')}\n🚀 Vehicle: {launch_info.get('rocket', 'Unknown')}\n📍 Location: {launch_info.get('launchpad', 'Unknown')}"
        
        else:
            # Default response for unrecognized goals
            summary = f"I've analyzed your request: '{goal}'\n\nI'm ready to help! Try asking me about:\n• SpaceX launches and missions\n• Weather conditions\n• Multi-agent task coordination\n\nFor example: 'Find the next SpaceX launch and check weather conditions'"

    previous_data.update({"summary": summary})
    return previous_data
