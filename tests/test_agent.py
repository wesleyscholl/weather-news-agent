"""Comprehensive unit tests for SimpleAIAgent"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import os
from datetime import datetime
from main import SimpleAIAgent


class TestSimpleAIAgentInitialization:
    """Test agent initialization"""
    
    def test_initialization_without_api_keys(self):
        """Test initialization without API keys"""
        old_weather = os.environ.get("OPENWEATHER_API_KEY")
        old_news = os.environ.get("NEWS_API_KEY")
        
        if old_weather:
            del os.environ["OPENWEATHER_API_KEY"]
        if old_news:
            del os.environ["NEWS_API_KEY"]
        
        try:
            agent = SimpleAIAgent()
            assert agent.weather_api_key is None
            assert agent.news_api_key is None
            assert len(agent.capabilities) == 5
        finally:
            if old_weather:
                os.environ["OPENWEATHER_API_KEY"] = old_weather
            if old_news:
                os.environ["NEWS_API_KEY"] = old_news
    
    @patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_weather_key", "NEWS_API_KEY": "test_news_key"})
    def test_initialization_with_api_keys(self):
        """Test initialization with API keys"""
        agent = SimpleAIAgent()
        assert agent.weather_api_key == "test_weather_key"
        assert agent.news_api_key == "test_news_key"
    
    def test_capabilities_list(self):
        """Test that capabilities are properly defined"""
        agent = SimpleAIAgent()
        expected_capabilities = [
            "check weather",
            "get news",
            "tell time",
            "simple math",
            "greet user"
        ]
        assert agent.capabilities == expected_capabilities


class TestProcessInput:
    """Test input processing and intent detection"""
    
    def test_weather_intent(self):
        """Test weather intent detection"""
        agent = SimpleAIAgent()
        
        intent, data = agent.process_input("What's the weather in Paris")
        assert intent == "weather"
        assert data == "Paris"
        
        intent, data = agent.process_input("Tell me the temperature")
        assert intent == "weather"
        
        intent, data = agent.process_input("forecast for tomorrow")
        assert intent == "weather"
    
    def test_news_intent(self):
        """Test news intent detection"""
        agent = SimpleAIAgent()
        
        intent, data = agent.process_input("Get me the latest news")
        assert intent == "news"
        
        intent, data = agent.process_input("headlines about technology")
        assert intent == "news"
    
    def test_time_intent(self):
        """Test time intent detection"""
        agent = SimpleAIAgent()
        
        intent, data = agent.process_input("What time is it?")
        assert intent == "time"
        assert data is None
        
        intent, data = agent.process_input("Tell me the clock")
        assert intent == "time"
        
        intent, data = agent.process_input("what's the time now")
        assert intent == "time"
    
    def test_math_intent(self):
        """Test math intent detection"""
        agent = SimpleAIAgent()
        
        intent, data = agent.process_input("calculate 5 + 3")
        assert intent == "math"
        assert data == "calculate 5 + 3"
        
        intent, data = agent.process_input("2 * 8")
        assert intent == "math"
    
    def test_greeting_intent(self):
        """Test greeting intent detection"""
        agent = SimpleAIAgent()
        
        intent, data = agent.process_input("Hello!")
        assert intent == "greeting"
        assert data is None
        
        intent, data = agent.process_input("Hi there")
        assert intent == "greeting"
        
        intent, data = agent.process_input("Hey")
        assert intent == "greeting"
    
    def test_help_intent(self):
        """Test help intent detection"""
        agent = SimpleAIAgent()
        
        intent, data = agent.process_input("help me")
        assert intent == "help"
        
        intent, data = agent.process_input("what can you do?")
        assert intent == "help"
    
    def test_unknown_intent(self):
        """Test unknown intent handling"""
        agent = SimpleAIAgent()
        
        intent, data = agent.process_input("random gibberish xyz")
        assert intent == "unknown"
        assert data == "random gibberish xyz"
    
    def test_input_normalization(self):
        """Test that input is normalized (lowercased, stripped)"""
        agent = SimpleAIAgent()
        
        intent, data = agent.process_input("  HELLO  ")
        assert intent == "greeting"
        
        intent, data = agent.process_input("WEATHER IN LONDON")
        assert intent == "weather"


class TestExtractLocation:
    """Test location extraction"""
    
    def test_extract_with_in_keyword(self):
        """Test location extraction with 'in' keyword"""
        agent = SimpleAIAgent()
        
        location = agent.extract_location("weather in Paris")
        assert location == "Paris"
        
        location = agent.extract_location("temperature in tokyo")
        assert location == "Tokyo"
    
    def test_extract_with_for_keyword(self):
        """Test location extraction with 'for' keyword"""
        agent = SimpleAIAgent()
        
        location = agent.extract_location("weather for Berlin")
        assert location == "Berlin"
    
    def test_extract_default_location(self):
        """Test default location when none specified"""
        agent = SimpleAIAgent()
        
        location = agent.extract_location("what's the weather like")
        assert location == "London"
    
    def test_extract_multiple_words(self):
        """Test location extraction handles only first word after keyword"""
        agent = SimpleAIAgent()
        
        location = agent.extract_location("weather in New York")
        assert location == "New"  # Current implementation only gets first word


class TestExtractTopic:
    """Test topic extraction for news"""
    
    def test_extract_with_about_keyword(self):
        """Test topic extraction with 'about' keyword"""
        agent = SimpleAIAgent()
        
        topic = agent.extract_topic("news about technology")
        assert topic == "technology"
    
    def test_extract_with_on_keyword(self):
        """Test topic extraction with 'on' keyword"""
        agent = SimpleAIAgent()
        
        topic = agent.extract_topic("headlines on sports")
        assert topic == "sports"
    
    def test_extract_default_topic(self):
        """Test default topic when none specified"""
        agent = SimpleAIAgent()
        
        topic = agent.extract_topic("get me the news")
        assert topic == "general"


class TestGetWeather:
    """Test weather fetching functionality"""
    
    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        """Test successful weather fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 20.5},
            'weather': [{'description': 'sunny'}]
        }
        mock_get.return_value = mock_response
        
        agent = SimpleAIAgent()
        result = agent.get_weather("Paris")
        
        assert "Paris" in result
        assert "20.5°C" in result
        assert "sunny" in result
    
    @patch('requests.get')
    def test_get_weather_api_error(self, mock_get):
        """Test weather fetch with API error"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        agent = SimpleAIAgent()
        result = agent.get_weather("InvalidCity")
        
        assert "couldn't get weather data" in result
    
    @patch('requests.get')
    def test_get_weather_exception(self, mock_get):
        """Test weather fetch with exception"""
        mock_get.side_effect = Exception("Network error")
        
        agent = SimpleAIAgent()
        result = agent.get_weather("Paris")
        
        assert "unavailable" in result


class TestGetNews:
    """Test news fetching functionality"""
    
    @patch('requests.get')
    def test_get_news_general_success(self, mock_get):
        """Test successful general news fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'articles': [
                {'title': 'Breaking News 1'},
                {'title': 'Breaking News 2'},
                {'title': 'Breaking News 3'}
            ]
        }
        mock_get.return_value = mock_response
        
        agent = SimpleAIAgent()
        result = agent.get_news("general")
        
        assert "Latest news" in result
        assert "Breaking News 1" in result
        assert "Breaking News 2" in result
    
    @patch('requests.get')
    def test_get_news_specific_topic_success(self, mock_get):
        """Test successful topic-specific news fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'articles': [
                {'title': 'Tech News 1'},
                {'title': 'Tech News 2'}
            ]
        }
        mock_get.return_value = mock_response
        
        agent = SimpleAIAgent()
        result = agent.get_news("technology")
        
        assert "technology" in result
        assert "Tech News 1" in result
    
    @patch('requests.get')
    def test_get_news_api_error(self, mock_get):
        """Test news fetch with API error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'message': 'Invalid API key'}
        mock_get.return_value = mock_response
        
        agent = SimpleAIAgent()
        result = agent.get_news("sports")
        
        assert "API Error" in result or "couldn't find news" in result
    
    @patch('requests.get')
    def test_get_news_empty_articles(self, mock_get):
        """Test news fetch with no articles"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'articles': []}
        mock_get.return_value = mock_response
        
        agent = SimpleAIAgent()
        result = agent.get_news("obscuretopic")
        
        assert "couldn't find news" in result
    
    @patch('requests.get')
    def test_get_news_exception(self, mock_get):
        """Test news fetch with exception"""
        mock_get.side_effect = Exception("Connection timeout")
        
        agent = SimpleAIAgent()
        result = agent.get_news("general")
        
        assert "error" in result.lower()


class TestGetTime:
    """Test time functionality"""
    
    def test_get_time_format(self):
        """Test that get_time returns proper format"""
        agent = SimpleAIAgent()
        result = agent.get_time()
        
        assert "Current time:" in result
        # Should contain date and time components
        assert "-" in result  # Date separator
        assert ":" in result  # Time separator
    
    @patch('main.datetime')
    def test_get_time_specific_datetime(self, mock_datetime):
        """Test get_time with mocked datetime"""
        mock_now = Mock()
        mock_now.strftime.return_value = "2025-11-04 15:30:45"
        mock_datetime.now.return_value = mock_now
        
        agent = SimpleAIAgent()
        result = agent.get_time()
        
        assert "2025-11-04 15:30:45" in result


class TestDoMath:
    """Test math functionality"""
    
    def test_addition(self):
        """Test basic addition"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("5 + 3")
        assert "Result: 8" in result
    
    def test_subtraction(self):
        """Test subtraction"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("10 - 4")
        assert "Result: 6" in result
    
    def test_multiplication(self):
        """Test multiplication"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("6 * 7")
        assert "Result: 42" in result
    
    def test_division(self):
        """Test division"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("20 / 4")
        assert "Result: 5" in result
    
    def test_complex_expression(self):
        """Test complex math expression"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("(5 + 3) * 2")
        assert "Result: 16" in result
    
    def test_decimal_numbers(self):
        """Test decimal number calculations"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("3.5 + 2.5")
        assert "Result: 6" in result or "Result: 6.0" in result
    
    def test_invalid_expression(self):
        """Test invalid math expression"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("abc + def")
        assert "basic math operations" in result
    
    def test_malicious_code(self):
        """Test that malicious code is rejected"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("__import__('os').system('ls')")
        assert "basic math operations" in result
    
    def test_exception_handling(self):
        """Test exception handling in math"""
        agent = SimpleAIAgent()
        
        result = agent.do_math("1 / 0")
        assert "couldn't calculate" in result


class TestGreetUser:
    """Test greeting functionality"""
    
    def test_greet_user_message(self):
        """Test greeting message content"""
        agent = SimpleAIAgent()
        result = agent.greet_user()
        
        assert "Hello" in result
        assert "AI assistant" in result
        assert "weather" in result
        assert "news" in result


class TestShowHelp:
    """Test help functionality"""
    
    def test_show_help_capabilities(self):
        """Test help shows all capabilities"""
        agent = SimpleAIAgent()
        result = agent.show_help()
        
        for capability in agent.capabilities:
            assert capability in result


class TestExecuteAction:
    """Test action execution"""
    
    @patch.object(SimpleAIAgent, 'get_weather')
    def test_execute_weather_action(self, mock_weather):
        """Test executing weather action"""
        mock_weather.return_value = "Weather result"
        agent = SimpleAIAgent()
        
        result = agent.execute_action("weather", "Paris")
        
        mock_weather.assert_called_once_with("Paris")
        assert result == "Weather result"
    
    @patch.object(SimpleAIAgent, 'get_news')
    def test_execute_news_action(self, mock_news):
        """Test executing news action"""
        mock_news.return_value = "News result"
        agent = SimpleAIAgent()
        
        result = agent.execute_action("news", "technology")
        
        mock_news.assert_called_once_with("technology")
        assert result == "News result"
    
    def test_execute_unknown_action(self):
        """Test executing unknown action"""
        agent = SimpleAIAgent()
        
        result = agent.execute_action("unknown", "data")
        
        assert "not sure how to help" in result


class TestRespond:
    """Test main respond functionality"""
    
    @patch.object(SimpleAIAgent, 'get_time')
    def test_respond_time_query(self, mock_time):
        """Test responding to time query"""
        mock_time.return_value = "Current time: 10:30"
        agent = SimpleAIAgent()
        
        result = agent.respond("What time is it?")
        
        assert result == "Current time: 10:30"
    
    @patch.object(SimpleAIAgent, 'greet_user')
    def test_respond_greeting(self, mock_greet):
        """Test responding to greeting"""
        mock_greet.return_value = "Hello!"
        agent = SimpleAIAgent()
        
        result = agent.respond("Hi there")
        
        assert result == "Hello!"
    
    def test_respond_integration(self):
        """Test full respond integration"""
        agent = SimpleAIAgent()
        
        # Test with greeting (no external API needed)
        result = agent.respond("hello")
        
        assert isinstance(result, str)
        assert len(result) > 0
