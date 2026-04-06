#!/bin/bash

export APP_MODE=application
export AGENT_BASE_URL="http://127.0.0.1:8001"
export AGENT_API_KEY="your-strong-agent-key"

source venv/bin/activate
uvicorn main:app --reload --port 8000
