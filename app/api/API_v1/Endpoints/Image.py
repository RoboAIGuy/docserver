import os

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

from app.models.Videos import Codes
from app.models.Transactions import Transactions

from app.db.database import get_db

from app.schemas import schemas

from fastapi.logger import logger

#  Initialize router
router = APIRouter()



################################################ START OF CODE APIs ######################################################

# API for creating a code
@router.post("/create", response_model=schemas.CodesRead, status_code=201)
def create_code(CodeCreate: schemas.CodesCreate = Body(...), db: Session = Depends(get_db)):
    db_return = Codes.get_code_image_by_code(db, CodeCreate.code)
    if db_return:
        raise HTTPException(status_code=400, detail="Code with same value is already present")
    return Codes.create_code(db=db, code=CodeCreate)


# API for getting all codes (limit 100)
@router.get("/get-all", response_model=List[schemas.CodesRead])
def read_all_codes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_return = Codes.get_codes(db, skip=skip, limit=limit)
    return db_return


# API for getting a code image by code
@router.get("/get-image-by-code/{Code}")
def read_code_image_by_code(Code: str, db: Session = Depends(get_db)):
    db_return = Codes.get_code_image_by_code(db, code=Code)
    logger.debug(f"User with first name received - {Code}")
    if db_return is None:
        raise HTTPException(status_code=404, detail="Code image not found")
    return db_return


# API for getting a code by code id
@router.get("/get-by-id/{Id}", response_model=schemas.CodesRead)
def read_code_by_id(Id: str, db: Session = Depends(get_db)):
    db_return = Codes.get_code_by_id(db, id=Id)
    logger.debug(f"Code with ID received - {Id}")
    if db_return is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return db_return


# API to delete a code by code value
@router.delete("/delete-by-code/{Codevalue}")
def delete_code_by_value(Codevalue: str, Lastname: str, db:Session = Depends(get_db)):
    db_return = Codes.delete_code_by_code_value(db, code=Codevalue)
    if db_return is None:
        raise HTTPException(status_code=404, detail="Code not found")
    else:
        return {"msg" : "deletion success"}

     
################################################# END OF CODE APIs #######################################################