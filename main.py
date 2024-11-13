from fastapi import FastAPI
from models.base import Base
from routes import auth, audio
from database import engine


app = FastAPI()

app.include_router(auth.router, prefix='/auth')
app.include_router(audio.router, prefix='/audio')

Base.metadata.create_all(engine)