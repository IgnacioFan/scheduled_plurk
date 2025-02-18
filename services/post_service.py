from sqlalchemy.orm import Session
from models import Post
from datetime import datetime
from schemas import PostCreate, PostUpdate
from typing import Union, Dict

class PostService:
  def __init__(self, db: Session):
    self.db = db

  def get_scheduled_posts(self, user_id: int) -> list[Post]:
    return self.db.query(Post) \
      .filter(
        Post.user_id == user_id,
        Post.post_at > datetime.now()
      ) \
      .order_by(Post.post_at) \
      .all()

  def create_scheduled_post(self, post: PostCreate, user_id: int) -> Post:
    db_post = Post(content=post.content, post_at=post.post_at, user_id=user_id)
    self.db.add(db_post)
    self.db.commit()
    self.db.refresh(db_post)
    return db_post

  def edit_scheduled_post(self, post_id: int, user_id: int, post: PostUpdate) -> tuple[Post, Dict[str, str]]:
    db_post = self.db.query(Post) \
      .filter(
        Post.id == post_id,
        Post.user_id == user_id
      ) \
      .first()
    if not db_post:
      return None, {"error": "Post not found"}

    update_data = post.model_dump(exclude_unset=True)
    for key, value in update_data.items():
      setattr(db_post, key, value)

    self.db.commit()
    self.db.refresh(db_post)
    return db_post, None

  def delete_scheduled_post(self, post_id: int, user_id: int) -> Dict[str, str]:
    db_post = self.db.query(Post) \
      .filter(
        Post.id == post_id,
        Post.user_id == user_id
      ) \
      .first()
    if not db_post:
      return {"error": "Post not found"}

    self.db.delete(db_post)
    self.db.commit()
    return {"message": "Scheduled post deleted successfully"}
