from fastapi import APIRouter,HTTPException,Depends ,UploadFile ,File,Form
from pydantic import BaseModel  # <--- 1. Import this
from schemas import UserInput,PostInput
from DataBase.db import AsyncSession,get_async_session,Post
import uuid
import shutil
import tempfile
import os
from images import imagekit
from sqlalchemy import Select

router = APIRouter()

@router.post("/upload")
async def add_post(file: UploadFile = File(...),
                   caption: str = Form(...),
                   session: AsyncSession = Depends(get_async_session)):
    
    tmp_file_path = None
    
    try:
        # 1. Create a temp file and write the upload to it
        # We use delete=False so we can re-open it for reading in step 2
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            tmp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        # The temp_file is automatically CLOSED here for writing.

        # 2. Re-open the file for READING to send to ImageKit
        # We use a 'with' block here so it CLOSES immediately after upload
        with open(tmp_file_path, "rb") as file_to_upload:
            result = imagekit.files.upload(
                file=file_to_upload,  # Use the file object we just opened
                file_name=file.filename,
                use_unique_file_name=True,
                tags=["backend-upload"]
            )

        # 3. Check success and save to DB
        if result.file_id:
            newpost = Post(
                Caption=caption,
                url_image=result.url,
                # Simple logic to determine type
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=result.name,
            )
            session.add(newpost)
            await session.commit()
            await session.refresh(newpost)
            return {"message": "User added successfully to the Database", "User": newpost}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
        # 4. Cleanup
        # Since the 'with' block in step 2 is finished, the file is definitely closed now.
        # We can safely delete it without PermissionError.
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        # Close the original uploaded file stream from FastAPI
        file.file.close()

# @router.post("/upload")
# async def add_post(
#                    post_input : PostInput ,
#                      session : AsyncSession =Depends(get_async_session) ): # that depends lets fast api create the session by its self
# # we are not adding it in the request body 
#     newpost= Post(
#     Caption = post_input.caption , 
#     url_image=post_input.url_image,
#     file_type=post_input.file_type,
#     file_name=post_input.file_name,
#        )
#     session.add(newpost)
#     await session.commit()
#     await session.refresh(newpost) 
#     return {"message":"User added succefully to the Database","User": newpost}



@router.get("/display")
async def get_all_posts(session : AsyncSession=Depends(get_async_session)): 
  try:
    query = Select(Post).order_by(Post.created_at.desc()) # this is like ( SELECT * FROM posts ) after it is a filter to get them basing on the cretaed at field 
    res =await  session.execute(query) # this is to tell the orm to execute this query 
    posts = res.scalars().all() # to transform it to a list in python and get everything in it 
    return {
       "message":"Those are all the posts", 
       "Posts": posts , 
       "total": len(posts)

    }
  except Exception as e :  
    raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
