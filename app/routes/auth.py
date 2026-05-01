from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
import app.models.model as model
from app.schemas.schemas import loginUser
from app.utils.pass_hash import verify_hash
from app.utils.oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
async def login(detail: OAuth2PasswordRequestForm = Depends(),
db: Session = Depends(get_db)
):
    # valid = db.query(model.User).filter(model.User.email == detail.email).first()
    valid = db.query(model.User).filter(model.User.email == detail.username).first()
    if not valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    valid2 = verify_hash(detail.password, valid.password)
    if not valid2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    access_token=create_access_token(data = {"user_id": valid.id})

    return {"access_token": access_token, "token_type": "bearer"}