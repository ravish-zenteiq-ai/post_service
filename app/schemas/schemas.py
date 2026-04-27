from pydantic import BaseModel, Field




class createPost(BaseModel):
    title: str
    description: str
    is_published: bool = True

class updatePost(createPost):
    pass

class newPost(createPost):
    is_new: bool = True
    