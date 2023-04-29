from fastapi import FastAPI,status,Depends;
from . import models;
from .database import engine,get_db
from .Router.Products import birds,fishes,companion,foods,medicens
from .Router import Orders
from .Router import User
from .database import get_db
from . import models
from . import database
from sqlalchemy.orm import Session
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()
@app.get("/testing",status_code=status.HTTP_200_OK)
def testing():
    return {"test":"tesing"}
#create data base
models.Base.metadata.create_all(bind=engine)



#adding cors urls
origins=[
    "*"
]

#add middleware

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"]
)





app.include_router(User.user_route)
app.include_router(Orders.orders_route)
app.include_router(fishes.fishes_route)
app.include_router(birds.birds_route)
app.include_router(foods.foods_route)
app.include_router(companion.companion_route)
app.include_router(medicens.medicens_route)

@app.get("/all_products")
def all_products(db:Session=Depends(get_db)):
    birds=db.query(models.Birds).count()
    fishes=db.query(models.Fishes).count()
    foods=db.query(models.Foods).count()
    medicine=db.query(models.Medicines).count()
    companion=db.query(models.Companion).count()

    total=int(birds)+int(fishes)+int(foods)+int(medicine)+int(companion)


    return {"total":total}
