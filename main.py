import requests
import json
from datetime import datetime
import re
import os

class SimpleAIAgent:
    def __init__(self):
        # You'll need to get free API keys for these services
        self.weather_api_key = os.environ.get("OPENWEATHER_API_KEY")  # Get from openweathermap.org
        self.news_api_key = os.environ.get("NEWS_API_KEY")  # Get from newsapi.org

        # Agent's knowledge base
        self.capabilities = [
            "check weather",
            "get news",
            "tell time",
            "simple math",
            "greet user"
        ]
    
    def process_input(self, user_input):
        """Process user input and determine intent"""
        user_input = user_input.lower().strip()
        
        # Simple intent detection using keywords
        if any(word in user_input for word in ["weather", "temperature", "forecast"]):
            return "weather", self.extract_location(user_input)
        elif any(word in user_input for word in ["news", "headlines", "latest"]):
            return "news", self.extract_topic(user_input)
        elif any(word in user_input for word in ["time", "clock", "now"]):
            return "time", None
        elif any(word in user_input for word in ["calculate", "math", "+", "-", "*", "/"]):
            return "math", user_input
        elif any(word in user_input for word in ["hello", "hi", "hey", "greetings"]):
            return "greeting", None
        elif any(word in user_input for word in ["help", "capabilities", "what can you do"]):
            return "help", None
        else:
            return "unknown", user_input
    
    def extract_location(self, text):
        """Extract location from weather request"""
        # Simple regex to find city names (this is basic - real agents use NLP)
        words = text.split()
        # Look for words after "in" or "for"
        for i, word in enumerate(words):
            if word in ["in", "for"] and i + 1 < len(words):
                return words[i + 1].title()
        return "London"  # Default location
    
    def extract_topic(self, text):
        """Extract topic from news request"""
        words = text.split()
        for i, word in enumerate(words):
            if word in ["about", "on"] and i + 1 < len(words):
                return words[i + 1]
        return "general"  # Default topic
    
    def get_weather(self, location):
        """Fetch weather data"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"Weather in {location}: {temp}°C, {description}"
            else:
                return f"Sorry, I couldn't get weather data for {location}"
        except:
            return "Weather service is currently unavailable"
    
    def get_news(self, topic):
        """Fetch news headlines"""
        try:
            if topic == "general":
                url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.news_api_key}"
            else:
                url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={self.news_api_key}&sortBy=popularity"
            
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data['articles']:
                headlines = []
                for article in data['articles'][:3]:  # Get top 3
                    headlines.append(f"• {article['title']}")
                return f"Latest news about {topic}:\n" + "\n".join(headlines)
            else:
                return f"Sorry, I couldn't find news about {topic}"
        except:
            return "News service is currently unavailable"
    
    def get_time(self):
        """Get current time"""
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def do_math(self, expression):
        """Simple calculator"""
        try:
            # Extract numbers and operators (basic security - don't eval arbitrary code!)
            if re.match(r'^[\d\+\-\*\/\.\s\(\)]+$', expression):
                result = eval(expression)
                return f"Result: {result}"
            else:
                return "Sorry, I can only do basic math operations"
        except:
            return "Sorry, I couldn't calculate that"
    
    def greet_user(self):
        """Friendly greeting"""
        return "Hello! I'm your AI assistant. I can help with weather, news, time, and simple math. What would you like to know?"
    
    def show_help(self):
        """Show available capabilities"""
        return f"I can help you with: {', '.join(self.capabilities)}. Just ask me something!"
    
    def execute_action(self, intent, data):
        """Execute the determined action"""
        if intent == "weather":
            return self.get_weather(data)
        elif intent == "news":
            return self.get_news(data)
        elif intent == "time":
            return self.get_time()
        elif intent == "math":
            return self.do_math(data)
        elif intent == "greeting":
            return self.greet_user()
        elif intent == "help":
            return self.show_help()
        else:
            return "I'm not sure how to help with that. Try asking about weather, news, time, or math!"
    
    def respond(self, user_input):
        """Main method to process input and generate response"""
        print(f"User: {user_input}")
        
        # Step 1: Process input and determine intent
        intent, data = self.process_input(user_input)
        print(f"Agent thinking: Intent='{intent}', Data='{data}'")
        
        # Step 2: Execute appropriate action
        response = self.execute_action(intent, data)
        
        # Step 3: Return response
        print(f"Agent: {response}")
        return response

# Example usage and testing
def main():
    agent = SimpleAIAgent()
    
    print("=== Simple AI Agent Demo ===")
    print("Note: You'll need to add your API keys to make weather and news work!")
    print()
    
    # Test cases
    test_inputs = [
        "Hello there!",
        "What can you do?",
        "What's the weather in Paris?",
        "Get me news about technology",
        "What time is it?",
        "Calculate 15 * 8 + 4",
        "Tell me a joke"  # This should trigger unknown intent
    ]
    
    for test_input in test_inputs:
        agent.respond(test_input)
        print("-" * 50)

if __name__ == "__main__":
    main()