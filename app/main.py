from fastapi import FastAPI, HTTPException, status, Depends
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session
from .schemas import Post


app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Wecome to FastAPI"}


# create
@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# read
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
            headers={"X-Error": "No posts available"},
        )
    return posts


@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
            headers={"X-Error": "Post not found"},
        )
    return post


# update
@app.put("/post/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
            headers={"X-Error": "Post not found"},
        )

    query.update(updated_post.dict(), synchronize_session=False)  # type: ignore
    db.commit()
    post = query.first()
    return post


# delete
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
            headers={"X-Error": "Post not found"},
        )
    query.delete()
    db.commit()
    return {"message": "Post deleted successfully"}
