from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models import User, Post
from database import get_db
import schemas

app = FastAPI()

@app.get("/api/v1/users", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
  users = db.query(User).all()
  return users

@app.get("/api/v1/scheduled-posts", response_model=list[schemas.Post])
def get_scheduled_posts(db: Session = Depends(get_db)):
  posts = db.query(Post) \
    .filter(Post.post_at > datetime.now()) \
    .order_by(Post.post_at) \
    .all()
  return posts

@app.post("/api/v1/scheduled-posts", response_model=schemas.Post)
def create_scheduled_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
  db_post = Post(content=post.content, post_at=post.post_at, user_id=post.user_id)
  db.add(db_post)
  db.commit()
  db.refresh(db_post)
  return db_post

@app.patch("/api/v1/scheduled-posts/{id}", response_model=schemas.Post)
def edit_scheduled_post(id: int,post_update: schemas.PostUpdate, db: Session = Depends(get_db)):
  db_post = db.query(Post).filter(Post.id == id).first()
  if not db_post:
    raise HTTPException(status_code=404, detail="Post not found")

  update_data = post_update.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(db_post, key, value)

  db.commit()
  db.refresh(db_post)
  return db_post

@app.delete("/api/v1/scheduled-posts/{id}")
def delete_scheduled_post(id: int, db: Session = Depends(get_db)):
  db_post = db.query(Post).filter(Post.id == id).first()
  if not db_post:
    raise HTTPException(status_code=404, detail="Post not found")

  db.delete(db_post)
  db.commit()
  return {"message": "Scheduled post deleted successfully"}
