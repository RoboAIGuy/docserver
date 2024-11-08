import os

from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from fastapi import Depends
from fastapi import Body
from fastapi import HTTPException
from fastapi import APIRouter

from app.models.Permissions import Permission
from app.models.Documents import Document
from app.models.Users import User

from app.db.database import get_db

from app.schemas import schemas

from fastapi.logger import logger

#  Initialize router
router = APIRouter()



################################################ START OF PERMISSIONS APIs ######################################################

# API for updating a Permission
@router.put("/create-update-permission/{granted_by_email}")
def create_update_permission(granted_by_email: str, PermissionUpdate: schemas.PermissionUpdate = Body(...), db: Session = Depends(get_db)):
    db_return = Document.get_document_by_title(db, title=PermissionUpdate.document_title)
    if db_return is None:
        raise HTTPException(status_code=404, detail=f"The document with title - '{PermissionUpdate.document_title}' doesn't exist")
    
    db_return = Permission.get_document_permissions(db, email=granted_by_email, title=PermissionUpdate.document_title)
    if db_return is None or db_return.can_write is False:
        raise HTTPException(status_code=401, detail=f"User - '{granted_by_email.strip()}' does not have write permission for document - '{PermissionUpdate.document_title}'")

    db_return = User.get_user_by_email(db, email=PermissionUpdate.user_email)
    if db_return is None:
        raise HTTPException(status_code=404, detail=f"The user with email - '{PermissionUpdate.user_email}' doesn't exist")
    
    db_return = Permission.get_document_permissions(db, email=PermissionUpdate.user_email, title=PermissionUpdate.document_title)
    if db_return is None:
        db_return = Permission.grant_permission(db, permission=PermissionUpdate, granted_by=granted_by_email)
        if db_return is not None:
            return {"msg" : f"No previous permissions found.\nNew Permission for user - '{PermissionUpdate.user_email}' on document - '{PermissionUpdate.document_title}' has been created and granted by - '{granted_by_email}'"}
    else:
        document_details = Document.get_document_by_title(db=db, title=PermissionUpdate.document_title)
        db_return, edit_level = Permission.update_permission(db, permission=PermissionUpdate, granted_by=granted_by_email, creator=document_details.creator)
        if edit_level == 1:
            return {"msg" : f"All provided Permissions for user - '{PermissionUpdate.user_email}' on document - '{PermissionUpdate.document_title}' has been updated"}
        elif edit_level == 2:
            return {"msg" : f"Only 'Read' Permission for user - '{PermissionUpdate.user_email}' on document - '{PermissionUpdate.document_title}' has been updated and granted by - '{granted_by_email}'"}

     
################################################# END OF PERMISSIONS APIs #######################################################