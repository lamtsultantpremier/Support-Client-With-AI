from fastapi import FastAPI,APIRouter,Depends,HTTPException,status,Body
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from src.schemas import CreateUser,ReadUser,CreateUserRequest
from sqlalchemy.orm import Session
from src.models import UsersModel
from src.database import get_db


from services import security,user_services
from datetime import timedelta
router = APIRouter()

@router.post("/register")
def create_user(user:CreateUser,db:Session=Depends(get_db)):
    user_services.create_user_account(user,db)
    payload={"message":"user is created successfully"}
    return JSONResponse(content=payload)

@router.post("/login",status_code=status.HTTP_200_OK)
def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db:Session=Depends(get_db)):
    user = user_services.authenticate_user(form_data.username,form_data.password,db)
    token = security.create_access_token(user.email,user.user_id,timedelta(minutes=20))
   
    return {"access_token": token,"token_type": "bearer"}

@router.get("/me",response_model = ReadUser)
def connected_user(current_user:Annotated[UsersModel,Depends(user_services.get_current_user)]):
    return current_user

