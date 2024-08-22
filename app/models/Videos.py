from math import prod
from fastapi import Body
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
import pprint
from sqlalchemy.orm import relationship

from app.db.database import Base, engine
from app.db.database import get_db

from datetime import datetime

from calendar import c
from typing import Hashable
from pprint import pprint

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import schemas
import json
from fastapi.logger import logger

#import pandas as pd

"""
CLASS MAPS TO THE ASSOCIATED TABLE 'videos' IN THE DATABASE 'reelblend'
"""
class Videos(Base):
    __tablename__ = "videos"

    video_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, primary_key=True, index=True)
    video_location_s3 = Column(String, nullable=False)
    video_type = Column(String)
    generation_date = Column(Date, nullable=False)



#################################### START OF VIDEOS CRUD ##########################################

    """
    GET A VIDEO DATA BY ID
    """
    def get_video_by_id(db:Session, id: str):
        try:
            return db.query(Videos).filter(Videos.video_id == id).first()

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback() 
            logger.error(error)
            return error


    """
    GET ALL ENTRIES UPTO 100 (limit can be changed)
    """
    def get_videos(db: Session, skip: int = 0, limit: int = 100):
        try:
            return db.query(Videos).offset(skip).limit(limit).all()

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error


    """
    INSERT NEW VIDEO DETAILS
    """
    def create_entry(db: Session, code: schemas.VideosCreate):
        try:
            db_code = Videos(code=code.code, code_image=code.code_image, generation_date=code.generation_date)
            db.add(db_code)
            db.commit()
            db.refresh(db_code)
            logger.debug("Product has been created successfully")
            return db_code

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error


    """
    DELETE AN EXISTING VIDEO BY ID
    """
    def delete_entry_by_id(db: Session, id: str):
        try:
            db_code = db.query(Videos).filter(Videos.video_id == id).delete(synchronize_session="fetch")
            db.commit()
            db.refresh(db_code)
            logger.debug(f"Video with ID - {id} has been deleted")
            return(db_code)

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error