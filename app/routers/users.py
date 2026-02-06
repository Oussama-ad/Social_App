from fastapi import APIRouter,HTTPException,Depends 
from pydantic import BaseModel  # <--- 1. Import this
from schemas import UserInput,PostInput
from DataBase.db import AsyncSession,get_async_session,Post
import uuid

router=APIRouter()
list1 = ["oussama", "amine", "sarah", "karim", "mohamed"]

@router.get("/") # everything that is a parameter to the functoin it is count as a Query parameter 
def get_users(limit : int = None): # like this the query is optional , to make it mendatory we omete that None 
    if (limit):
        return list1[:limit]
    return list1 

@router.post("/add")
def add_user(user : UserInput):
    list1.append(user.name)
    return {"message":"your user has been added succefully ","your new list ":list1}

@router.get("/{nom}")
def get_user_by_name(nom : str)->UserInput : # this spesefy the type of the output like what we expect in return  
    exist = nom in  list1
    if (exist): 
        return {"name" : "This user exist "}
    raise HTTPException(404,"User not found") # this is used to raise an error 
