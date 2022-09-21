from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import (ALGORITHM, JWT_SECRET_KEY)

from jose import JWTError, jwt
from db import db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


async def authorize(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
  try:     
    payload = jwt.decode(token,JWT_SECRET_KEY,algorithms=ALGORITHM)
    id = payload.get("id")
    username = payload.get("username")

    if id is None:
      print('No Id')
      raise credentials_exception
          #token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception
      #print('looking for id in db')
  user = db.get_user_by('user', 'id', id)
  if user is None:
    print('user is none')
    raise credentials_exception
        
      #return str(user['_id'])
  return {'username': username,'id': id}
