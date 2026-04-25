from fastapi import FastAPI
from app.models.model import Post
from app.db.base import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)




app = FastAPI()

@app.get("/")
async def root():
    return{"message": "This is Your root path"}

