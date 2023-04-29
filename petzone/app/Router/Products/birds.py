from fastapi import HTTPException,Depends,status,APIRouter,Response
from ...database import get_db
from typing import List
from ... import models
from ... import schemas
from ... import database
from sqlalchemy.orm import Session


birds_route=APIRouter(
    tags=['Birds']
    )
#Add Birds
@birds_route.post("/add/birds",status_code=status.HTTP_201_CREATED)
def addBirds(payload:schemas.Birds,db:Session=Depends(get_db)):
    add_query=models.Birds(**payload.dict())
    db.add(add_query)
    db.commit()
    db.refresh(add_query)
    new_birds=add_query
    return new_birds

#Update Birds
@birds_route.put("/update/birds/{id}")
def updateBirds(id,payload:schemas.Birds,db:Session=Depends(get_db)):
    db_update=db.query(models.Birds).filter(models.Birds.id==id)
    bird=db_update.first()
    if bird == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Birds data not found")
    db_update.update(payload.dict(),synchronize_session=False)
    db.commit()
    return db_update.first()

#Delete Birds
@birds_route.delete("/delete/birds/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleteBirds(id,db:Session=Depends(get_db)):
    db_delete=db.query(models.Birds).filter(models.Birds.id == id)
    bird=db_delete.first()
    if bird == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data does not exist")
    db_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Get all Birds
@birds_route.get("/birds",)
def get_all_birds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    birds = db.query(models.Birds).offset(skip).limit(limit).all()
    return [bird.__dict__ for bird in birds]





