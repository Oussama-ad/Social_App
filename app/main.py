from fastapi import FastAPI 
from routers import users
app = FastAPI()

#including the routers here 
app.include_router(users.router,prefix="/users",tags=["Users"])

@app.get("/")
def hello():
    return {"message":"Hello from fast"} 
   