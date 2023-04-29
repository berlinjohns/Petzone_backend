
from sqlalchemy import Column, Integer,String,Float,DATE,SMALLINT,ForeignKey,BigInteger,DateTime,TIMESTAMP
from .database import Base
import datetime as _dt
import passlib.hash as _hash
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String,unique=True,index=True)
    password=Column(String)
    created_date=Column(DateTime,default=_dt.datetime.utcnow)
    def verify_password(self,password:str):
        return _hash.bcrypt.verify(password,self.password)



class Birds(Base):
    __tablename__="birds"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String(30),nullable=False,unique=False)
    image=Column(String(300),nullable=False,unique=True)
    price=Column(BigInteger,nullable=False)
    salestype=Column(String(10),nullable=False,unique=False)
    


class Companion(Base):
    __tablename__="companions"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String(30),nullable=False,unique=False)
    image=Column(String(300),nullable=False,unique=True)
    price=Column(BigInteger,nullable=False)
    salestype=Column(String(10),nullable=False,unique=False)

class Fishes(Base):
    __tablename__="fishes"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String(30),nullable=False,unique=False)
    image=Column(String(300),nullable=False,unique=True)
    price=Column(BigInteger,nullable=False)
    fishtype=Column(String(30),nullable=False,unique=False)
    salestype=Column(String(10),nullable=False,unique=False)
    

class Foods(Base):
    __tablename__="foods"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String(30),nullable=False,unique=False)
    image=Column(String(300),nullable=False,unique=True)
    price=Column(Integer,nullable=False)
    description=Column(String(300),nullable=False,unique=True)
    weight=Column(String(10),nullable=False)

class Medicines(Base):
    __tablename__="medicines"
    image=Column(String(300),nullable=False,unique=True)
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String(40),nullable=False,unique=False)
    price=Column(Integer,nullable=False)
    weight=Column(String(10),nullable=False,)
    for_=Column(String(15),nullable=False)
    description=Column(String(300),nullable=False)

class Orders(Base):
    __tablename__="orders"
    ordered_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    image=Column(String(300),nullable=False,unique=True)
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String(40),nullable=False,unique=False)
    price=Column(Integer,nullable=False)

