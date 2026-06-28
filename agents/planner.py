import json
import anthropic

client = anthropic.Anthropic()


def planner_node(state: dict) -> dict:
    """Break the user question into focused search queries."""
    question = state["question"]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=(
            "You are a research planner. Given a question, produce 3-5 focused "
            "web search queries that together will gather enough information to "
            "answer it thoroughly. Return ONLY a JSON array of query strings, "
            "no explanation."
        ),
        messages=[{"role": "user", "content": question}],
    )

    raw = response.content[0].text.strip()
    # strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    queries = json.loads(raw.strip())
    return {"search_queries": queries}
