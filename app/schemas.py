from pydantic import BaseModel


# schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
