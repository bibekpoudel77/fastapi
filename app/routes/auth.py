from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import Token
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from .. import utils, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    user_credentail: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == user_credentail.username).first()
    exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
    )
    if not user:
        raise exception

    if not utils.verify_password(user_credentail.password, user.password):
        raise exception

    return Token(
        access_token=oauth2.create_access_token(data={"user_id": user.id}),
        token_type="bearer",
    )
