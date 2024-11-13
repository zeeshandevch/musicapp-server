
import os
import uuid
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session, joinedload

from database import get_db
from middleware.auth_middleware import auth_middleware
from models.audio import Audio
from models.favorite import Favorite
from schemas.favorite_audio import FavoriteAudio

router = APIRouter()

# Configuration       
cloudinary.config( 
    cloud_name = str(os.getenv("CLOUD_NAME")), 
    api_key = str(os.getenv("CLOUD_API_KEY")), 
    api_secret = str(os.getenv("CLOUD_SECRET_KEY")),
    secure=True
)

### Upload Audio End point
@router.post('/upload', status_code=201)
def upload_audio(
    audio: UploadFile = File(...),
    thumbnail : UploadFile = File(...),
    artist : str = Form(...),
    audio_name : str = Form(...),
    hex_code : str = Form(...),
    db : Session = Depends(get_db),
    auth_dict = Depends(auth_middleware),
    ):
    audio_id = str(uuid.uuid4())
    audio_res = cloudinary.uploader.upload(audio.file, resource_type = 'auto', folder = f'audios/{audio_id}')
    # print(f'Audio File Response : {audio_res['url']}') #for testing
    thumbnail_res = cloudinary.uploader.upload(thumbnail.file, resource_type = 'image', folder = f'audios/{audio_id}')
    # print(f'Thumbnail Response : {thumbnail_res['url']}') #for testing
    
    new_audio = Audio(
        id = audio_id,
        audio_name = audio_name,
        artist = artist,
        hex_code = hex_code,
        audio_url = audio_res['url'],
        thumbnail_url = thumbnail_res['url'],
    )

    db.add(new_audio)
    db.commit()
    db.refresh(new_audio)
    return new_audio


### Get Audio List End point
@router.get('/list')
def list_audio(
    db : Session = Depends(get_db),
    auth_dict = Depends(auth_middleware),
    ):
    audios = db.query(Audio).all()
    return audios

### Audio Favorite End point
@router.post('/favorite')
def favorite_audio(
    audio : FavoriteAudio,
    db : Session = Depends(get_db),
    auth_dict = Depends(auth_middleware),
    ):

    user_id = auth_dict['uid']

    fav_audio = db.query(Favorite).filter(Favorite.audio_id == audio.audio_id, Favorite.user_id == user_id).first()

    if fav_audio :
        db.delete(fav_audio)
        db.commit()
        return {'Message' : False}
    else:
        new_fav = Favorite(id = str(uuid.uuid4()), audio_id = audio.audio_id, user_id = user_id)
        db.add(new_fav)
        db.commit()
        return {'Message' : True}
    

### Get Favorites Audio List End point
@router.get('/list/favorites')
def list_audio(
    db : Session = Depends(get_db),
    auth_dict = Depends(auth_middleware),
    ):
    user_id = auth_dict['uid']
    fav_audios = db.query(Favorite).filter(Favorite.user_id == user_id).options(
        joinedload(Favorite.audio)
    ).all()
    return fav_audios