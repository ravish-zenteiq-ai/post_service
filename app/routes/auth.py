
from dns import message
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
import app.models.model as model
from app.schemas.schemas import loginUser
from app.utils.pass_hash import verify_hash

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
async def login(detail: loginUser,db: Session = Depends(get_db)):
    valid = db.query(model.User).filter(model.User.email == detail.email).first()
    if not valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    valid2 = verify_hash(detail.password, valid.password)
    if not valid2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    

    return {"message": "Logged In"}