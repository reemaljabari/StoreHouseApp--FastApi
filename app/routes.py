from fastapi import APIRouter,Body, Depends, HTTPException, status, UploadFile, File, Response, Form
from sqlalchemy.orm import Session


from app.database import get_db
from app.models import User, Product
from app.schemas import UserSchema,Token, UserLoginSchema, ProductSchema, ProductInDB, ProductUpdate
from app.oath2 import get_current_user, create_access_token
from app import utils




authontication=APIRouter(
tags=["authontication"]
)


product=APIRouter(
    tags=["product"]
)



@authontication.post("/signup", status_code= status.HTTP_201_CREATED)
def signup_user(user:UserSchema= Body(), db:Session=Depends(get_db)):
    hashed_password= utils.hash(user.Password)
    user.Password=hashed_password
    user_db=db.query(User).filter(User.email==user.email).first()
    if not user_db:
        new_user=user.dict()
        db_obj= User(**new_user)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return {f" New User : {user.first_name} {user.last_name} added to the Database"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" user already exist , please Login")






@authontication.post("/login", response_model=Token)
def login (user_credentials:UserLoginSchema=Body(), db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credrntials"
        )
    if not utils.verify(user_credentials.Password, user.Password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="INVALID CREDINTIALS"
        )
    token_data={
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name":user.last_name,
        "email": user.email,
        "phone_number": user.phone_number
    }
    acces_token=create_access_token(token_data)
    return {
        "access_token": acces_token,
        "token_type": "bearer"
    }





@product.get("/users/{user_id}/products")
def  get_products(user_id:int,db:Session=Depends(get_db)):
    products=db.query(Product).filter(Product.user_id==user_id).all()
    return products



@product.post("/products",dependencies= [Depends(get_current_user)],response_model=ProductInDB,  status_code=status.HTTP_201_CREATED)
async def create_product(name:str=Form(...),description: str=Form(...),Quantity:str=Form(...),price:float=Form(...),currency:str=Form(...),Image:UploadFile=File(...),user_id:int=Form(...),db:Session=Depends(get_db)):
    
    db_query=db.query(Product).filter(Product.name == name).first()
    if  db_query:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Item already Exist")
            
        
    else:
        product=ProductSchema(name=name, description=description, Quantity=Quantity,price=price, currency=currency, user_id=user_id)
        product.Image= await utils.handle_file_upload(Image)
        product_dict=product.dict()

        db_obj=Product(**product_dict)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return (db_obj)




@product.put("/product/{name}")
def update_product(name:str,updated_product:ProductUpdate,db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    product_query=db.query(Product).filter(Product.name== name)
    product=product_query.first()
    if product==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product => {name} doesn't exist "
        )
    if product.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Unauthorized user"
        )
    product_query.update(updated_product.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()






@product.delete("/product/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(name:str, db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    
    
    product_query=db.query(Product).filter(Product.name==name)
    product=product_query.first()
    if product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product : {name} doesn't exist"
            
        )
    print(current_user)
    if product.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorize"
        )
    product_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


