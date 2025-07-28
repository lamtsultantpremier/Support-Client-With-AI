
from src.schemas import CreateClassification,ReadClassification
from sqlalchemy.orm import Session
from src.models import ClassificationsModel
def create_classificaton(classification : CreateClassification, db:Session):
    message_classify = ClassificationsModel(session_id = classification.session_id,
                                            categorie = classification.categorie,
                                            emergency_level = classification.emergency_level)
    db.add(message_classify)
    db.commit()
    db.refresh(message_classify)
    return ReadClassification.model_validate(message_classify)