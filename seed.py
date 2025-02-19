from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, UserConnection, Post
from datetime import datetime, timedelta

def seed_users(db: Session):
  seed_users = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Anne Smith"},
    {"id": 3, "name": "Mark Forsen"},
  ]
  seed_user_connections = [
    {"follower_id": 1, "following_id": 2}, # John follows Anne
    {"follower_id": 1, "following_id": 3}, # John follows Mark
    {"follower_id": 2, "following_id": 3}, # Anne follows Mark
  ]
  seed_posts = [
    {"content": "John's published post", "user_id": 1, "post_at": datetime.now() - timedelta(days=2)},
    {"content": "Mark's published post 1", "user_id": 3, "post_at": datetime.now() - timedelta(days=1)},
    {"content": "Mark's published post 2", "user_id": 3, "post_at": datetime.now()},
  ]
  try:
    for user in seed_users:
      db_user = User(name=user["name"])
      db.add(db_user)
    db.commit()
    print("Users seeded successfully")
    for connection in seed_user_connections:
      db_connection = UserConnection(follower_id=connection["follower_id"], following_id=connection["following_id"])
      db.add(db_connection)
    db.commit()
    print("UserConnections seeded successfully")
    for post in seed_posts:
      db_post = Post(content=post["content"], user_id=post["user_id"], post_at=post["post_at"])
      db.add(db_post)
    db.commit()
    print("Posts seeded successfully")
  except Exception as e:
    db.rollback()
    print(f"Error seeding users: {e}")
  finally:
    db.close()

if __name__ == "__main__":
  seed_users(SessionLocal())
