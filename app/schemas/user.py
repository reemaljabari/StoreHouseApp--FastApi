from pydantic import BaseModel, Field, EmailStr, validator



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
            "Password":"12345678"
            }
        }
        orm_mode = True
    

    @validator("email")
    def email_validatoer(cls,value, values):
        firstname_validate=values["first_name"]
        if (not value.startswith(firstname_validate.lower())):
            raise ValueError(" Email should start with your first name ")
        return value


    
class UserLoginSchema(BaseModel):
    email:str = Field(max_length=100)
    Password:str = Field(min_length=8)
    class Config:
        schema_extra={
            "example":{
            "email":"reem@gmail.com",
            "Password": "12345678"
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