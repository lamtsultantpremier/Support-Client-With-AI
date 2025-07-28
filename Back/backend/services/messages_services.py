from src.schemas import CreateMessage,MessageBase

from sqlalchemy.orm import Session

from src.models import MessagesModel

def create_message(message:CreateMessage,db:Session):

    message_created = MessagesModel(content = message.content , session_id = message.session_id , role = message.role)
    db.add(message_created)
    db.commit()
    db.refresh(message_created)

    return message_created
