from fastapi import APIRouter, Request, Response, status
from sse_starlette.sse import EventSourceResponse

import json
import asyncio

from ..utilities import dashboard_utils

router = APIRouter(
    tags=["event-dashboard"]
)

received_calls = []

@router.post("/incoming-call")
async def call_log_receiver(request: Request, response: Response):
    """
        Endpoint to receive data from web-hook.
    """
    data = await request.json()
    if dashboard_utils.detected_test_call(data) == False:
        received_calls.append(data)

    response.status_code = status.HTTP_200_OK
    return {
        "message": "Received"
    }


@router.get("/dashboard")
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
                    "data": json.dumps(*list(dashboard_utils.get_calls(received_calls))) if len(received_calls) > 0 else None
                }
                await asyncio.sleep(1)
    return EventSourceResponse(event_generator())