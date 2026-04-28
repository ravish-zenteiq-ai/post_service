from pickle import FALSE
from fastapi import HTTPException

from fastapi import Depends
from fastapi import FastAPI, status, HTTPException
from sqlalchemy.orm import Session
import app.models.model as model
from app.db.base import Base, engine, SessionLocal
from app.schemas.schemas import (
    Post,
    createPost
)


model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()



@app.get("/")
async def root():
    return{"message": "This is Your root path"}

@app.get("/posts")
async def root():
    return{"message": "This is Your root path"}

@app.get("/posts")
async def posts(db: Session = Depends(get_db)):
    return{"message": db.query(model.Post).all()}


@app.post("/post", response_model=Post)
async def create_post(post: createPost,db: Session =  Depends(get_db)):
    newPost = model.Post(title = post.title, description= post.description)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    # return{"message": newPost}
    return newPost
@app.get("/post/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    one_post = db.query(model.Post).filter(model.Post.id == id).first()   #.all() is also there but the thing is only one post will be there of 1 id it will onl;y take tyime in db to search another post of that id i.e time wate onl;y
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post is not available")
    # return{"message": one_post}
    return{"message": one_post}

@app.put("/post/{id}")
async def update_post(id: int, db: Session = Depends(get_db), post = createPost):
    find = db.query(model.Post).filter(model.Post.id == id)
    find.update({"title": post.title, "description": post.description}, synchronize_session=False),
    db.commit()
    return{"message", "POst updated"}

@app.delete("/post/{id}")
async def dlt_post(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(model.Post).filter(model.Post.id == id)
    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="POst not found")
    delete_post.delete(synchronize_session=False)
    db.commit()
    # return{"message": f"Post {delete_post} is deleted"}
    return  delete_post