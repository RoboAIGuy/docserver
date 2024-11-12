import os

from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from fastapi import Depends
from fastapi import Body
from fastapi import HTTPException
from fastapi import APIRouter

from app.models.Users import User

from app.db.database import get_db

from app.schemas import schemas

from fastapi.logger import logger

#  Initialize router
router = APIRouter()



################################################ START OF USER APIs ######################################################

# API for creating a User
@router.post("/create", response_model=schemas.UserRead, status_code=201)
def create_user(UserCreate: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    db_return = User.get_user_by_email(db, UserCreate.email)
    if db_return:
        raise HTTPException(status_code=400, detail="User with same email address already exists")
    return User.create_user(db=db, user=UserCreate)


# API for getting all Users (limit 100)
@router.get("/get-all-users", response_model=List[schemas.UserRead])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_return = User.get_users(db, skip=skip, limit=limit)
    return db_return


# API for getting a User by email
@router.get("/get-user-by-email/{Email}")
def read_user_by_email(Email: str, db: Session = Depends(get_db)):
    db_return = User.get_user_by_email(db, email=Email)
    logger.debug(f"User with first name received - {Email}")
    if db_return is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_return


# API to delete an User by email
@router.delete("/delete/{Email}")
def delete_user(Email: str, db:Session = Depends(get_db)):
    db_return = User.get_user_by_email(db, Email)
    if db_return is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    else:
        db_return = User.delete_user_by_email(db, email=Email)
        if db_return is not None:
            return {"msg" : "User deletion successful"}

     
################################################# END OF USER APIs #######################################################