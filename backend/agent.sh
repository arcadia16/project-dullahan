#!/bin/bash

export APP_MODE=agent
export AGENT_API_KEY="your-strong-agent-key"
export HASHCAT_BIN=/usr/bin/hashcat
export WORDLIST_PATH=/usr/share/wordlists/rockyou.txt
source venv/bin/activate

uvicorn main:app --reload --port 8001
