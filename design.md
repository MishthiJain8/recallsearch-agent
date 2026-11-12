# RecallSearch — Design Document

## Objective
Build a fast, accurate conversational search agent that remembers
previous questions and their timestamps.

## Architecture
Streamlit chat UI
  |
  +-- SQLite conversation memory
  |
  +-- Local previous-question recall
  |
  +-- Tavily web search
        |
        +-- Search-backed answer
        +-- Ranked source URLs
        +-- Local search cache

## One-tool constraint
The only external agent tool is Tavily Search.
There are no additional agent tools.

Tavily's search endpoint can optionally generate a
search-backed answer as part of the same search request.

SQLite provides local persistent memory.

## Conversation Memory
User questions and assistant responses are stored with
ISO-8601 UTC timestamps.

Previous-question requests are answered locally and
timestamps are converted to IST for display.

Recent user messages provide context for short follow-ups.

## Speed
Memory recall requires no network request.
Web results are cached for 30 minutes.
The app makes one search request per uncached question.

## Accuracy
Answers use search-provider results and source URLs.
If no generated answer is available, the app displays
source excerpts instead.

Search results and generated answers may contain errors.
The app does not independently verify full source pages.

## Reliability
Search errors are displayed without crashing the app.
Question memory continues working during search failures.

## Limitations
Keyless Tavily searches have rate limits.
Search-provider summaries may be incomplete.
Follow-up handling is heuristic, not full LLM reasoning.
SQLite is designed for local single-user use.
