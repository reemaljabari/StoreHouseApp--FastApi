from pydantic import BaseModel, Field, EmailStr

from typing import Optional

class UserSchema(BaseModel):
    first_name:str=Field(max_length=15)
    last_name:str=Field(max_length=15)
    email:EmailStr= Field()
    phone_number:str = Field(max_length=10)
    Password:str = Field(min_length=8)
    class Config:
        schema_extra={
            "example":{
            "first_name":"Reem",
            "last_name":"aljabari",
            "email":"reem@gmail.com",
            "phone_number":"0799999999",
            "Password":"12@345"
            }
        }
        orm_mode = True
    



class UserLoginSchema(BaseModel):
    email:str = Field(max_length=100)
    Password:str = Field(min_length=8)
    class Config:
        schema_extra={
            "example":{
            "email":"reem@gmail.com",
            "Password": "12@345"
            }
        }

    orm_mode = True


class UserOutSchema(BaseModel):
    id:int
    email:str

    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token:str
    token_type:str

    class Config:
        orm_mode=True




class ProductSchema(BaseModel):
    name:str
    description:str=Field(min_length=10, default="Descirbe the product that you made ")
    Quantity:int=Field(1)
    price:float=Field(1.0)
    currency:str=Field("JOD")
    Image:Optional[str]
    user_id:int



class ProductInDB(ProductSchema):
    class Config:
            orm_mode = True


class ProductUpdate(BaseModel):
    description:str=Field(min_length=10, default="Descirbe the product that you made ")
    Quantity:int=Field(1)
    price:float=Field(1.0)
    currency:str=Field("JOD")
    class Config:
        orm_mode=True