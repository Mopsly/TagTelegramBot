from sqlalchemy import Column, Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    tg_id = Column(Integer, primary_key=True)
    tag = Column(String)
    set_up = Column(Boolean)
    aliases = relationship("Alias", back_populates="owner")


class Alias(Base):
    __tablename__ = 'aliases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    chat_id = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.tg_id"))

    owner = relationship("User", back_populates="aliases")
