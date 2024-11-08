from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.database import get_db

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import schemas
from fastapi.logger import logger


"""
CLASS MAPS TO THE ASSOCIATED TABLE 'users' IN THE DATABASE 'docserver'
"""
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())


#################################### START OF USERS CRUD ##########################################

    """
    GET A USER BY EMAIL
    """
    def get_user_by_email(db:Session, email: str):
        try:
            return db.query(User).filter(User.email == email).first()

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback() 
            logger.error(error)
            return error


    """
    GET ALL USERS UPTO 100 (limit can be changed)
    """
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        try:
            return db.query(User).offset(skip).limit(limit).all()

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error


    """
    CREATE A NEW USER
    """
    def create_user(db: Session, user: schemas.UserCreate):
        try:
            db_user = User(email=user.email, password=user.password, name=user.name)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.debug("User created successfully")
            return db_user

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error


    """
    DELETE AN EXISTING USER
    """
    def delete_user_by_email(db: Session, email: str):
        try:
            db_user = db.query(User).filter(User.email == email).delete(synchronize_session="fetch")
            db.commit()
            db.refresh(db_user)
            logger.debug(f"User with email - {email} has been deleted")
            return {"msg" : "User deletion successful"}

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error