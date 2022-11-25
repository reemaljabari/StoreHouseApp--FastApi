from fastapi import APIRouter,Body, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.database import get_db
from app.models import User
from app.schemas.user import UserSchema,Token, UserLoginSchema
from app.oath2 import create_access_token
from app import utils




authontication=APIRouter(
tags=["authontication"]
)



@authontication.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_user(user:UserSchema= Body(), db:Session=Depends(get_db)):
    hashed_password= utils.hash(user.Password)
    user.Password=hashed_password
    user_db=db.query(User).filter(User.email== user.email).first()
    if not user_db:
        new_user=user.dict()
        db_obj= User(**new_user)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return {
                "Message": {"new User Added to the DataBase"},
                "Data": db_obj
            }
            

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" user already exist , please Login")






@authontication.post("/login", response_model=Token)
def login (user_credentials:UserLoginSchema=Body(), db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credrntials"
        )
    if not utils.verify(user_credentials.Password, user.Password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="INVALID CREDINTIALS"
        )
    token_data={
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name":user.last_name,
        "email": user.email,
        "phone_number": user.phone_number
    }
    acces_token=create_access_token(token_data)
    return {
        "access_token": acces_token,
        "token_type": "bearer"
    }


