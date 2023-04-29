from fastapi import HTTPException,Depends,status,APIRouter,Response,security
from ..database import get_db
from typing import List
from .. import models
from .. import schemas
from .. import database
from sqlalchemy.orm import Session
# import passlib.hash as hash
from .utils import hash
import jwt as _jwt
from jwt import PyJWTError
from fastapi.security import OAuth2AuthorizationCodeBearer 
from ..config import settings



oauth2_scheme=OAuth2AuthorizationCodeBearer(tokenUrl='login',authorizationUrl='login')


_JWT_SECRET=settings.secret_key
#Create User

user_route=APIRouter(
    tags=['User']
    )

async def get_user_by_email(email:str,db:Session=Depends(get_db)):
    return db.query(models.User).filter(models.User.email == email).first()

async def creating_user(payload:schemas.CreateUser,db:Session=Depends(get_db)):
    hashed_password=hash(payload.password)
    user_object=models.User(email=payload.email,password=hashed_password,name=payload.name)
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object

async def create_token(payload:models.User):
    user_schema_obj=schemas.CreateUser.from_orm(payload)
    user_dict=user_schema_obj.dict()
    print(user_dict)
    # del user_dict["created_date"]
    token=_jwt.encode(user_dict,_JWT_SECRET)

    return dict(access_token=token,token_type="bearer")

@user_route.post("/user/create")
async def create_user(payload:schemas.CreateUser,db:Session=Depends(get_db),response_model=schemas.returnUser):
    db_user=await get_user_by_email(email=payload.email,db=db)
    if db_user:
        raise HTTPException(
            status_code=400,detail="User with that email already exists"
        )
    #cerete the user
    user=await creating_user(payload=payload,db=db)

    return await create_token(payload=user)

async def authenticate_user(email:str,password:str,db:Session=Depends(get_db)):
    user=await get_user_by_email(email=email,db=db)
    if not user:
        return False
    if not user.verify_password(password=password):
        return False
    
    return user

@user_route.post("/user/login")
async def generate_token(payload:security.OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email == payload.username).first()
    user=await authenticate_user(email=payload.username,password=payload.password,db=db)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    return  create_access_token(data={"user_id":user.id})

def verify_access_token(token:str,credential_exception):

    try:
         payload=_jwt.decode(token,_JWT_SECRET,algorithms=['HS256'])

         id:str = payload.get("user_id")

         if id is None:
             raise credential_exception
         token_data=schemas.TokenData(id=id)
    except PyJWTError:
        raise credential_exception

    return token_data

def get_current_user(token:str=Depends(oauth2_scheme)):
   credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                   detail=f"Could not validate credentials",headers={"WWW-Authorization":"Bearer"})
                
   return verify_access_token(token,credential_exception)


def create_access_token(data:dict):
    to_encode=data.copy()

   

    encoded_jwt = _jwt.encode(to_encode,_JWT_SECRET,algorithm='HS256')

    return encoded_jwt