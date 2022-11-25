from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload


from app.database import get_db
from app.models import Categury, Product
from app.oath2 import get_current_user



categury=APIRouter(tags=["Categury"])


@categury.post("/categury/{name}", dependencies= [Depends(get_current_user)] ,status_code=status.HTTP_201_CREATED)
def add_categury(categury_name: str, db:Session=Depends(get_db)):
    db_query=db.query(Categury).filter(Categury.name == categury_name).first()
    if db_query:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail= "Categury already Exist")
    db_obj=Categury(name=categury_name)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return {
        "message": "add to the Database",
        "data": db_obj
    }
    


@categury.get("/categuries",dependencies= [Depends(get_current_user)], status_code= status.HTTP_200_OK)
def get_categuries(db : Session=Depends(get_db)):
    categuries= db.query(Categury).all()
    if not categuries:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "No Categuries"
        )
    return categuries


@categury.get("/categuries/{categury_id}",dependencies= [Depends(get_current_user)], status_code= status.HTTP_200_OK)
def get_categuryByid(categury_id : int, db: Session= Depends(get_db)):
    db_query = db.query(Categury).options(joinedload(Categury.products)).where(Categury.id == categury_id).one()
    return db_query

@categury.post("/categuries/{categury_id}/products/{product_id}", dependencies= [Depends(get_current_user)], status_code=status.HTTP_201_CREATED)
def add_product_to_categury(categury_id : int, product_id: int,  db: Session= Depends(get_db)):
    categury=db.query(Categury).where(Categury.id == categury_id).first()
    product=db.query(Product).where(Product.id == product_id).first()
    categury.products.append(product)
    db.commit()


