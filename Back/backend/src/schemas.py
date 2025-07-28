from pydantic import BaseModel,Field,EmailStr,ConfigDict
from typing import List,Optional

class UserBase(BaseModel):
    nom:str
    prenom:str
    email:EmailStr

class CreateUser(UserBase):
    password:str

class ReadUser(UserBase):
    user_id:int
    sessions:List["ReadSession"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

class CreateStatut(BaseModel):
    libelle:str

class MessageBase(BaseModel):
       role:str
       content:str
       model_config = ConfigDict(from_attributes = True)

class CreateMessage(MessageBase):
    session_id:int

class ReadMessage(MessageBase):
    id:int
    model_config=ConfigDict(from_attributes=True)

class CreateSession(BaseModel):
    statut_id:int

class ReadSession(CreateSession):
   user_id:int
   messages:Optional[List["MessageBase"]]=Field(default_factory=list)
   session_id:int
   model_config=ConfigDict(from_attributes=True)

class CreateClassification(BaseModel):
    session_id:int
    categorie:str
    emergency_level:str

class ReadClassification(CreateClassification):
    id:int
    #session:Optional[ReadSession] = None
    model_config=ConfigDict(from_attributes=True)

class CreateUserRequest(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_size:str