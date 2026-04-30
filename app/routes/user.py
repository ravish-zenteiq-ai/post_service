import app.models.model as model
from app.schemas.schemas import (
    createPost,
    Post,
    CreateUser,
    User
    )

from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.utils import pass_hash

from app.db.session import get_db

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/", response_model= User, status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):

#has the pass - user.password
    # hashed_pass=pwd_context.hash(user.password)
    # user.password = hashed_pass
#hash using argon2 pwdlib
    pass_hashing= pass_hash.hash_pass(user.password)
    user.password = pass_hashing

    # createUser = model.User(email = user.email, password = user.password, name =  user.name)
    createUser = model.User(**user.dict())
    db.add(createUser)

    db.commit()
    db.refresh(createUser)
    return createUser

@router.get("/{id}", response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):
    getUser  =db.query(model.User).filter(model.User.id == id).first()
    if not getUser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user is not there")
    return getUser