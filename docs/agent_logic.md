# 🧠 Agent Logic Documentation

## Overview

This document details the architecture, logic, and data flow of our Multi-Agent AI System using Google ADK integration.

## 🏗️ System Architecture

### Core Components

1. **Google ADK Coordinator** - Intelligent planning and validation using Google's Gemini API
2. **Agent Pipeline** - Sequential execution of specialized agents
3. **Data Enrichment** - Each agent adds and enriches data for the next
4. **Automated Evaluation** - Comprehensive testing and quality assessment

## 🤖 Agent Specifications

### 1. Google ADK Agent (`google_adk_agent.py`)

**Purpose**: Intelligent coordination and validation using Google's Gemini API

**Key Functions**:
- `plan_agent_sequence()`: Uses Gemini to determine optimal agent execution order
- `validate_goal_completion()`: Evaluates goal satisfaction and provides improvement suggestions

**Input**: User goal string
**Output**: Agent sequence plan OR validation report with confidence scores

**Example Output**:
```json
{
  "goal_achieved": true,
  "confidence": 95,
  "missing_data": [],
  "suggested_improvements": ["Include more detailed weather analysis"],
  "quality_score": 90
}
```

### 2. Planner Agent (`planner.py`)

**Purpose**: Fallback planning when Google ADK is unavailable

**Logic**:
- Keyword-based pattern matching
- Supports multiple goal variations
- Returns agent sequence based on detected patterns

**Input**: User goal string
**Output**: List of agent names in execution order

### 3. SpaceX Agent (`spacex_agent.py`)

**Purpose**: Fetch SpaceX launch data and resolve launchpad coordinates

**API Integration**: 
- `https://api.spacexdata.com/v4/launches/next`
- `https://api.spacexdata.com/v4/launchpads/{id}`

**Data Flow**:
1. Fetch next launch information
2. Extract launchpad ID
3. Resolve launchpad to coordinates
4. Return enriched launch data

**Output Structure**:
```json
{
  "spacex": {
    "mission": "USSF-44",
    "date": "2022-11-01T13:41:00.000Z",
    "launchpad_id": "5e9e4502f509094188566f88",
    "coordinates": {
      "latitude": 28.6080585,
      "longitude": -80.6039558,
      "name": "KSC LC 39A",
      "location": "Cape Canaveral"
    }
  }
}
```

### 4. Weather Agent (`weather_agent.py`)

**Purpose**: Get weather data for launch location coordinates

**API Integration**: OpenWeatherMap API
**Dependencies**: Requires coordinates from SpaceX agent

**Logic**:
1. Extract coordinates from previous SpaceX data
2. Fallback to Kennedy Space Center if coordinates unavailable
3. Fetch current weather conditions
4. Return comprehensive weather data

**Output Structure**:
```json
{
  "weather": {
    "location": "KSC LC 39A",
    "latitude": 28.6080585,
    "longitude": -80.6039558,
    "temperature": 25.29,
    "wind_speed": 4.5,
    "clouds": 82,
    "condition": "broken clouds",
    "humidity": 90
  }
}
```

### 5. Summary Agent (`summary_agent.py`)

**Purpose**: Analyze collected data and determine launch delay probability

**Logic**:
- Evaluates wind speed (>30 = potential delay)
- Evaluates cloud coverage (>70 = potential delay) 
- Generates human-readable summary

**Output**: Summary string with delay assessment

## 🔄 Data Flow

```
User Goal → Google ADK Planning → Agent Sequence → Data Enrichment → Validation
    ↓              ↓                    ↓               ↓              ↓
"Find next    ["spacex_agent",    SpaceX Data →   Weather Data → Summary +
SpaceX        "weather_agent",        +               +         Validation
launch..."    "summary_agent"]   Coordinates     Analysis        Score
```

### Data Structure Evolution

**Initial**: `{"goal": "user_goal_string"}`

**After SpaceX Agent**: 
```json
{
  "goal": "...",
  "spacex": { "mission": "...", "coordinates": {...} }
}
```

**After Weather Agent**:
```json
{
  "goal": "...",
  "spacex": {...},
  "weather": { "temperature": 25.29, "wind_speed": 4.5, ... }
}
```

**After Summary Agent**:
```json
{
  "goal": "...",
  "spacex": {...},
  "weather": {...},
  "summary": "Launch might be delayed due to weather conditions."
}
```

**After ADK Validation**:
```json
{
  "goal": "...",
  "spacex": {...},
  "weather": {...}, 
  "summary": "...",
  "adk_validation": { "goal_achieved": true, "confidence": 95, ... }
}
```

## 🔍 Error Handling

### Graceful Degradation
- Google ADK failures → Fallback to basic planner
- API failures → Informative error messages
- Missing data → Default values with warnings

### Retry Logic
- Weather API failures include error codes
- SpaceX API has redundant endpoint calls
- Validation provides confidence scores for reliability

## 📊 Quality Metrics

### ADK Validation Scoring
- **Confidence**: 0-100 (goal achievement likelihood)
- **Quality Score**: 0-100 (data completeness and accuracy)
- **Goal Achievement**: Boolean (was the goal satisfied)

### Performance Metrics
- **Execution Time**: Average 4.13s per goal
- **Success Rate**: 100% in current test suite
- **Agent Sequence Accuracy**: Google ADK vs fallback comparison

## 🧪 Testing Strategy

### Automated Evaluation
- Multiple goal variations tested
- Expected data keys validation
- Performance and accuracy metrics
- Comprehensive result logging

### Test Cases
1. Complete SpaceX + Weather scenarios
2. Single-agent scenarios
3. Edge cases and error conditions
4. Performance benchmarks

## 🔄 Iterative Improvement

### ADK Suggestions Integration
The system automatically provides suggestions for enhancement:
- More detailed weather analysis
- Probability-based delay predictions  
- Source attribution for transparency
- Time-sensitive data handling

### Continuous Learning
- Results logged for pattern analysis
- Performance metrics tracked over time
- Error patterns identified for improvement