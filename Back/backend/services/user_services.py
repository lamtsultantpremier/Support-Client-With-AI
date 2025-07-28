from fastapi import HTTPException,status,Depends

from src.schemas import CreateUser

from sqlalchemy.orm import Session

from services import security

from src.models import UsersModel

from src.database import get_db
import jwt

def create_user_account(UserInfo:CreateUser,db:Session):
    existing_user = db.query(UsersModel).filter(UsersModel.email == UserInfo.email).first()

    if existing_user:
      raise HTTPException(
          status_code = status.HTTP_409_CONFLICT,
          detail = "User with this username already exist" 
      )
    new_user = UsersModel(nom = UserInfo.nom,
                    prenom = UserInfo.prenom,
                    email = UserInfo.email,
                    password = security.crypt_password(UserInfo.password))
    db.add(new_user)
    db.commit()

def authenticate_user(username: str,password: str,db: Session):
        user = db.query(UsersModel).filter(UsersModel.email == username).first()

        if not user or not security.verify_password(password , user.password):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Username name or password not found",
            headers={"WWW-Authenticate": "Bearer"})
    
        return user

def get_current_user(token:str=Depends(security.oauth2_scheme),db:Session=Depends(get_db)):
    try:

      user_id = security.get_token_info(token = token)
      if user_id is None:
          raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Token non valid"
          )
      user = get_user_by_id(user_id,db)
      if  user is None:
          raise HTTPException(
              status_code = status.HTTP_401_UNAUTHORIZED,
              detail = "utilisateur non trouvé"
          )
      
      return user
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    

def get_user_by_id(user_id: int,db:Session):
    user = db.query(UsersModel).filter(UsersModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="User not Found")
    return user