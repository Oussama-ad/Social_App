from fastapi import FastAPI 
from routers import users, posts
from DataBase.db import create_db_and_tables
from contextlib import asynccontextmanager
from images import imagekit
import shutil
import uuid
import tempfile
import os 

@asynccontextmanager
async def lifespan(app : FastAPI): # here we are defing le comportement of the application 
    await create_db_and_tables() # we tell it start by creating the tables and then continue 
    yield # continue 

app = FastAPI(lifespan=lifespan) # the parameter is for calling the functon above so it starts working 

#including the routers here 
app.include_router(users.router,prefix="/users",tags=["Users"])
app.include_router(posts.router,prefix="/posts",tags=["Posts"])


@app.get("/")
def hello():
    return {"message":"Hello from fast"} 
   