# RecallSearch Agent

A lightweight web-search chat agent created for the
Broadcastwell software engineering challenge.

## Features
- One external agent tool: Tavily web search
- Search-backed answers and clickable sources
- Timestamped conversation memory
- Previous-question recall in IST
- 30-minute search cache
- Streamlit chat interface
- No payment card or API key needed for light usage

## Run locally

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

## Optional free search API key

Tavily's keyless tier is rate-limited.
For higher free limits, create a free Tavily account:
https://app.tavily.com/

Add TAVILY_API_KEY=your_key to .env

No credit card is required for the free Researcher plan.

## Tests

python3 -m unittest discover -s tests -v

## Design

See design.md for architecture and trade-offs.

## Demo

Ask a web question, then ask:
"What was my previous question, and when did I ask it?"

Questions remain in SQLite across restarts.

## Security

Never commit your .env file or API keys.
# recallsearch-agent
