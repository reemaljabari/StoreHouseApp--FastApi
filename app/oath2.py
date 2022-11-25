import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database import get_db




JWT_KEY="f36b64bc74e9c7ae562e0a983bb9fcca"
JWT_ALGRITHM="HS256"


oath2_scehma =OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    encoded_jwt=jwt.encode(payload=data, key= JWT_KEY, algorithm=JWT_ALGRITHM)
    return encoded_jwt


def decode_JWT(token:str):
    payload=jwt.decode(jwt=token, key=JWT_KEY, algorithms=JWT_ALGRITHM)
    id=payload.get("user_id")
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ld not validate"
        )
    return payload
    
def get_current_user(authorization: str = Security(APIKeyHeader(name='Authorization')), db:Session=Depends(get_db)):
    token=decode_JWT(token=authorization)
    return token

