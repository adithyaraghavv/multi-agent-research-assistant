import anthropic

client = anthropic.Anthropic()


def synthesizer_node(state: dict) -> dict:
    """Synthesize search results into a cited markdown report."""
    question = state["question"]
    results = state["search_results"]

    sources_block = ""
    for i, r in enumerate(results, 1):
        sources_block += (
            f"[{i}] {r['title']}\nURL: {r['url']}\n{r['content'][:800]}\n\n"
        )

    system_prompt = (
        "You are an expert research analyst. Using the provided sources, write a "
        "comprehensive, well-structured markdown report that answers the user's "
        "question. Requirements:\n"
        "- Use clear headings and subheadings\n"
        "- Cite sources inline using [N] notation\n"
        "- Include a ## References section at the end listing all cited sources\n"
        "- Be factual and objective; note conflicting information where it exists\n"
        "- Aim for depth and clarity"
    )

    user_content = (
        f"## Question\n{question}\n\n"
        f"## Sources\n{sources_block}\n\n"
        "Write the research report now."
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )

    return {"report": response.content[0].text}
