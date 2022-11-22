
from passlib.context import CryptContext
from fastapi import UploadFile, HTTPException
import uuid, aiofiles
import os


PWD_CONTENT=CryptContext(schemes=["bcrypt"], deprecated="auto")
BASEDIR=os.path.dirname(__file__)




def hash(password:str):
    return PWD_CONTENT.hash(password)


def verify(plain_password, hashed_password):
    return PWD_CONTENT.verify(plain_password, hashed_password)



async def handle_file_upload(file:UploadFile):
    _, ext = os.path.splitext(file.filename)
    img_dir = os.path.join(BASEDIR, 'uploads/')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'
    async with aiofiles.open(os.path.join(img_dir, file_name), mode='wb') as f:
        await f.write(content)

    return file_name
