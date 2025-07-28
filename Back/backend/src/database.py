import configs
from src.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session

engine=create_engine(configs.DATABASE_URL)

Base.metadata.create_all(bind=engine)

LocalSession=sessionmaker(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()