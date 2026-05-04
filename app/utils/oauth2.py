# from time import timezone
from app.models import model
from fastapi import HTTPException, status
from fastapi import Depends
from jwt import PyJWTError
import jwt
from sqlalchemy.orm import Session
from app.db import session
from datetime import datetime, timedelta, timezone
from app.schemas import schemas
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#ALOGRITHM
#EXPIRY



SECRET_KEY = "09d25e094faa6ca2556c818166b7a099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode= data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        return token_data
    except PyJWTError:
        raise credentials_exception

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(session.get_db)):
    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token =  verify_access_token(token, credentials_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user