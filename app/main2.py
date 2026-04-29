from sqlalchemy.util import deprecated
from fastapi import HTTPException, status
from sqlalchemy.orm import query
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from passlib.context import CryptContext
from app.db.base import Base, SessionLocal, engine
import app.models.model as model
from app.schemas.schemas import (
    createPost,
    Post,
    CreateUser,
    User
    )
password_hash = PasswordHash.recommended
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
model.Base.metadata.create_all(bind=engine)  #Take all classes that inherit from Base, collect their table definitions (metadata), and create those tables in the database using the given engine.

def get_db():
    db = SessionLocal()
    try:
        yield db    #Give db to the route (endpoint function) pause this function
    finally:
        db.close()   #after req is done  resume func close this session 

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "This is root path"}


@app.get("/posts")
async def posts(db: Session = Depends(get_db)):
    getPosts = db.query(model.Post).all()
    return getPosts

@app.post("/post", response_model=Post)
async def post(post: createPost ,db: Session = Depends(get_db) ):
    newPost = model.Post(title = post.title, description = post.description)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@app.get("/post/{id}", response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    getPost  = db.query(model.Post).filter(model.Post.id == id).first()
    if not getPost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='This post is not available')
    return getPost

@app.put("/post/{id}", response_model=Post)
async def put_post(post: createPost,id: int,db: Session = Depends(get_db)):
    updtPost = db.query(model.Post).filter(model.Post.id == id)
    if not updtPost.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post is not there")
    newpost = updtPost.update({"title": post.title, "description": post.description})
    db.commit()
    return updtPost.first()

@app.delete("/post/{id}")
async def dlt_post(id: int,db: Session = Depends(get_db)):
    dltPost = db.query(model.Post).filter(model.Post.id == id)
    if not dltPost.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post is not there")
    dltPost.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post is Deleted Now"}


@app.post("/user", response_model= User, status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):

#has the pass - user.password
    pwd_context.hash(user.password)

    # createUser = model.User(email = user.email, password = user.password, name =  user.name)
    createUser = model.User(**user.dict())
    db.add(createUser)

    db.commit()
    db.refresh(createUser)
    return createUser