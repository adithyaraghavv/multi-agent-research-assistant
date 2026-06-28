#!/usr/bin/env python3
"""CLI entry point for the multi-agent research assistant."""

import sys
from dotenv import load_dotenv

load_dotenv()

from graph import research_graph  # noqa: E402 — load env before importing graph


def run(question: str) -> str:
    print(f"\n[Planner] Breaking down question into search queries...")
    result = research_graph.invoke({"question": question, "search_results": []})

    queries = result.get("search_queries", [])
    print(f"[Planner] Generated {len(queries)} queries:")
    for q in queries:
        print(f"  • {q}")

    results = result.get("search_results", [])
    print(f"\n[Searcher] Retrieved {len(results)} source documents.")
    print("[Synthesizer] Writing report...\n")

    return result["report"]


def main():
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Enter your research question: ").strip()
        if not question:
            print("No question provided.")
            sys.exit(1)

    report = run(question)
    print(report)


if __name__ == "__main__":
    main()
