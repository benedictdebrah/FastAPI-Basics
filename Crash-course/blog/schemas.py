from pydantic import BaseModel
from typing import Optional





class Blog(BaseModel):
    title :str
    body : str 

class ShowBlog(BaseModel): 
    title :str
    body : str 

    class Config():
        from_attributes = True 

class User(BaseModel):
    name : str
    email : str
    password : str

class ShowUser(BaseModel):
    name : str
    email : str

    class Config():
        from_attributes = True