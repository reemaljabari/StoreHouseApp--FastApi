from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload


from app.database import get_db
from app.models import Product
from app.schemas.product import  ProductSchema
from app.oath2 import get_current_user
from app import utils




product=APIRouter(
    tags=["product"],
    prefix="/users"
)


@product.get("/{user_id}/products", status_code=status.HTTP_200_OK)
def  get_products(user_id:int, db:Session=Depends(get_db)):
    db_query=db.query(Product).filter(Product.user_id==user_id)
    products=db_query.all()

    if  products :
        return products
    return {
            "This User Has no products"
        }



@product.post("/products" , status_code= status.HTTP_201_CREATED)
async def create_product(data=Depends(get_current_user), name:str=Form(...), description: str=Form(...), quantity:str=Form(...), price:float=Form(...),currency:str=Form(...),  image:UploadFile=File(None),db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    
    db_query=db.query(Product).filter(Product.name == name).first()
    if  db_query:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Item already Exist")

    else:
        product=ProductSchema(name=name, description=description, quantity=quantity,price=price, currency=currency, user_id=data["user_id"])
        product.image= await utils.handle_file_upload(image)
        
        product_dict=product.dict()
        db_obj=Product(**product_dict)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return {
                "message": " Add new Product",
                "Data": db_obj
            }


# @product.put("/products/{product_id}")
# async def update_product(product_id: int, product: ProductUpdate, image:UploadFile=File(None), db:Session=Depends(get_db), current_user=Depends(get_current_user)):
#     if product.user_id != current_user["user_id"]:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not Authorize"
#         )

#     db_product=db.query(Product).filter(Product.id == product_id).first()
#     if not db_product:
#             raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Product not found")

#     if image:
#         product.image= await utils.handle_file_upload(image)

#     product_data = product.dict(exclude_unset=True)
#     for key, value in product_data.items():
#         setattr(db_product, key, value)
#         db.add(db_product)
#         db.commit()
#         db.refresh(db_product)
#         return db_product



@product.delete("/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id:int , db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    
    if product.user_id != current_user["user_id"]:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not Authorize"
        )
    
    product_query=db.query(Product).filter(Product.id==product_id)
    product=product_query.first()
    if product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with ID  ({product_id})  doesn't exist"
            
        )

    if product.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorize"
        )
    product_query.delete(synchronize_session=False)
    db.commit()


@product.get("/products/{product_id}")
def get_product(product_id: int , db: Session = Depends(get_db)):
    db_product= db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        return {" No Product Available with This ID "}
    return db_product




