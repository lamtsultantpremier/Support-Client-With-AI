from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from src.database import get_db

from typing import Annotated

from src.models import UsersModel,SessionsModel

from src.schemas import ReadUser,CreateSession,CreateStatut,ReadSession,ReadMessage,MessageBase,CreateClassification

from services import session_services,user_services,messages_services,classsification_service

from typing import List

import requests
import configs
router = APIRouter()

@router.post("")
def create_sessions(session:CreateSession,user: Annotated[UsersModel,Depends(user_services.get_current_user)],db:Session = Depends(get_db)):
    session_save = session_services.create_session(db,session,user)
    return session_save.session_id


@router.post("/{id}/classify")
def classify_user_message():
    pass


@router.post("/{id}/end")
def classify_messages_and_killed_session(id: int , db:Session = Depends(get_db)):
   session = session_services.end_session(id,db)
   session_messages = [MessageBase.model_validate(messages).model_dump() for messages in session.messages]
   session_messages.pop()
   input = session_messages[-1]["content"]
   messages = session_messages
   payload = {"input": input, "messages": messages}
   chatbot_response = requests.post(configs.URL_API_LLM , json = payload).json()
   response = chatbot_response["chatbot_response"]
   chatbot_classification = chatbot_response["classification"]
   classification_schema = CreateClassification(session_id = session.session_id,
                                                categorie = chatbot_classification["categorie"],
                                                emergency_level = chatbot_classification["emergency_level"])
   classification = classsification_service.create_classificaton(classification_schema,db)
   
   return classification


@router.post("/statut")
def create_session_statut(statut:CreateStatut,db:Session = Depends(get_db)):
    statut_id= session_services.create_statut(db,statut)
    return {"id_statut": statut_id}


@router.get("/{id}/messages",response_model = List[MessageBase])
def  get_messages_by_session_id(user: Annotated[UsersModel , Depends(user_services.get_current_user)],
                                session : Annotated[ReadSession,Depends(session_services.get_session_by_id)]):
    
    return session.messages

@router.get("/last")
def get_latest_session_id(db : Session = Depends(get_db)):
    latest_id = session_services.get_latest_id(db)
    return latest_id