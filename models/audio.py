from sqlalchemy import TEXT, VARCHAR, Column
from models.base import Base

class Audio(Base):
    __tablename__ = 'audios'

    id = Column(TEXT, primary_key=True)
    audio_url = Column(TEXT)
    thumbnail_url = Column(TEXT)
    artist = Column(TEXT)
    audio_name = Column(VARCHAR(100))
    hex_code = Column(VARCHAR(6))