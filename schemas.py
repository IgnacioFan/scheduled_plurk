from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
  content: str
  post_at: datetime

class PostCreate(PostBase):
  pass

class PostUpdate(PostBase):
  content: Optional[str] = None
  post_at: Optional[datetime] = None

class Post(PostBase):
  pass

class User(BaseModel):
  id: int
  name: str

  class Config:
    from_attributes = True

class TimelinePost(BaseModel):
  id: int
  content: str
  post_at: datetime
  user: User

  class Config:
    from_attributes = True
