from fastapi import FastAPI
from .database import engine
from . import models
from .routes import post, user, auth, vote

# Create the database tables
# models.Base.metadata.create_all(bind=engine)
# This used to create tables when the app starts, but it's commented out as we started using Alembic for migrations.

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Wecome to FastAPI"}
