from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr


# schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }  # This allows the model to read data as dictionaries


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = {
        "from_attributes": True
    }  # This allows the model to read data as dictionaries


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
