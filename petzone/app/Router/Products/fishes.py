from fastapi import HTTPException,Depends,status,APIRouter,Response
from ...database import get_db
from typing import List
from ... import models
from ... import schemas
from ... import database
from sqlalchemy.orm import Session

fishes_route=APIRouter(
    tags=['Fishes']
    )

#Add Fishes
@fishes_route.post("/add/fishes",status_code=status.HTTP_201_CREATED)
def add_fishes(payload:schemas.Fishes,db:Session=Depends(get_db)):
    add_query=models.Fishes(**payload.dict())
    db.add(add_query)
    db.commit()
    db.refresh(add_query)
    new_birds=add_query
    return new_birds

#Update Fishes
@fishes_route.put("/update/fishes/{id}")
def update_fishes(id,payload:schemas.Fishes,db:Session=Depends(get_db)):
    db_update=db.query(models.Fishes).filter(models.Fishes.id==id)
    bird=db_update.first()
    if bird == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Fishes data not found")
    db_update.update(payload.dict(),synchronize_session=False)
    db.commit()
    return db_update.first()

#Delete Fishes
@fishes_route.delete("/delete/fishes/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_fishes(id,db:Session=Depends(get_db)):
    db_delete=db.query(models.Fishes).filter(models.Fishes.id == id)
    bird=db_delete.first()
    if bird == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data does not exist")
    db_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Get all Fishes
@fishes_route.get("/fishes",)
def get_all_fishes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fishes = db.query(models.Fishes).offset(skip).limit(limit).all()
    return [fish.__dict__ for fish in fishes]
