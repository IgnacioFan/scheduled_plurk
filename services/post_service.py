from sqlalchemy.orm import Session
from typing import Dict
from ..models import Post
from ..schemas import PostCreate, PostUpdate

NOT_FOUND_ERROR = {"error": "Post not found"}

class PostService:
  def __init__(self, db: Session):
    self.db = db

  def get_scheduled_posts(self, user_id: int, limit: int = 50, offset: int = 0) -> list[Post]:
    return self.db.query(Post) \
      .filter(
        Post.user_id == user_id,
        Post.is_scheduled(Post.post_at)
      ) \
      .order_by(Post.post_at.desc()) \
      .limit(limit) \
      .offset(offset) \
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
        Post.user_id == user_id,
        Post.is_scheduled(Post.post_at)
      ) \
      .first()
    if not db_post:
      return None, NOT_FOUND_ERROR

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
        Post.user_id == user_id,
        Post.is_scheduled(Post.post_at)
      ) \
      .first()
    if not db_post:
      return NOT_FOUND_ERROR

    self.db.delete(db_post)
    self.db.commit()
    return {"message": "Scheduled post deleted successfully"}
