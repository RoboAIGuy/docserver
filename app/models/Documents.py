from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import and_

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.database import get_db

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import schemas
from app.models.Permissions import Permission

from fastapi.logger import logger


"""
CLASS MAPS TO THE ASSOCIATED TABLE 'documents' IN THE DATABASE 'docserver'
"""
class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    content = Column(Text)
    creator = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    public = Column(Boolean, default=False)



#################################### START OF VIDEOS CRUD ##########################################

    """
    GET A DOCUMENT BY TITLE
    """
    def get_document_by_title(db:Session, title: str):
        try:
            return db.query(Document).filter(Document.title == title).first()

        except SQLAlchemyError as e:
            error = str(e)
            db.rollback() 
            logger.error(error)
            return error
        
        
    """
    GET ALL DOCUMENT BY USER EMAIL
    """
    def get_documents_by_email(db:Session, email: str):
        try:
            return db.query(Document).filter(Document.creator == email).all()

        except SQLAlchemyError as e:
            error = str(e)
            db.rollback() 
            logger.error(error)
            return error
        
    
    """
    GET ALL DOCUMENTS BY USER EMAIL AND DOCUMENT TITLE
    """
    def get_document_by_user_and_title(db:Session, email: str, title: str):
        try:
            return db.query(Document).filter(and_(Document.creator == email, Document.title == title))

        except SQLAlchemyError as e:
            error = str(e)
            db.rollback() 
            logger.error(error)
            return error
    


    """
    GET ALL DOCUMENTS UPTO 100 (limit can be changed)
    """
    def get_documents(db: Session, skip: int = 0, limit: int = 100):
        try:
            return db.query(Document).offset(skip).limit(limit).all()

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error


    """
    CREATE A NEW DOCUMENT
    """
    def create_document(db: Session, document: schemas.DocumentCreate):
        try:
            db_document = Document(title=document.title, content=document.content, creator=document.creator, public=document.public)
            db.add(db_document)
            db.commit()
            db.refresh(db_document)
            
        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error
        
        try:
            # Give full permissions to the creator
            db_permission = Permission(document_title=document.title, creator_email=document.creator, can_read=True, can_write=True, can_delete=True, granted_by=document.creator)
            db.add(db_permission)
            db.commit()
            db.refresh(db_permission)
            return db_document

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error
        
    
    """
    UPDATE AN EXISTING DOCUMENT
    """
    def update_document(db: Session, DocumentUpdate: schemas.DocumentUpdate):
        try:
            db_document = db.query(Document).filter(Document.title == DocumentUpdate.title).first()
            db_document.content = DocumentUpdate.content
            if DocumentUpdate.public is not None:
                db_document.public = DocumentUpdate.public
            db_document.updated_at = func.now()
            db.commit()
            db.refresh(db_document)
            return db_document

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error    
        


    """
    DELETE AN EXISTING DOCUMENT
    """
    def delete_document_by_title(db: Session, title: str):
        try:
            db_code = db.query(Document).filter(Document.title == title).delete(synchronize_session="fetch")
            db.commit()
            db.refresh(db_code)
            logger.debug(f"Document with title - {title} has been deleted")
            return(db_code)

        except SQLAlchemyError as e:
            error = str(e) # or error = str(e.orig) works as well
            db.rollback()
            logger.error(error)
            return error