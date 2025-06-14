# Individual Agent Testing Guide

## Overview
This guide shows you multiple ways to test individual agents in the Multi-Agent AI System.

## Method 1: Direct Agent Testing

### Basic Agent Test
```python
# test_individual_agents.py
import sys
sys.path.append('.')

def test_spacex_agent():
    """Test SpaceX agent individually"""
    print("🧪 Testing SpaceX Agent")
    print("-" * 40)
    
    # Import the agent
    from agents import spacex_agent
    
    # Create test data
    test_data = {"goal": "Get SpaceX launch data"}
    
    try:
        # Run the agent
        result = spacex_agent.run(test_data)
        
        # Display results
        print("✅ SpaceX Agent Test Results:")
        print(f"📊 Data returned: {result.keys()}")
        if "spacex_data" in result:
            launch = result["spacex_data"].get("next_launch", {})
            print(f"🚀 Mission: {launch.get('name', 'Unknown')}")
            print(f"📅 Date: {launch.get('date', 'TBD')}")
            print(f"🚀 Rocket: {launch.get('rocket', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ SpaceX Agent Test Failed: {e}")
        return False

def test_weather_agent():
    """Test Weather agent individually"""
    print("\n🧪 Testing Weather Agent")
    print("-" * 40)
    
    from agents import weather_agent
    
    # Create test data with coordinates (simulating SpaceX data)
    test_data = {
        "goal": "Get weather data",
        "spacex": {
            "coordinates": {
                "latitude": 28.6080585,
                "longitude": -80.6039558,
                "name": "KSC LC 39A"
            }
        }
    }
    
    try:
        result = weather_agent.run(test_data)
        
        print("✅ Weather Agent Test Results:")
        print(f"📊 Data returned: {result.keys()}")
        if "weather" in result:
            weather = result["weather"]
            print(f"🌡️ Temperature: {weather.get('temperature', 'N/A')}°F")
            print(f"💨 Wind Speed: {weather.get('wind_speed', 'N/A')} mph")
            print(f"☁️ Cloud Cover: {weather.get('clouds', 'N/A')}%")
        
        return True
    except Exception as e:
        print(f"❌ Weather Agent Test Failed: {e}")
        return False

def test_summary_agent():
    """Test Summary agent individually"""
    print("\n🧪 Testing Summary Agent")
    print("-" * 40)
    
    from agents import summary_agent
    
    # Test conversational input
    test_data = {"goal": "hi there"}
    
    try:
        result = summary_agent.run(test_data)
        
        print("✅ Summary Agent Test Results:")
        print(f"📊 Data returned: {result.keys()}")
        if "summary" in result:
            summary = result["summary"]
            print(f"📝 Summary: {summary[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ Summary Agent Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔬 Individual Agent Testing Suite")
    print("=" * 50)
    
    results = []
    results.append(test_spacex_agent())
    results.append(test_weather_agent())
    results.append(test_summary_agent())
    
    print("\n📊 Test Summary:")
    print("=" * 30)
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
```

## Method 2: Using Main System's Extract Function

```python
# test_with_extraction.py
import sys
sys.path.append('.')

from main import extract_agent_output

def test_agent_with_extraction():
    """Test agent and use the main system's output extraction"""
    from agents import spacex_agent
    
    print("🧪 Testing with Output Extraction")
    print("-" * 40)
    
    # Test data
    test_data = {"goal": "Get SpaceX data"}
    
    # Run agent
    previous_data = test_data.copy()
    result = spacex_agent.run(test_data)
    
    # Extract formatted output
    formatted_output = extract_agent_output("spacex_agent", result, previous_data)
    
    print("📊 Formatted Agent Output:")
    print(formatted_output)
    
    return result

if __name__ == "__main__":
    test_agent_with_extraction()
```

## Method 3: Interactive Agent Testing

