# Changelog

All notable changes to Weather News Agent will be documented in this file.

## [Unreleased]

### Added
- **Comprehensive Test Suite** - Achieved 87% code coverage
  - 45 unit tests covering all major functionality
  - Test coverage: main.py (87%)
  - Test suites for:
    - Agent initialization and API key handling
    - Intent detection (weather, news, time, math, greetings, help)
    - Location and topic extraction
    - Weather API integration (mocked)
    - News API integration (mocked)
    - Time functionality
    - Math calculator with security validation
    - Action execution and response generation
- **Testing Infrastructure** - pytest with coverage reporting
  - Mock testing for external API dependencies
  - Comprehensive edge case testing
  - Security testing (malicious code rejection)
- **Quality Assurance** - All tests passing with robust error handling

### Changed
- Enhanced code reliability through extensive testing
- Improved security validation in math expressions

## [1.0.0] - 2025-11-04

### Initial Release
- Simple AI agent with multiple capabilities
- Weather data fetching (OpenWeatherMap API)
- News headlines fetching (News API)
- Current time display
- Basic math calculator
- Intent-based natural language processing
- Interactive command-line interface
