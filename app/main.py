from fastapi import FastAPI


from app.routes import authontication, product




application=FastAPI(title="StoreHouse App")



application.include_router(router= authontication)
application.include_router(router=product)