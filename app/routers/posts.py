from fastapi import APIRouter,HTTPException,Depends 
from pydantic import BaseModel  # <--- 1. Import this
from schemas import UserInput,PostInput
from DataBase.db import AsyncSession,get_async_session,Post
import uuid
from sqlalchemy import Select
router = APIRouter()

@router.post("/upload")
async def add_post(post_input : PostInput , session : AsyncSession =Depends(get_async_session) ): # that depends lets fast api create the session by its self
# we are not adding it in the request body 
    newpost= Post(
    Caption = post_input.caption , 
    url_image=post_input.url_image,
    file_type=post_input.file_type,
    file_name=post_input.file_name,
       )
    session.add(newpost)
    await session.commit()
    await session.refresh(newpost) 
    return {"message":"User added succefully to the Database","User": newpost}

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
