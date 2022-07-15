from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

import json
import asyncio

from .config import get_settings, Settings


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

received_calls = []

def get_calls():
    """
        Pulls calls out of the received_calls list.
        Returns a generator object.
    """
    for call in received_calls:
        yield dict(data=call)
    received_calls.clear()   


@app.get("/status-check")
async def check(settings: Settings = Depends(get_settings)):
    """
        Provides a base HTTP route for checking the server status.
    """
    return {
        "environment": settings.environment,
        "testing": settings.testing
    }

@app.post("/incoming-call")
async def call_log_receiver(request: Request):
    """
        Endpoint to receive data from web-hook.
    """
    data = await request.json()
    received_calls.append(data)


@app.get("/dashboard")
async def run(request: Request):
    """
        Endpoint for a client to subscribe to. 
        Emits SSE Events to subscribed client(s).
    """
    def new_call():
        return len(received_calls) > 0

    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            if new_call():
                yield {
                    "retry": 15000,
                    "data": json.dumps(*list(get_calls())) if len(received_calls) > 0 else None
                }
                await asyncio.sleep(1)
    return EventSourceResponse(event_generator())
    