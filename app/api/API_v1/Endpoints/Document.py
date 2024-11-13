from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from fastapi import Depends
from fastapi import Query
from fastapi import Body
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File
from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.models.Documents import Document
from app.models.Permissions import Permission
from app.models.Users import User

from app.db.database import get_db

from app.schemas import schemas

from fastapi.logger import logger

#  Initialize router
router = APIRouter()



################################################ START OF VIDEO APIs ######################################################

# API for creating a document
@router.post("/create-document", response_model=schemas.DocumentCreate, status_code=201)
def create_document(DocumentCreate: schemas.DocumentCreate = Body(...), db: Session = Depends(get_db)):
    db_return = User.get_user_by_email(db, email=DocumentCreate.creator)
    if db_return is None:
        raise HTTPException(status_code=404, detail=f"User with email - {DocumentCreate.creator} not found")
    if Document.get_document_by_title(db, title=DocumentCreate.title) is not None:
        raise HTTPException(status_code=400, detail="Document with same title already exists")
    return Document.create_document(db=db, document=DocumentCreate)

# API to read a document by user and title
@router.get("/read-document/{title}/{user}", response_model=schemas.DocumentReadContent)
def read_document_by_user_and_title(title: str, user: str, db: Session = Depends(get_db)):
    document_details = Document.get_document_by_title(db, title=title)
    if document_details is None:
        raise HTTPException(status_code=404, detail=f"Document with title - {title} not found")
    if document_details.public is False:
        db_return = Permission.get_document_permissions(db, email=user, title=title) 
        if db_return is None or db_return.can_read is False:
            raise HTTPException(status_code=403, detail="You do not have permission to read this document")    
    return document_details

# API to update a document by title
@router.put("/update-document")
def update_document_by_title(DocumentUpdate: schemas.DocumentUpdate = Body(...), db: Session = Depends(get_db)):
    # check if document exists for particular user
    db_document = Document.get_document_by_user_and_title(db, email=DocumentUpdate.creator, title=DocumentUpdate.title)
    if db_document is None:
        raise HTTPException(status_code=404, detail=f"Document with title - {DocumentUpdate.title} for user - '{DocumentUpdate.creator}' not found")
    doc_permissions = Permission.get_document_permissions(db, email=DocumentUpdate.creator, title=DocumentUpdate.title)
    print(doc_permissions)
    if doc_permissions is None or not doc_permissions.can_write:
        raise HTTPException(status_code=403, detail="You do not have permission to update this document")
    return Document.update_document(db, DocumentUpdate=DocumentUpdate)


# API for getting all documents (limit 100)
@router.get("/get-all-documents", response_model=List[schemas.DocumentRead])
def get_all_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_return = Document.get_documents(db, skip=skip, limit=limit)
    return db_return


# API for getting and classifying all documents as per user (limit 100)
@router.get("/get-documents-classified-for-user/{user}")
def get_user_documents(user:str, db: Session = Depends(get_db)):
    created_documents = db.query(Document).filter(Document.creator == user).all()
    readable_documents = db.query(Document).join(Permission, Document.title == Permission.document_title).filter(Permission.creator_email == user, Permission.can_read == True).all()
    editable_documents = db.query(Document).join(Permission, Document.title == Permission.document_title).filter(Permission.creator_email == user, Permission.can_write == True).all()
    return {"created_documents": created_documents, "readable_documents": readable_documents, "editable_documents": editable_documents}

            

# API for getting documents by title
@router.get("/get-document-by-title/{title}")
def get_document_by_title(title: str, db: Session = Depends(get_db)):
    db_return = Document.get_document_by_title(db, title=title)
    if db_return is None:
        raise HTTPException(status_code=404, detail=f"Document with title - {title} not found")
    return db_return
  
  
# API for getting documents by user email
@router.get("/get-documents-by-user/{email}")
def get_documents_by_user_email(email: str, db: Session = Depends(get_db)):
    db_return = Document.get_documents_by_email(db, email=email)
    logger.debug(f"User with email - '{email}' received")
    if db_return is None:
        raise HTTPException(status_code=404, detail=f"No documents found for the user with email - {email}")
    return db_return


# API to delete a document
@router.delete("/delete-document")
def delete_document_by_title(document: schemas.DocumentDelete = Body(...), db: Session = Depends(get_db)):
    db_present = Document.get_document_by_user_and_title(db, email=document.creator, title=document.title)
    if db_present is None:
        raise HTTPException(status_code=404, detail=f"Document with title - {document.title} for user - '{document.email}' not found")
    doc_permissions = Permission.get_document_permissions(db, email=document.creator, title=document.title)
    if doc_permissions is None or not doc_permissions.can_delete:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this document")
    if db_present is not None and doc_permissions.can_delete:
      db_return = Document.delete_document_by_title(db, title=document.title)
      if db_return is None:
          raise HTTPException(status_code=404, detail=f"Document with title - '{document.title}' not found")
      Permission.delete_entry_by_user_and_title(db, title=document.title, creator=document.creator)
      return {"msg" : f"Document with title - '{document.title}' has been deleted"}
     
################################################# END OF CODE APIs #######################################################