from fastapi import HTTPException,Depends,status,APIRouter,Response
from ...database import get_db
from typing import List
from ... import models
from ... import schemas
from ... import database
from sqlalchemy.orm import Session


medicens_route=APIRouter(
    tags=['pets medicens']
    )


@medicens_route.post("/add/medicine",status_code=status.HTTP_201_CREATED)
def add_medicine(payload:schemas.Medicines,db:Session=Depends(get_db)):
    add_query=models.Medicines(**payload.dict())
    db.add(add_query)
    db.commit()
    db.refresh(add_query)
    new_foods=add_query
    return new_foods

#Update  Medicine
@medicens_route.put("/update/medicines/{id}")
def update_medicine(id,payload:schemas.Medicines,db:Session=Depends(get_db)):
    db_update=db.query(models.Medicines).filter(models.Medicines.id==id)
    food=db_update.first()
    if food == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Medicines data not found")
    db_update.update(payload.dict(),synchronize_session=False)
    db.commit()
    return db_update.first()

#Delete FOODS

@medicens_route.delete("/delete/medicines/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_medicine(id,db:Session=Depends(get_db)):
    db_delete=db.query(models.Medicines).filter(models.Medicines.id == id)
    food=db_delete.first()
    if food == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data does not exist")
    db_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Get Medicine BY ID

#GET ALL FOODS
@medicens_route.get("/medicines", response_model=List[schemas.Medicines])
def get_all_medicine(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medicines = db.query(models.Medicines).offset(skip).limit(limit).all()
    return [medicine.__dict__ for medicine in medicines]