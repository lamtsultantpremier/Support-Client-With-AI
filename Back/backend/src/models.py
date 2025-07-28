from sqlalchemy.orm import (DeclarativeBase,
                            MappedAsDataclass,
                            Mapped,
                            mapped_column,relationship)
from sqlalchemy import ForeignKey
from sqlalchemy import String
from typing import List,Optional

class Base(DeclarativeBase,MappedAsDataclass):
    pass

class UsersModel(Base):
    __tablename__="users"
    user_id:Mapped[int] = mapped_column(init=False,name="user_id",primary_key=True,autoincrement=True)
    nom:Mapped[str] = mapped_column(String(100))
    prenom:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(100))
    password:Mapped[str] = mapped_column(String(100))
    sessions:Mapped[List["SessionsModel"]] = relationship(default_factory=list)

class StatutModel(Base):
    __tablename__="statut"
    id:Mapped[int] = mapped_column(name="status_id",init=False,primary_key=True,autoincrement=True)
    libelle:Mapped[str] = mapped_column(String(50))
    sessions:Mapped["SessionsModel"] = relationship(back_populates="statut",init=False)

class MessagesModel(Base):
    __tablename__="messages"
    id:Mapped[int] = mapped_column(name="message_id",init=False,primary_key=True,autoincrement=True)
    content:Mapped[str]=mapped_column()
    role: Mapped[str]=mapped_column(String(250))
    session_id:Mapped[int]=mapped_column(ForeignKey("sessions.session_id"))

class SessionsModel(Base):
    __tablename__="sessions"
    session_id:Mapped[int] = mapped_column(name="session_id",init=False,primary_key=True,autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    statut_id:Mapped[int] = mapped_column(ForeignKey("statut.status_id"))
    statut:Mapped[StatutModel]=relationship(back_populates="sessions",init = False)
    
    classification:Mapped["ClassificationsModel"]=relationship(back_populates="session",uselist=False,default=None)
    messages:Mapped[List[MessagesModel]]=relationship(default_factory = list)

class ClassificationsModel(Base):
    __tablename__="classifications"
    id:Mapped[int]=mapped_column(name="class_id",init=False,primary_key=True,autoincrement=True)
    categorie:Mapped[str]=mapped_column()
    emergency_level:Mapped[str]=mapped_column()
    session_id:Mapped[int]=mapped_column(ForeignKey("sessions.session_id"))
    session:Mapped["SessionsModel"]=relationship(back_populates="classification",single_parent=True,init = False)
