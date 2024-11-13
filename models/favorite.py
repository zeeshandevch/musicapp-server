from sqlalchemy import Column, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(TEXT, primary_key=True)
    audio_id = Column(TEXT, ForeignKey("audios.id"))
    user_id = Column(TEXT, ForeignKey("users.id"))

    audio = relationship('Audio')
    user = relationship('User', back_populates='favorites')
