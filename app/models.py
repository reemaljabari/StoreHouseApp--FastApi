from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base



products_categuries=Table("products_categuries", Base.metadata,
Column("product_id",ForeignKey("products.id")),
Column("categury_id", ForeignKey("categuries.id"))
)

class Product(Base):
    __tablename__="products"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, index=True, nullable=False, unique=True)
    description=Column(String, nullable=True)
    Quantity=Column(Integer, default=0)
    price=Column(Float, nullable=False)
    currency=Column(String, default="JOD", nullable=False)
    Image=Column(String)
    categuries=relationship("Categury", secondary="products_categuries", back_populates="products" )
    user_id=Column(Integer, ForeignKey("users.id"))
    product_creator=relationship("User", back_populates="products", uselist=False)


class Categury(Base):
    __tablename__="categuries"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String,  nullable=False)
    products=relationship("Product", secondary="products_categuries", back_populates="categuries")


class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    first_name=Column(String, nullable=False)
    last_name=Column(String,nullable=False)
    email=Column(String, unique=True, nullable=False)
    phone_number=Column(String, nullable=False)
    Password=Column(String, nullable=False)
    products=relationship("Product", back_populates="product_creator")