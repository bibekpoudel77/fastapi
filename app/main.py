from random import randrange
from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

#connect to postgres database
while True:
    try:
        conn = psycopg2.connect(
            dbname="fastapi",
            user="postgres",
            password="root",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Unable to connect to the database. Retrying...")
        time.sleep(5)

@app.get("/")
async def root():
    return {"message": "Wecome to FastAPI"}

#post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


#create
@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published) )
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": "Post created successfully", "data": new_post}

#read
@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"posts": posts}


@app.get("/post/{id}")
async def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found",
                        headers={"X-Error": "Post not found"})
    return {"data": post}

#update
@app.put("/post/{id}")
async def update_post(id: int, post: Post):
    cursor.execute(
            "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
            (post.title, post.content, post.published, id)
        )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found",
                            headers={"X-Error": "Post not found"})
    return {"message": "Post updated successfully", "data": updated_post}

#delete
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found",
                            headers={"X-Error": "Post not found"})
    return {"message": "Post deleted successfully"}

