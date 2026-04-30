
from sqlalchemy.util import deprecated
from fastapi import HTTPException, status
from sqlalchemy.orm import query
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
# from pwdlib import PasswordHash
# from app.utils import pass_hash
# from passlib.context import CryptContext
from app.db.base import Base, SessionLocal, engine
import app.models.model as model
# from app.schemas.schemas import (
#     createPost,
#     Post,
#     CreateUser,
#     User
#     )
from app.routes import (
    post,
    user,
    auth
)

# pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")
model.Base.metadata.create_all(bind=engine)  #Take all classes that inherit from Base, collect their table definitions (metadata), and create those tables in the database using the given engine.



app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return{"message": "This is root path"}





