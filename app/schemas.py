from pydantic import BaseModel , Field
import datetime
from typing import Optional
class UserInput(BaseModel): 
    name:str 


class PostInput(BaseModel): 
    caption : Optional[str] =Field(None, description="Post caption") #to make it optional , field is todefine the value basic  
    url_image: Optional[str] = Field(
        None, 
        description="Image URL (will be auto-generated if not provided)"
    )
    file_type: Optional[str] = Field(
        None,
        description="File type (will be auto-generated if not provided)"
    )
    file_name: Optional[str] = Field(
        None,
        description="File name (will be auto-generated if not provided)"
    ) 
