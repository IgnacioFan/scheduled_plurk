
from sqlalchemy import select, union, literal
from sqlalchemy.orm import Session
from models import Post, UserConnection

class TimelineService:
  def __init__(self, db: Session):
    self.db = db

  def get_posts(self, user_id: int, limit: int = 50, offset: int = 0) -> list[Post]:
    following_ids_subquery = union(
      select(UserConnection.following_id).where(UserConnection.follower_id == user_id),
      select(literal(user_id))
    ).scalar_subquery()

    return self.db.query(Post)\
        .filter(
            Post.user_id.in_(following_ids_subquery),
            Post.is_published(Post.post_at)
        )\
        .order_by(Post.post_at.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()
