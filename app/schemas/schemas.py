
from __future__ import annotations #store type hint as strings instead of acutual objects ( we can use title: name => even if name is not defined yet)
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional




class createPost(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(max_length=30)      #for number we can use gt and lt liek Field(gt=0, lt=2650)
    is_published: bool = True
    

# class updatePost(createPost):
#     pass

# class newPost(createPost):
#     is_new: bool = True

class Post(createPost):
    # title: str
    # description: str
    created_at: datetime
    # is_published: bool


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    name: str
    job: str | None = None

class User(BaseModel):
    email: EmailStr
    name: str
    created_at: datetime

class loginUser(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None
    
