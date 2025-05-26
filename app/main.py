from fastapi import FastAPI, HTTPException, status, Depends
from .database import engine, get_db
from . import models, utils, schemas
from sqlalchemy.orm import Session
from .schemas import PostBase, Post

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Wecome to FastAPI"}


# create
@app.post("/post", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# read
@app.get("/posts", response_model=list[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
            headers={"X-Error": "No posts available"},
        )
    return posts


@app.get("/post/{id}", response_model=Post)
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
@app.put("/post/{id}", response_model=Post)
def update_post(id: int, updated_post: PostBase, db: Session = Depends(get_db)):
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


# Users CREATE
@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Users READ
@app.get("/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if users is None or len(users) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
            headers={"X-Error": "No users available"},
        )
    return users


@app.get("/user/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
            headers={"X-Error": "No users available"},
        )
    return user


# Users UPDATE
@app.put("/user/{id}", response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
            headers={"X-Error": "User not found"},
        )
    updated_user.password = utils.hash(updated_user.password)
    user.update(updated_user.dict(), synchronize_session=False)  # type: ignore
    db.commit()
    return user.first()


# Users DELETE
@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    if query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
            headers={"X-Error": "User not found"},
        )
    query.delete()
    db.commit()
    return {"message": "User deleted successfully"}
