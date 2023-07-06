from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

LIMIT = int(os.getenv("LIMIT"))
OFFSET = int(os.getenv("OFFSET"))


class BlogParams(BaseModel):
    limit: int = LIMIT
    offset: int = OFFSET
    start: str = None
    end: str = None
    owner: str = None
    title: str = None
    sort: str = '-updated_at'


class PostParams(BaseModel):
    limit: int = LIMIT
    offset: int = OFFSET
    start: str = None
    end: str = None
    author: str = None
    title: str = None
    sort: str = '-created_at'
    tags: str = None


class BlogModel(BaseModel):
    title: str
    description: str


class PostModel(BaseModel):
    title: str
    body: str
    is_published: bool = False
    tags: str = None


class BlogUpdate(BaseModel):
    title: str = None
    description: str = None


class PostUpdate(BaseModel):
    title: str = None
    body: str = None
    is_published: bool = None
    tags: str = None
