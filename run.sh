#!/bin/bash
# Script to run the weather-news-agent with the proper virtual environment
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/myenv/bin/activate"
python "$DIR/main.py" "$@"
