Hi, I'm Mishthi. I built RecallSearch, a web-search chat agent
focused on fast answers, accuracy, and conversational memory.

I used Streamlit for the chat interface and Gemini with Google
Search grounding as the agent's only external tool.

Each question and response is stored locally in SQLite with
a UTC timestamp, allowing the agent to remember previous
questions even after restarting.

I kept the architecture simple with one model request per
question, bounded conversation history, and source links
when search results are available.

I also documented the architecture in design.md and added
automated tests for the memory layer.
