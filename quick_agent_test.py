# quick_agent_test.py
# Quick and easy way to test individual agents

import sys
sys.path.append('.')

def quick_test():
    """Quick interactive agent testing"""
    
    print("🚀 Quick Agent Testing Tool")
    print("=" * 40)
    
    agents = {
        "1": "spacex_agent",
        "2": "weather_agent", 
        "3": "summary_agent",
        "4": "google_adk_agent",
        "5": "calculator_agent",
        "6": "dictionary_agent"
    }
    
    print("Select an agent to test:")
    for key, name in agents.items():
        print(f"  {key}. {name}")
    print("  0. Test all agents")
    
    choice = input("\nEnter choice (0-6): ").strip()
    
    if choice == "0":
        test_all_agents()
    elif choice in agents:
        test_single_agent(agents[choice])
    else:
        print("Invalid choice!")

def test_single_agent(agent_name):
    """Test a single agent"""
    print(f"\n🧪 Testing {agent_name}")
    print("-" * 30)
    
    try:
        if agent_name == "spacex_agent":
            from agents import spacex_agent
            result = spacex_agent.run({"goal": "Get SpaceX data"})
            
            print(f"🔍 Keys returned: {list(result.keys())}")
            
            if "spacex" in result:
                spacex_data = result["spacex"]
                print(f"✅ Mission: {spacex_data.get('mission', 'No data')}")
                print(f"📅 Date: {spacex_data.get('date', 'No data')}")
                print(f"🚀 Launchpad ID: {spacex_data.get('launchpad_id', 'No data')}")
                
                coordinates = spacex_data.get('coordinates')
                if coordinates:
                    print(f"📍 Location: {coordinates.get('name', 'Unknown')}")
                    print(f"🌍 Coordinates: {coordinates.get('latitude', 'N/A')}, {coordinates.get('longitude', 'N/A')}")
                else:
                    print("📍 No coordinates available")
            else:
                print("⚠️ No SpaceX data returned")
                print(f"   Available keys: {list(result.keys())}")
                
        elif agent_name == "weather_agent":
            from agents import weather_agent
            test_data = {
                "goal": "Get weather",
                "spacex": {
                    "coordinates": {
                        "latitude": 28.6080585,
                        "longitude": -80.6039558,
                        "name": "KSC LC 39A"
                    }
                }
            }
            result = weather_agent.run(test_data)
            
            print(f"🔍 Keys returned: {list(result.keys())}")
            
            if "weather" in result:
                weather = result["weather"]
                print(f"✅ Temperature: {weather.get('temperature', 'No data')}°F")
                print(f"💨 Wind: {weather.get('wind_speed', 'No data')} mph")
                print(f"☁️ Clouds: {weather.get('clouds', 'No data')}%")
                print(f"💧 Humidity: {weather.get('humidity', 'No data')}%")
            else:
                print("⚠️ No weather data returned")
                print(f"   Available keys: {list(result.keys())}")
                
        elif agent_name == "summary_agent":
            from agents import summary_agent
            
            user_input = input("Enter message for summary agent (or press Enter for 'hi'): ").strip()
            if not user_input:
                user_input = "hi"
                
            result = summary_agent.run({"goal": user_input})
            
            print(f"🔍 Keys returned: {list(result.keys())}")
            
            if "summary" in result:
                summary_text = result['summary']
                print(f"✅ Response: {summary_text[:200]}{'...' if len(summary_text) > 200 else ''}")
            else:
                print("⚠️ No summary generated")
                print(f"   Available keys: {list(result.keys())}")
                
        elif agent_name == "google_adk_agent":
            from agents.google_adk_agent import GoogleADKCoordinator
            
            adk = GoogleADKCoordinator()
            
            # Test planning
            test_goal = input("Enter goal for planning (or press Enter for default): ").strip()
            if not test_goal:
                test_goal = "get spacex and weather data"
                
            sequence = adk.plan_agent_sequence(test_goal)
            print(f"✅ Planned sequence: {sequence}")
            
        elif agent_name == "calculator_agent":
            from agents import calculator_agent
            
            calc_input = input("Enter calculation (or press Enter for '2 + 3'): ").strip()
            if not calc_input:
                calc_input = "calculate 2 + 3"
                
            result = calculator_agent.run({"goal": calc_input})
            
            print(f"🔍 Keys returned: {list(result.keys())}")
            
            if "calculation" in result:
                calculation = result["calculation"]
                if calculation.get("success"):
                    calculations = calculation.get("calculations", [])
                    if calculations:
                        print("✅ Calculation Results:")
                        for calc in calculations:
                            if calc.get("success"):
                                print(f"  📊 {calc['expression']} = {calc['result']}")
                            else:
                                print(f"  ❌ {calc['expression']}: {calc.get('error', 'Unknown error')}")
                    else:
                        print("✅ Calculation completed")
                else:
                    print(f"⚠️ Calculation failed: {calculation.get('error', 'Unknown error')}")
            else:
                print("⚠️ No calculation data returned")
                print(f"   Available keys: {list(result.keys())}")
                
        elif agent_name == "dictionary_agent":
            from agents import dictionary_agent
            
            word_input = input("Enter word to define (or press Enter for 'serendipity'): ").strip()
            if not word_input:
                word_input = "define serendipity"
                
            result = dictionary_agent.run({"goal": word_input})
            
            print(f"🔍 Keys returned: {list(result.keys())}")
            
            if "definition" in result:
                definition = result["definition"]
                if definition.get("success"):
                    word = definition.get("word", "")
                    definitions = definition.get("definitions", [])
                    if definitions and len(definitions) > 0:
                        first_def = definitions[0]
                        print(f"✅ Definition of '{word.upper()}':")
                        
                        # Show phonetic if available
                        phonetic = first_def.get("phonetic", "")
                        if phonetic:
                            print(f"🔊 {phonetic}")
                        
                        # Show first meaning
                        meanings = first_def.get("meanings", [])
                        if meanings:
                            first_meaning = meanings[0]
                            part_of_speech = first_meaning.get("partOfSpeech", "")
                            if part_of_speech:
                                print(f"📝 Part of speech: {part_of_speech}")
                            
                            definitions_list = first_meaning.get("definitions", [])
                            if definitions_list:
                                def_text = definitions_list[0].get("definition", "")
                                example = definitions_list[0].get("example", "")
                                print(f"📖 {def_text}")
                                if example:
                                    print(f"💡 Example: {example}")
                    else:
                        print(f"✅ Definition found for '{word}'")
                else:
                    print(f"⚠️ Definition failed: {definition.get('error', 'Unknown error')}")
            else:
                print("⚠️ No definition data returned")
                print(f"   Available keys: {list(result.keys())}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"   Details: {traceback.format_exc()}")

def test_all_agents():
    """Test all agents quickly"""
    print("\n🔄 Testing All Agents")
    print("=" * 30)
    
    agents = [
        ("SpaceX", "agents.spacex_agent", {"goal": "Get SpaceX data"}),
        ("Weather", "agents.weather_agent", {
            "goal": "Get weather",
            "spacex": {"coordinates": {"latitude": 28.6, "longitude": -80.6, "name": "Test"}}
        }),
        ("Calculator", "agents.calculator_agent", {"goal": "calculate 2 + 3"}),
        ("Dictionary", "agents.dictionary_agent", {"goal": "define test"}),
        ("Summary", "agents.summary_agent", {"goal": "hi"}),
    ]
    
    results = []
    
    for name, module_name, test_data in agents:
        try:
            module = __import__(module_name, fromlist=[module_name.split('.')[-1]])
            result = module.run(test_data)
            print(f"✅ {name}: OK")
            results.append(True)
        except Exception as e:
            print(f"❌ {name}: {e}")
            results.append(False)
    
    # Test ADK separately
    try:
        from agents.google_adk_agent import GoogleADKCoordinator
        adk = GoogleADKCoordinator()
        sequence = adk.plan_agent_sequence("test goal")
        print(f"✅ Google ADK: OK")
        results.append(True)
    except Exception as e:
        print(f"❌ Google ADK: {e}")
        results.append(False)
    
    print(f"\n📊 Results: {sum(results)}/{len(results)} agents working")

if __name__ == "__main__":
    quick_test()
