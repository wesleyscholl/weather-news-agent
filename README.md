# 🌦️📰 Weather & News AI Agent

A simple AI agent that demonstrates basic intent detection, API integration, and natural language understanding without complex LLM dependencies.

## Features

- 🌤️ **Weather Forecasts** - Get current weather for any city via OpenWeatherMap API
- 📰 **News Headlines** - Fetch latest news by topic using NewsAPI
- 🕐 **Time & Date** - Simple datetime queries
- 🧮 **Basic Math** - Calculator functionality
- 💬 **Natural Language** - Keyword-based intent detection

## Quick Start

```bash
# Clone the repository
git clone https://github.com/wesleyscholl/weather-news-agent.git
cd weather-news-agent

# Set up environment variables
export OPENWEATHER_API_KEY="your_key_here"  # Get from openweathermap.org
export NEWS_API_KEY="your_key_here"         # Get from newsapi.org

# Run the agent
./run.sh
```

## Example Interactions

```
You: What's the weather in London?
Agent: Current weather in London: 15°C, Partly Cloudy

You: Show me tech news
Agent: Top headlines about tech:
1. New AI Model Released...
2. Tech Company Announces...

You: What time is it?
Agent: Current time: 2024-10-31 14:30:45

You: Calculate 25 * 4
Agent: Result: 100
```

## Project Structure

```
weather-news-agent/
├── main.py          # Core agent logic
├── run.sh           # Startup script
├── myenv/           # Python virtual environment
└── README.md        # This file
```

## 📊 Project Status

**Status:** ✅ **Educational Demo Complete**

### Current Capabilities
- ✅ Simple intent detection using keyword matching
- ✅ Weather API integration (OpenWeatherMap)
- ✅ News API integration (NewsAPI.org)
- ✅ Basic natural language parsing
- ✅ Error handling and fallbacks
- ✅ Command-line interface

### What This Demonstrates
- **No LLM Required:** Shows how far you can get with simple NLP
- **API Integration:** Clean patterns for external services
- **Intent Detection:** Keyword-based vs. ML-based approaches
- **Agent Architecture:** Basic structure for conversational AI
- **Free Tier Friendly:** Uses free APIs with generous limits

## 🗺️ Roadmap

### v1.1 (Future)
- 📋 Add more intents (reminders, todos, searches)
- 📋 Improve NER (Named Entity Recognition) for better parsing
- 📋 Add conversation history and context
- 📋 Web UI with Streamlit or Flask

### v2.0 (LLM Integration)
- 📋 Optional LLM for better intent classification
- 📋 Natural language generation for responses
- 📋 Multi-turn conversations with memory
- 📋 Integration with more APIs (calendar, email, etc.)

## 🎯 Next Steps

### For Learning
1. Study the intent detection logic in `main.py`
2. Try adding a new capability (e.g., jokes, facts)
3. Experiment with different NLP approaches
4. Compare with LLM-based solutions

### For Building
1. Fork and extend with your own APIs
2. Add a web interface
3. Integrate with voice assistants
4. Build mobile app wrapper

## 💡 Use Cases

- **Education:** Learn agent architecture basics
- **Prototyping:** Quick proof-of-concept for simple agents
- **Low-Cost Deployment:** No expensive LLM API calls
- **Local-First:** Runs without cloud dependencies (except APIs)
- **Gateway Drug:** Step into AI agents without complexity

## API Keys

### OpenWeatherMap (Free Tier)
- Sign up at https://openweathermap.org/api
- 1,000 calls/day free
- 60 calls/minute

### NewsAPI (Free Tier)
- Sign up at https://newsapi.org/
- 100 requests/day free
- Development use only

## 🤝 Contributing

This is an educational project. Contributions welcome:
- Add new intents and capabilities
- Improve NLP parsing
- Better error handling
- Documentation improvements
- Testing and examples

## 📝 License

MIT License - Free to use and modify

## 🎓 Learning Resources

This project demonstrates:
- **Agent Pattern:** Input → Intent Detection → Action → Response
- **API Integration:** Best practices for external services
- **Error Handling:** Graceful degradation
- **NLP Basics:** Keyword matching, entity extraction
- **CLI Design:** User-friendly command-line interfaces

Perfect for beginners learning about AI agents before diving into complex LLM frameworks!
