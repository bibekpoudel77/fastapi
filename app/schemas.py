from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.networks import EmailStr
from typing import Annotated


# schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostUpdate(PostBase):
    pass


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


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    model_config = {"from_attributes": True}


class PostOut(BaseModel):
    Post: Post
    votes: int
    model_config = {"from_attributes": True}


class Vote(BaseModel):
    post_id: int
    # dir must be either 0 or 1
    dir: Annotated[int, Field(strict=True, gt=-1, le=1)]
