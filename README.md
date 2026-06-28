# Multi-Agent Research Assistant

A LangGraph-powered research pipeline that takes a question, plans targeted web searches, retrieves live results via Tavily, and synthesizes a cited markdown report using Claude.

## Architecture

```
User Question
     │
     ▼
┌─────────────┐
│   Planner   │  Claude generates 3-5 focused search queries
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Searcher  │  Tavily fetches top results for each query
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Synthesizer  │  Claude writes a cited markdown report
└──────┬───────┘
       │
       ▼
  Markdown Report
```

## Setup

1. **Clone and install dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure API keys**

```bash
cp .env.example .env
# edit .env and add your keys
```

You need:
- `ANTHROPIC_API_KEY` — from [console.anthropic.com](https://console.anthropic.com)
- `TAVILY_API_KEY` — from [tavily.com](https://tavily.com)

## Usage

```bash
# Pass question as argument
python main.py "What are the latest breakthroughs in fusion energy?"

# Or run interactively
python main.py
```

The report is printed to stdout as markdown. Pipe it to a file:

```bash
python main.py "Impact of AI on software engineering jobs" > report.md
```

## Project Structure

```
├── main.py              # CLI entry point
├── graph.py             # LangGraph graph definition
├── agents/
│   ├── state.py         # Shared ResearchState TypedDict
│   ├── planner.py       # Breaks question into search queries
│   ├── searcher.py      # Runs Tavily searches
│   └── synthesizer.py   # Synthesizes results into report
├── requirements.txt
└── .env.example
```
