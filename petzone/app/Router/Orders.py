from fastapi import HTTPException,Depends,status,APIRouter,Response
from ..database import get_db
from typing import List
from .. import models
from . import User
from .. import schemas
from .. import database
from sqlalchemy.orm import Session


orders_route=APIRouter(
    tags=["Orders"]
)

#Create Order

@orders_route.post("/order",status_code=status.HTTP_201_CREATED,response_model=schemas.MyOrder)
def create_order(order:schemas.MyOrder,db:Session=Depends(get_db),current_user:int=Depends(User.get_current_user)):
    print(current_user.id)
    order=models.Orders(owner_id=int(current_user.id),**order.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

# @orders_route.get("/allorders",status_code=status.HTTP_200_OK)
# def get_allorders(db:Session=Depends(get_db)):
#     order=