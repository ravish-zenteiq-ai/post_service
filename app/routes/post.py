import app.models.model as model
from app.schemas.schemas import (
    createPost,
    Post,
    CreateUser,
    User
    )

from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
# from app.main2 import get_db
from app.db.session import get_db

router = APIRouter(
    prefix="/post", #/post+/id -> simple way to remove repittion and make things better
    tags=["Posts"]

)



@router.get("/")
async def posts(db: Session = Depends(get_db)):
    getPosts = db.query(model.Post).all()
    return getPosts

@router.post("/", response_model=Post)
async def post(post: createPost ,db: Session = Depends(get_db) ):
    newPost = model.Post(title = post.title, description = post.description)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@router.get("/{id}", response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    getPost  = db.query(model.Post).filter(model.Post.id == id).first()
    if not getPost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='This post is not available')
    return getPost

@router.put("/{id}", response_model=Post)
async def put_post(post: createPost,id: int,db: Session = Depends(get_db)):
    updtPost = db.query(model.Post).filter(model.Post.id == id)
    if not updtPost.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post is not there")
    newpost = updtPost.update({"title": post.title, "description": post.description})
    db.commit()
    return updtPost.first()

@router.delete("/{id}")
async def dlt_post(id: int,db: Session = Depends(get_db)):
    dltPost = db.query(model.Post).filter(model.Post.id == id)
    if not dltPost.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post is not there")
    dltPost.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post is Deleted Now"}