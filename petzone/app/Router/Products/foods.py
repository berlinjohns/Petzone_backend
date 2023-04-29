from fastapi import HTTPException,Depends,status,APIRouter,Response
from ...database import get_db
from typing import List
from ... import models
from ... import schemas
from ... import database
from sqlalchemy.orm import Session


foods_route=APIRouter(
    tags=['foods']
    )

#Add Food

@foods_route.post("/add/foods",status_code=status.HTTP_201_CREATED)
def addBirds(payload:schemas.Foods,db:Session=Depends(get_db)):
    add_query=models.Foods(**payload.dict())
    db.add(add_query)
    db.commit()
    db.refresh(add_query)
    new_foods=add_query
    return new_foods

#Update  Food
@foods_route.put("/update/foods/{id}")
def updateBirds(id,payload:schemas.Foods,db:Session=Depends(get_db)):
    db_update=db.query(models.Foods).filter(models.Foods.id==id)
    food=db_update.first()
    if food == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Foods data not found")
    db_update.update(payload.dict(),synchronize_session=False)
    db.commit()
    return db_update.first()

#Delete FOODS

@foods_route.delete("/delete/foods/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_foods(id,db:Session=Depends(get_db)):
    db_delete=db.query(models.Foods).filter(models.Foods.id == id)
    food=db_delete.first()
    if food == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data does not exist")
    db_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Get Food BY ID

#GET ALL FOODS
@foods_route.get("/foods", )
def get_all_foods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    foods = db.query(models.Foods).offset(skip).limit(limit).all()
    return [food.__dict__ for food in foods]




