import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env file

database_url = os.environ.get("DATABASE_URL")

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# perfrom database action/query & then close 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()