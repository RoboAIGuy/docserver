"""
Imports for the app
"""
from typing import List
from typing import Optional

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import SecretStr

from sqlalchemy.orm import Session

from app import config

from app.db import database


from fastapi.middleware.cors import CORSMiddleware


from app.api.API_v1.Api import api_router


# App declaration
app = FastAPI(  
                title = "This is a demo document server made for an assignment for Chronicle.",
                description = config.app_description,
                version = "1.0.0",
                openapi_url="/api/v1/openapi.json",
                swagger_ui_parameters={"defaultModelsExpandDepth": -1}
            )


# Create tables
database.CreateTables()


# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



"""
START OF FASTAPI API DEFINITIONS
The standard FastAPI path operations code.
"""

@app.get("/health", status_code=200)
def dummy_health_for_deployment():
    return {"message": "OK"}

# Include all routes from API v1
app.include_router(api_router, prefix = config.API_V1_STR)