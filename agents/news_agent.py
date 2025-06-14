# agents/news_agent.py

import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def run(previous_data: dict) -> dict:
    """
    News agent that fetches relevant news articles based on the goal or context.
    Uses NewsAPI to get current news articles.
    """
    goal = previous_data.get("goal", "")
    
    # Extract topics from the goal and existing data
    news_result = get_relevant_news(goal, previous_data)
    
    # Add news result to the data
    previous_data.update({"news": news_result})
    return previous_data

def get_relevant_news(goal: str, data: dict) -> dict:
    """
    Fetch relevant news based on the goal and existing data context.
    """
    try:
        # Determine search terms based on goal and existing data
        search_terms = extract_news_topics(goal, data)
        
        if not search_terms:
            return {
                "success": False,
                "error": "No relevant topics found for news search",
                "input": goal
            }
        
        # Fetch news for the most relevant topic
        primary_topic = search_terms[0]
        articles = fetch_news_articles(primary_topic)
        
        if articles:
            return {
                "success": True,
                "topic": primary_topic,
                "search_terms": search_terms,
                "articles": articles[:5],  # Limit to top 5 articles
                "total_results": len(articles),
                "input": goal
            }
        else:
            return {
                "success": False,
                "error": f"No news articles found for topic: {primary_topic}",
                "topic": primary_topic,
                "search_terms": search_terms,
                "input": goal
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"News retrieval error: {str(e)}",
            "input": goal
        }

def extract_news_topics(goal: str, data: dict) -> list:
    """
    Extract relevant news topics from the goal and existing data.
    """
    topics = []
    goal_lower = goal.lower()
    
    # Check for explicit news requests
    if any(word in goal_lower for word in ["news", "article", "headlines", "breaking", "latest"]):
        # Extract topics from goal
        if "spacex" in goal_lower or "space" in goal_lower:
            topics.append("SpaceX")
        elif "weather" in goal_lower or "climate" in goal_lower:
            topics.append("weather")
        elif "technology" in goal_lower or "tech" in goal_lower:
            topics.append("technology")
        elif "science" in goal_lower:
            topics.append("science")
        else:
            # Generic news request
            topics.append("technology")
    
    # Check existing data context for relevant topics
    if "spacex" in data:
        topics.append("SpaceX launch")
        topics.append("space exploration")
    
    if "weather" in data:
        weather_info = data.get("weather", {})
        location = weather_info.get("location", "")
        if location:
            topics.append(f"weather {location}")
    
    # Default topics if nothing specific found
    if not topics:
        if any(word in goal_lower for word in ["spacex", "launch", "rocket", "space"]):
            topics.append("SpaceX")
        elif any(word in goal_lower for word in ["weather", "climate", "storm"]):
            topics.append("weather")
        else:
            # Default to technology news
            topics.append("technology")
    
    return topics

def fetch_news_articles(topic: str) -> list:
    """
    Fetch news articles from NewsAPI for a given topic.
    """
    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            print("⚠️ NEWS_API_KEY not found in environment variables")
            return []
        
        # Calculate date for recent news (last 7 days)
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Build API URL
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': topic,
            'from': from_date,
            'sortBy': 'relevancy',
            'language': 'en',
            'pageSize': 10,
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            # Process and filter articles
            processed_articles = []
            for article in articles:
                if article.get('title') and article.get('description'):
                    processed_article = {
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'author': article.get('author', 'Unknown')
                    }
                    processed_articles.append(processed_article)
            
            return processed_articles
        else:
            print(f"⚠️ NewsAPI error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"⚠️ Error fetching news: {e}")
        return []

def format_news_for_display(news_data: dict) -> str:
    """
    Format news data for readable display.
    """
    if not news_data.get("success"):
        return f"❌ {news_data.get('error', 'Unknown error')}"
    
    topic = news_data.get("topic", "")
    articles = news_data.get("articles", [])
    
    if not articles:
        return f"📰 No recent news found for '{topic}'"
    
    output = f"📰 **Latest News: {topic.upper()}**\n\n"
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', 'No title')
        description = article.get('description', 'No description')
        source = article.get('source', 'Unknown source')
        published = article.get('published_at', '')
        
        # Format date if available
        date_str = ""
        if published:
            try:
                date_obj = datetime.fromisoformat(published.replace('Z', '+00:00'))
                date_str = f" ({date_obj.strftime('%B %d, %Y')})"
            except:
                date_str = ""
        
        output += f"**{i}. {title}**\n"
        output += f"📝 {description}\n"
        output += f"📰 Source: {source}{date_str}\n\n"
    
    return output.strip()

if __name__ == "__main__":
    # Test the news agent
    test_cases = [
        "get latest spacex news",
        "find technology news",
        "news about weather",
        "latest headlines"
    ]
    
    for test in test_cases:
        print(f"\nTest: {test}")
        result = run({"goal": test})
        print(f"Result: {result['news']}")
        if result['news'].get('success'):
            print(format_news_for_display(result['news']))