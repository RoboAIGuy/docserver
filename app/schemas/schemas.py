"""
PYTHON FILE TO STORE PYDANTIC MODELS OR SCHEMAS REPRESENTING JSON FORMATS WHILE INTERACTING WITH API/DB
"""

from enum import Enum
from typing import List, Union,Set
from typing import Optional
from datetime import date
from psycopg2 import Date
from pydantic import constr
from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import validator
from fastapi import  Query
from typing import Dict



"""
Schemas for video
"""
class VideosCreate(BaseModel):
    user_id : str
    s3_link : str
    date : date

    class Config:
        orm_mode = True

class VideoRead(VideosCreate):
    video_id : str


