from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import and_

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.database import get_db

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import schemas

from fastapi.logger import logger
from sqlalchemy import String


"""
CLASS MAPS TO THE ASSOCIATED TABLE 'permissions' IN THE DATABASE 'docserver'
"""
class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, index=True)
    document_title = Column(String)
    creator_email = Column(String)
    can_read = Column(Boolean, default=False)
    can_write = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    granted_by = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())




#################################### START OF VIDEOS CRUD ##########################################


    """
    GET THE PERMISSIONS FOR A USER OF A DOCUMENT
    """
    def get_document_permissions(db: Session, email: str, title: str):
        return db.query(Permission).filter(and_(Permission.document_title == title, Permission.creator_email == email)).first()
    
    
    
    """
    CREATE A NEW PERMISSION FOR A USER ON A DOCUMENT
    """
    def grant_permission(db: Session, permission: schemas.PermissionCreate, granted_by: str):
        db_permission = Permission(
            document_title=permission.document_title,
            creator_email=permission.user_email,
            can_read=permission.can_read,
            can_write=permission.can_write,
            can_delete=permission.can_delete,
            granted_by=granted_by
        )
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission
    
    
    
    """
    UPDATE A PERMISSION FOR A USER ON A DOCUMENT
    """
    def update_permission(db: Session, permission: schemas.PermissionUpdate, granted_by: str, creator: str):
        edit_level = 0
        try:
            permission_details = Permission.get_document_permissions(db=db, email=permission.user_email, title=permission.document_title)
            print(creator, granted_by.strip())
            if permission_details is not None and creator == granted_by.strip():
                if permission.can_read is not None:
                    permission_details.can_read = permission.can_read
                if permission.can_write is not None:
                    permission_details.can_write = permission.can_write
                if permission.can_delete is not None:
                    permission_details.can_delete = permission.can_delete
                edit_level = 1
                    
            if permission_details is not None and creator != granted_by.strip():
                if permission.can_read is not None:
                    permission_details.can_read = permission.can_read
                edit_level = 2
                
                permission_details.granted_by = granted_by
                db.commit()
                db.refresh(permission_details)
            return permission_details, edit_level
        
        except SQLAlchemyError as e:
            error = str(e)
            db.rollback()
            logger.error(error)
            return error
    


    """
    DELETE AN EXISTING PERMISSION
    """
    def delete_entry_by_id(db: Session, id: str):
        try:
            db_code = db.query(Permission).filter(Permission.id == id).delete(synchronize_session="fetch")
            db.commit()
            db.refresh(db_code)
            logger.debug(f"Permission with ID - {id} has been deleted")
            return(db_code)

        except SQLAlchemyError as e:
            error = str(e)
            db.rollback()
            logger.error(error)
            return error
        
        
        
    """
    DELETE ALL EXISTING PERMISSIONS FOR A DOCUMENT (USE WHEM DOC IS DELETED)
    """        
    def delete_entry_by_user_and_title(db: Session, title: str, creator: str):
        try:
            # delete all entries in permission table filtering based on title and creator
             
            db_code = db.query(Permission).filter(Permission.document_title == title).delete(synchronize_session="fetch")
            db.commit()
            db.refresh(db_code)
            logger.debug(f"Permission with ID - {id} has been deleted")
            return(db_code)

        except SQLAlchemyError as e:
            error = str(e)
            db.rollback()
            logger.error(error)
            return error