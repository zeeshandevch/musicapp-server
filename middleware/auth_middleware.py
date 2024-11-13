import os
from fastapi import HTTPException, Header
import jwt

def auth_middleware(auth_token = Header()):
    try:
        if not auth_token:
            raise HTTPException(401, 'No auth token, access denied!')

        verified_token = jwt.decode(auth_token, str(os.getenv("SECRET_KEY")), ['HS256'])

        if not verified_token:
            raise HTTPException(401, 'Token verification failed, authorization denied!')

        uid = verified_token.get('id')
        return {'uid': uid, 'token': auth_token}

    except jwt.PyJWTError:
        raise HTTPException(401, 'Token is not valid, authorization failed.')