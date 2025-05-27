from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from .. import models, oauth2
from sqlalchemy.orm import Session
from ..schemas import PostBase, Post, TokenData

router = APIRouter(prefix="/posts", tags=["Posts"])


# create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    post: PostBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# read
@router.get("/", response_model=list[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
            headers={"X-Error": "No posts available"},
        )
    return posts


@router.get("/{id}", response_model=Post)
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
@router.put("/{id}", response_model=Post)
def update_post(
    id: int,
    updated_post: PostBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
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
