from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from .. import models, oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..schemas import PostBase, Post, PostOut, TokenData

router = APIRouter(prefix="/posts", tags=["Posts"])


# create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    post: PostBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# read
@router.get("/", response_model=list[PostOut])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)  # Use outerjoin
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
            headers={"X-Error": "No posts available"},
        )
    return posts


@router.get("/{id}", response_model=PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)  # Use outerjoin
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
            headers={"X-Error": "Post not found"},
        )

    if post.Post.owner_id is not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this post",
            headers={"X-Error": "Permission denied"},
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

    if post.owner_id is not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this post",
            headers={"X-Error": "Permission denied"},
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
    post = query.first()

    # Check if the post exists
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
            headers={"X-Error": "Post not found"},
        )

    if post.owner_id is not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post",
            headers={"X-Error": "Permission denied"},
        )
    query.delete()
    db.commit()
    return {"message": "Post deleted successfully"}
