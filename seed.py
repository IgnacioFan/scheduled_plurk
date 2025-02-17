from sqlalchemy.orm import Session
from models import User
from database import SessionLocal

def seed_users(db: Session):
  seed_users = [
    {"name": "John Doe"},
    {"name": "Anne Smith"},
    {"name": "Mark Forsen"},
  ]
  try:
    for user in seed_users:
      db_user = User(name=user["name"])
      db.add(db_user)
    db.commit()
    print("Users seeded successfully")
  except Exception as e:
    db.rollback()
    print(f"Error seeding users: {e}")
  finally:
    db.close()

if __name__ == "__main__":
  seed_users(SessionLocal())

