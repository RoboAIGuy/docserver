"""
Python file to read diferent configurations
"""

from pydantic import Field
from pydantic import BaseSettings
from pydantic import BaseModel



############################################# API VI ENDPOINT SETTINGS ##########################################

API_V1_STR = "/api/v1"

######################################### END OF API VI ENDPOINT SETTINGS #######################################


########################################## APP DESCRIPTION FOR OPEN API #########################################
app_description = """
DocServer - This system does end-to-end management of documents created by users. 🚀 Developed using [FastAPI](https://fastapi.tiangolo.com/) by Kaustuv Sarkar.

# This API suite consists of the following parts:
    1. User management.
    2. Document management.
    3. Permissions Management.
"""

###################################### END OF APP DESCRIPTION FOR OPEN API ######################################


############################################## CORS ORIGIN SETTINGS #############################################
"""
    Declaration of CORS origins
"""
origins = [ "https://localhost"
]

########################################## END OF CORS ORIGIN SETTINGS ##########################################


################################################ DATABASE SETTINGS ##############################################
"""
Read the database connection string from the docker compose file
"""
class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')

settings = Settings()

############################################# END OF DATABASE SETTINGS ##########################################

################################################## LOGGER SETTINGS ##############################################

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "DocServerAdmin"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "DocServerAdmin": {"handlers": ["default"], "level": LOG_LEVEL},
    }
    
########################################### END OF LOGGER SETTINGS ##############################################