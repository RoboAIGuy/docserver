"""
PYTHON FILE TO DECLARE ALL DATABASE INITIALIZERS
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import settings

SQLALCHEMY_DATABASE_URL = settings.db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


"""
 Create all tables
"""
def CreateTables():
    Base.metadata.create_all(bind=engine)
    

"""
 Create an independent database session/connection per request, 
 use the same session through all the request and then close it after the request is finished.
"""
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()