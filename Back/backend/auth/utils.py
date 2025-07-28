from sqlalchemy.orm import Session

from src.schemas import CreateUser
from src.models import UsersModel

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException

from src.models import UsersModel

from datetime import timedelta
import configs

from services.security import verify_password

async def get_token(data:OAuth2PasswordBearer,db:Session):
    user = db.query(UsersModel).filter(UsersModel.email == data.username).first()

    if not user:
        raise HTTPException(status_code=404, 
                             detail="User with this email is not exist",
                             headers={"WWW-Authenticate":"Bearer"})
    
    if verify_password(data.username,user.email):
        raise HTTPException(status_code=404,
                            detail="Credentials is not valid",
                            headers={"WWW-Authenticate":"Bearer"})
    
def get_user_token(user:UsersModel,refresh_token=None):
    payload = {"id":user.user_id}
    token_expired_times=timedelta(minutes = configs.JWT_TOKEN_EXPIRE_MINUTES)
    access_token = ""
    refresh_token = ""

    
    

    
    