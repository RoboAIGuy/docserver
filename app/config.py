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
ReelBlend - This system does end-to-end analysis of videos provided by users tracking. 🚀 Developed using [FastAPI](https://fastapi.tiangolo.com/) by Devs@ReelBlend.

# This API module consists of the following parts:
    1. Video Segmentation Analysis.
    2. Video Lighting Analysis.
    3. Upload and Download of Analyzed filed.
    4. Video Analysis Status query.
    4. Other utility APIs.
"""

###################################### END OF APP DESCRIPTION FOR OPEN API ######################################


########################################## API TAG METADATA DECLARATION #########################################

"""
    Metadata for tags
"""
tags_metadata = [
    {
        "name": "Video",
        "description": "APIs to handle Video Analysis - Segmentation, Lighting, Plane Detections, etc.",
        # "externalDocs": {
        #     "description": "Segmentation docs",
        #     "url": "",
        # },
    },
]

##################################### END OF API TAG METADATA DECLARATION #######################################


############################################## CORS ORIGIN SETTINGS #############################################
"""
    Declaration of CORS origins
"""
origins = [ "https://localhost"
]

########################################## END OF CORS ORIGIN SETTINGS ##########################################





############################################### FILE PATH SETTINGS ##############################################
"""
File Upload settings dictionary
"""

############################################ END OF FILE PATH SETTINGS ##########################################


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

    LOGGER_NAME: str = "ReelBlendCVAdmin"
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
        "ReelBlendCVAdmin": {"handlers": ["default"], "level": LOG_LEVEL},
    }
    
########################################### END OF LOGGER SETTINGS ##############################################