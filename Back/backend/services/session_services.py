from dataclasses import dataclass
from sqlalchemy.orm import Session
from src.schemas import CreateSession,ReadUser,CreateStatut,ReadSession,ReadMessage,MessageBase
from src.models import StatutModel,SessionsModel
from fastapi import Depends,HTTPException
from src.database import get_db

def create_session(db:Session,session:CreateSession,user: ReadUser):

    db_statut = db.query(StatutModel).filter(StatutModel.id == session.statut_id).first()
    save_session = SessionsModel(user_id = user.user_id , statut_id = db_statut.id)
    db.add(save_session)
    db.commit()
    db.refresh(save_session)
    return ReadSession.model_validate(save_session)

def create_statut(db:Session,statut:CreateStatut):
    
    statut_save = StatutModel(
        libelle = statut.libelle
    )
    db.add(statut_save)
    db.commit()
    db.refresh(statut_save)
    return statut_save.id

def get_messages(session: ReadSession, db:Session):
    sessions_binding = db.query(SessionsModel).filter(SessionsModel.session_id == session.session_id).first()
    messages = sessions_binding.messages
    return messages

def get_session_by_id(id: int,db:Session = Depends(get_db))->ReadSession:
    session = db.query(SessionsModel).filter(SessionsModel.session_id == id).first()
    if session is None:
        raise HTTPException(status_code = 404, detail = "Session not Found")
    return session

def end_session(id: int , db:Session):
    session = db.query(SessionsModel).filter(SessionsModel.session_id == id).first()
    if session is None:
        raise HTTPException(status_code = 404 , detail = "Session not Found")
    session.statut_id =2
    db.commit()
    return ReadSession.model_validate(session)

def get_latest_id(db : Session):
    last_session = db.query(SessionsModel).filter(SessionsModel)