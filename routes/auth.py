
import os
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
import uuid
import bcrypt
import jwt

from database import get_db
from middleware.auth_middleware import auth_middleware
from models.user import User
from schemas.user_create import UserCreate
from schemas.user_login import UserLogin

router = APIRouter()

@router.post('/signup', status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    #check if the user already exist in db
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(400, "User with same email already exists!")
    #add the user to the db
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_add = User(id = str(uuid.uuid4()), name = user.name, email = user.email, password = hashed_pw)
    db.add(user_add)
    db.commit()
    db.refresh()

    return {
        "Message" : "Sign up Successfully!"
    }

@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    #check if the user email already exist in db
    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(400, "User with this email does not exists!")
    
    #password matching or not
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)

    if not is_match:
        raise HTTPException(400, "Incorrect password!")
    
    jwt_token = jwt.encode({'id' : user_db.id}, str(os.getenv("SECRET_KEY")),)

    return {
        'token' : jwt_token,
        'user' : {
            'id' : user_db.id,
            'name' : user_db.name,
            'email' : user_db.email,
        }
    }


@router.get('/')
def current_user_data(db: Session=Depends(get_db), 
                      user_dict = Depends(auth_middleware)):
    user = db.query(User).filter(User.id == user_dict['uid']).options(
        joinedload(User.favorites)
    ).first()

    if not user:
        raise HTTPException(404, 'User not found!')
    
    return user