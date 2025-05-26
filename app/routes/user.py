from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from .. import models, utils
from sqlalchemy.orm import Session
from ..schemas import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


# Users CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Users READ
@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if users is None or len(users) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
            headers={"X-Error": "No users available"},
        )
    return users


@router.get("/{id}", response_model=UserOut)
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
@router.put("/{id}", response_model=UserOut)
def update_user(id: int, updated_user: UserIn, db: Session = Depends(get_db)):
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
