from random import randrange
from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Wecome to FastAPI"}


records = [
    {"id": 1, "title": "John Doe", "content": 'This is text about John Doe.'},
    {"id": 2, "title": "Jane Smith", "content": 'This is text about Jane Smith.'},
    {"id": 3, "title": "Alice Johnson", "content": 'This is text about Alice Johnson.'},
]

def find_post(id):
    for record in records:
        if record["id"] == id:
            return record
    return None

def find_post_index(id):
    for index, record in enumerate(records):
        if record["id"] == id:
            return index
    return None

#post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


#create
@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(1, 1000000)
    records.append(post_dict)
    return {"post": post_dict}

#read
@app.get("/posts")
async def get_posts():
    return {"posts": records}


@app.get("/post/{id}")
async def get_post(id: int):
    post = find_post(id)
    if post:
        return {"post": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found",
                        headers={"X-Error": "Post not found"})

#update
@app.put("/post/{id}")
async def update_post(id: int, post: Post):
    post_index = find_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found",
                            headers={"X-Error": "Post not found"})
    
    post_dict = post.model_dump()
    post_dict["id"] = id
    records[post_index] = post_dict
    return {"message": "Post updated successfully", "post": post_dict}

#delete
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    post_index = find_post_index(id)
    if post_index is not None:
       records.pop(post_index)
       return Response(status_code=status.HTTP_204_NO_CONTENT)
