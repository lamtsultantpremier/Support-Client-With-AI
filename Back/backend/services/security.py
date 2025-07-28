from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
import jwt
import configs
pwd_context = CryptContext(schemes=["sha256_crypt","md5_crypt","des_crypt"],deprecated="auto")

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

def crypt_password(password:str):
    return pwd_context.hash(password,scheme="sha256_crypt")


def verify_password(plain_password,hash_password):
    return pwd_context.verify(plain_password,hash_password)

def get_token_info(token: str):
    payload: dict= jwt.decode(jwt = token,key = configs.JWT_SECRET,algorithms = [configs.JWT_ALGORITHM])
    user_id = payload.get("id")
    user_name = payload.get("sub")
    return user_id

def create_access_token(username: str,user_id:str,expire_time:timedelta):
    encode = {"sub": username,"id": user_id}
    expires = datetime.utcnow() + expire_time
    encode.update({"exp": expires})
    return jwt.encode(encode,key = configs.JWT_SECRET,algorithm = configs.JWT_ALGORITHM)