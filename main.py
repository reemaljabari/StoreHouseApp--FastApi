from fastapi import FastAPI


from app.routes.authentication import authontication
from app.routes.product import product
from app.routes.categury import categury


app=FastAPI(title="StoreHouse App")



app.include_router(router= authontication)
app.include_router(router=product)
app.include_router(router=categury)