from pydantic import BaseModel, Field

from typing import Optional




class ProductSchema(BaseModel):
    name:str
    description:str=Field(min_length=10)
    quantity:int=Field(1)
    price:float=Field(1.0)
    currency:str=Field("JOD")
    image:Optional[str]
    user_id:str
    categuries: str



class ProductUpdate(ProductSchema):
    pass




class ProductBase(BaseModel):
    id : int 
    name : str

    class Config:
        orm_mode = True



class CateguryBase(BaseModel):
    id : int
    name: str

    class Config:
        orm_mode = True
