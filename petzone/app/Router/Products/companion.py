from fastapi import HTTPException,Depends,status,APIRouter,Response
from ...database import get_db
from typing import List
from ... import models
from ... import schemas
from ... import database
from sqlalchemy.orm import Session


companion_route=APIRouter(
    tags=['Companion']
    )
#Add Companion
@companion_route.post("/add/companion",status_code=status.HTTP_201_CREATED)
def add_companion(payload:schemas.Companion,db:Session=Depends(get_db)):
    add_query=models.Companion(**payload.dict())
    db.add(add_query)
    db.commit()
    db.refresh(add_query)
    new_birds=add_query
    return new_birds

#Update Companion
@companion_route.put("/update/companion/{id}")
def update_companion(id,payload:schemas.Companion,db:Session=Depends(get_db)):
    db_update=db.query(models.Companion).filter(models.Companion.id==id)
    companion=db_update.first()
    if companion == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Companion data not found")
    db_update.update(payload.dict(),synchronize_session=False)
    db.commit()
    return db_update.first()

#Delete Companion
@companion_route.delete("/delete/companion/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_companion(id,db:Session=Depends(get_db)):
    db_delete=db.query(models.Companion).filter(models.Companion.id == id)
    companion=db_delete.first()
    if companion == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data does not exist")
    db_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Get all Companion
@companion_route.get("/companions",)
def get_all_companion(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companions = db.query(models.Companion).offset(skip).limit(limit).all()
    return [companion.__dict__ for companion in companions]





