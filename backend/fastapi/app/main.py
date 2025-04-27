import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from .controllers import post, user
from .utils.middleware import LimitUploadSize
from .db.postgres import engine, Base
from fastapi.middleware.cors import CORSMiddleware


# Create tables at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LimitUploadSize, max_upload_size=50_000)

# Routers
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(post.router, prefix="/post", tags=["post"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
