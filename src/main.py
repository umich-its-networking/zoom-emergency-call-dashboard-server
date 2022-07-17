from fastapi import FastAPI, Depends, Response, status
from fastapi.middleware.cors import CORSMiddleware


from src.routes import dashboard_routes
from src.config import get_settings, Settings


app = FastAPI()
app.include_router(dashboard_routes.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/status-check", 
    tags=['status'],
    summary="Check server settings.",
    description="Provides HTTP GET route to check server settings.",
    response_description="Current environment settings."
)
async def status_check(response: Response, settings: Settings = Depends(get_settings)):
    """
        Server status comes from the config.py file. Settings are extracted 
        from Environment variables set by admin.
    """
    try:
        response.status_code = status.HTTP_200_OK
        return {
            "environment": settings.environment,
            "testing": settings.testing
        }
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "Server Error"
        }


    