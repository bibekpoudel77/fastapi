from fastapi import FastAPI
from .routes import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables
# models.Base.metadata.create_all(bind=engine)
# This used to create tables when the app starts, but it's commented out as we started using Alembic for migrations.


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Wecome to FastAPI"}
