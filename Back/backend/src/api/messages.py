from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.orm import Session

from src.schemas import CreateMessage,MessageBase,CreateClassification,ReadSession

from src.models import UsersModel

from src.database import get_db

from services import messages_services,user_services,session_services,classsification_service

import configs

import requests

from typing import Annotated , List

router = APIRouter()


@router.post("")
def conversation_to_chatbot(user : Annotated[UsersModel , Depends(user_services.get_current_user)],
                            message : CreateMessage,
                            db:Session = Depends(get_db)):
     session_message = ReadSession.model_validate(session_services.get_session_by_id(message.session_id,db))
     if session_message.statut_id == 1:
          user_message = messages_services.create_message(message,db)
   #deux problemes au niveaux de la base de donnée(user_id) je m'arrête ici
          messages = [MessageBase.model_validate(message).model_dump() for message in session_message.messages]
          payload = {"input":user_message.content,"messages":messages}
          chatbot_response = requests.post(url = configs.URL_API_LLM , json = payload).json()
          response = chatbot_response["chatbot_response"]
          classification = chatbot_response["classification"]
          chatbot_response_schema = CreateMessage(role = "assistant", 
                                        content = response,
                                        session_id = user_message.session_id)
   
          classify_schema = CreateClassification(session_id=user_message.session_id,
                                                categorie = classification["categorie"],
                                                emergency_level = classification["emergency_level"])
   
          chatbot_message = messages_services.create_message(chatbot_response_schema,db)
          message_classify = classsification_service.create_classificaton(classify_schema,db)
     else : 
          raise HTTPException(status_code = 200 , detail = "Merci d'utiliser notre service")

     return response