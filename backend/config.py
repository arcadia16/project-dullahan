import os

# Mode: "agent" or "application"
APP_MODE = os.getenv("APP_MODE", "mainframe")

# Agent API (used by orchestrator to call agent)
# TODO: test for non-localhost interactions
AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "http://localhost:8001")
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "change-me-in-production")

# Orchestrator API key (reserved)
ORCHESTRATOR_API_KEY = os.getenv("ORCHESTRATOR_API_KEY", "change-me-too")

# Agent local paths
HASHCAT_BIN = os.getenv("HASHCAT_BIN", "hashcat")
# TODO: fetch available wordlists list from agent and make a selector on the frontend side
WORDLIST_PATH = os.getenv("WORDLIST_PATH", "/usr/share/wordlists/rockyou.txt")
JOBS_BASE_DIR = os.getenv("JOBS_BASE_DIR", "/tmp/hashcat_jobs")
