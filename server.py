import asyncio
import json
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from graph import research_graph

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.post("/research")
async def research(req: QuestionRequest):
    async def event_stream():
        loop = asyncio.get_event_loop()

        def run_graph():
            events = []
            for event in research_graph.stream(
                {"question": req.question, "search_results": []},
                stream_mode="updates",
            ):
                events.append(event)
            return events

        events = await loop.run_in_executor(None, run_graph)

        for event in events:
            for node_name, output in event.items():
                if node_name == "planner":
                    data = {
                        "node": "planner",
                        "queries": output["search_queries"],
                    }
                elif node_name == "searcher":
                    data = {
                        "node": "searcher",
                        "count": len(output["search_results"]),
                    }
                elif node_name == "synthesizer":
                    data = {
                        "node": "synthesizer",
                        "report": output["report"],
                    }
                else:
                    continue

                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(0)

        yield "data: {\"node\": \"done\"}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


app.mount("/static", StaticFiles(directory="static"), name="static")
