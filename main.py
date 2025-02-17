from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import User as UserSchema

app = FastAPI()

@app.get("/api/v1/users", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
  users = db.query(User).all()
  return users

@app.get("/api/v1/scheduled-posts")
def get_scheduled_posts():
  return "get scheduled posts"

@app.post("/api/v1/scheduled-posts")
def create_scheduled_post(payload: dict = Body(...)):
  return "create scheduled post"

@app.patch("/api/v1/scheduled-posts/{id}")
def edit_scheduled_post(id: int, payload: dict = Body(...)):
  return "edit scheduled post"

@app.delete("/api/v1/scheduled-posts/{id}")
def delete_scheduled_post(id: int):
  return "delete scheduled post"
