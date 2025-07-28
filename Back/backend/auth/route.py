from fastapi import APIRouter,status,Depends
from fastapi.security import OAuth2PasswordBearer
from src.database import get_db
from sqlalchemy.orm import Session
from auth.utils import get_token

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/token",status_code=status.HTTP_200_OK)
async def athenticate_user(data:OAuth2PasswordBearer=Depends(),db:Session=Depends(get_db)):
    return get_token(data,db)
