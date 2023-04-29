from datetime import date
from pydantic import BaseModel,EmailStr,HttpUrl
from typing import Optional


class CommonAttributes(BaseModel):
    name:str
    image:HttpUrl
    price:int


class Birds(CommonAttributes):
    salestype:str

class Companion(CommonAttributes):
    salestype:str

class Fishes(CommonAttributes):
    fishtype:str
    salestype:str

class Foods(CommonAttributes):
    description:str
    weight:str

class Medicines(CommonAttributes):
    weight:str
    for_:str
    description:str

class CreateUser(BaseModel):
    name:str
    email:EmailStr
    password:str

    class Config:
        orm_mode=True


class MyOrder(BaseModel):
    name:str
    # ordered_at:str
    # owner_id:int
    price:int
    image:HttpUrl


class TokenData(BaseModel):
    id:Optional[str]=None


class returnUser(BaseModel):
    email:EmailStr
    id:str
    class Config: #for convert sqlalchemy model to pythondic model
        orm_mode=True


