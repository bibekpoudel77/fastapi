from fastapi import FastAPI
from .database import engine
from . import models
from .routes import post, user

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Wecome to FastAPI"}
