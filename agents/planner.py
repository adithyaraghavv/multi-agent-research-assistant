import json
import os
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])


def planner_node(state: dict) -> dict:
    """Break the user question into focused search queries."""
    question = state["question"]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=512,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research planner. Given a question, produce 3-5 focused "
                    "web search queries that together will gather enough information to "
                    "answer it thoroughly. Return ONLY a JSON array of query strings, "
                    "no explanation."
                ),
            },
            {"role": "user", "content": question},
        ],
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    queries = json.loads(raw.strip())
    return {"search_queries": queries}