```python
# interactive_agent_test.py
import sys
sys.path.append('.')

def interactive_test():
    """Interactive testing of individual agents"""
    
    agents = {
        "1": ("spacex_agent", "SpaceX Launch Data"),
        "2": ("weather_agent", "Weather Information"),
        "3": ("summary_agent", "Summary & Conversation"),
        "4": ("google_adk_agent", "Google ADK Coordinator")
    }
    
    print("🔬 Interactive Agent Testing")
    print("=" * 40)
    print("Available Agents:")
    for key, (name, desc) in agents.items():
        print(f"{key}. {name} - {desc}")
    
    choice = input("\nSelect agent to test (1-4): ")
    
    if choice in agents:
        agent_name, desc = agents[choice]
        print(f"\n🧪 Testing {agent_name}")
        print("-" * 30)
        
        # Import and test the selected agent
        agent_module = __import__(f"agents.{agent_name}", fromlist=[agent_name])
        
        # Create test data based on agent
        if agent_name == "spacex_agent":
            test_data = {"goal": "Get SpaceX launch data"}
        elif agent_name == "weather_agent":
            test_data = {
                "goal": "Get weather data",
                "spacex": {
                    "coordinates": {
                        "latitude": 28.6080585,
                        "longitude": -80.6039558,
                        "name": "KSC LC 39A"
                    }
                }
            }
        elif agent_name == "summary_agent":
            test_input = input("Enter message for summary agent: ") or "hi"
            test_data = {"goal": test_input}
        else:
            test_data = {"goal": "Test ADK coordinator"}
        
        try:
            result = agent_module.run(test_data)
            print("\n✅ Agent Test Results:")
            print("=" * 30)
            for key, value in result.items():
                if isinstance(value, dict):
                    print(f"{key}: {type(value).__name__} with {len(value)} items")
                else:
                    preview = str(value)[:100]
                    print(f"{key}: {preview}{'...' if len(str(value)) > 100 else ''}")
                    
        except Exception as e:
            print(f"❌ Test failed: {e}")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    interactive_test()
```

## Method 4: Pytest-style Testing

```python
# test_agents_pytest.py
import pytest
import sys
sys.path.append('.')

class TestIndividualAgents:
    
    def test_spacex_agent_basic(self):
        """Test SpaceX agent returns required data structure"""
        from agents import spacex_agent
        
        test_data = {"goal": "Get SpaceX data"}
        result = spacex_agent.run(test_data)
        
        assert "goal" in result
        assert isinstance(result, dict)
        # Add more assertions based on expected structure
    
    def test_weather_agent_with_coordinates(self):
        """Test Weather agent with provided coordinates"""
        from agents import weather_agent
        
        test_data = {
            "goal": "Get weather",
            "spacex": {
                "coordinates": {
                    "latitude": 28.6080585,
                    "longitude": -80.6039558,
                    "name": "Test Location"
                }
            }
        }
        
        result = weather_agent.run(test_data)
        
        assert "goal" in result
        assert isinstance(result, dict)
    
    def test_summary_agent_conversation(self):
        """Test Summary agent with conversational input"""
        from agents import summary_agent
        
        test_data = {"goal": "hello"}
        result = summary_agent.run(test_data)
        
        assert "goal" in result
        assert "summary" in result
        assert isinstance(result["summary"], str)
        assert len(result["summary"]) > 0

# Run with: python -m pytest test_agents_pytest.py -v
```

## Method 5: Agent Performance Testing

```python
# test_agent_performance.py
import sys
import time
sys.path.append('.')

def performance_test():
    """Test agent performance and response times"""
    
    from agents import spacex_agent, weather_agent, summary_agent
    
    agents = [
        ("spacex_agent", spacex_agent, {"goal": "Get SpaceX data"}),
        ("weather_agent", weather_agent, {
            "goal": "Get weather",
            "spacex": {"coordinates": {"latitude": 28.6, "longitude": -80.6, "name": "Test"}}
        }),
        ("summary_agent", summary_agent, {"goal": "hi"})
    ]
    
    print("⏱️ Agent Performance Testing")
    print("=" * 40)
    
    for name, agent, test_data in agents:
        print(f"\n🔄 Testing {name}...")
        
        start_time = time.time()
        try:
            result = agent.run(test_data)
            end_time = time.time()
            
            execution_time = end_time - start_time
            data_size = len(str(result))
            
            print(f"✅ {name}:")
            print(f"   ⏱️ Execution time: {execution_time:.3f} seconds")
            print(f"   📊 Data size: {data_size} characters")
            print(f"   🔑 Keys returned: {list(result.keys())}")
            
        except Exception as e:
            print(f"❌ {name} failed: {e}")

if __name__ == "__main__":
    performance_test()
```

## Usage Examples:

### Quick Test Single Agent:
```bash
python -c "
import sys; sys.path.append('.')
from agents import spacex_agent
result = spacex_agent.run({'goal': 'test'})
print('Keys:', list(result.keys()))
"
```

### Test With Main System Integration:
```bash
echo 'spacex launch data' | python main.py
# This will show individual agent outputs
```

### Run Comprehensive Test Suite:
```bash
python test_individual_agents.py
```

## Testing Tips:

1. **Mock Data**: For weather agent, provide mock coordinates
2. **API Keys**: Ensure environment variables are set
3. **Error Handling**: Test both success and failure cases
4. **Data Structure**: Verify returned data format
5. **Integration**: Test how agents work together

## Common Test Scenarios:

- **SpaceX Agent**: Test with/without API access
- **Weather Agent**: Test with/without coordinates
- **Summary Agent**: Test conversational vs analytical inputs
- **ADK Agent**: Test planning and validation functions
