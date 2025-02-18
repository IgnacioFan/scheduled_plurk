from fastapi import FastAPI, Body, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import get_db
import schemas
from auth import get_current_user_id
from services.post_service import PostService
from services.timeline_service import TimelineService

app = FastAPI()

@app.get("/api/v1/scheduled-posts", response_model=list[schemas.Post])
def get_scheduled_posts(
  db: Session = Depends(get_db),
  current_user_id: int = Depends(get_current_user_id)
):
  return PostService(db).get_scheduled_posts(current_user_id)

@app.post("/api/v1/scheduled-posts", response_model=schemas.Post)
def create_scheduled_post(
  db: Session = Depends(get_db),
  post: schemas.PostCreate = Body(...),
  current_user_id: int = Depends(get_current_user_id)
):
  return PostService(db).create_scheduled_post(post, current_user_id)

@app.patch("/api/v1/scheduled-posts/{id}", response_model=schemas.Post)
def edit_scheduled_post(
  db: Session = Depends(get_db),
  id: int = Path(...),
  post_update: schemas.PostUpdate = Body(...),
  current_user_id: int = Depends(get_current_user_id)
):
  post, error = PostService(db).edit_scheduled_post(id, current_user_id, post_update)
  if error:
    raise HTTPException(status_code=404, detail=error["error"])
  else:
    return post

@app.delete("/api/v1/scheduled-posts/{id}")
def delete_scheduled_post(
  db: Session = Depends(get_db),
  id: int = Path(...),
  current_user_id: int = Depends(get_current_user_id)
):
  res = PostService(db).delete_scheduled_post(id, current_user_id)
  if "error" in res:
    raise HTTPException(status_code=404, detail=res["error"])
  else:
    return res

@app.get("/api/v1/timeline")
def get_timeline(
  db: Session = Depends(get_db),
  current_user_id: int = Depends(get_current_user_id),
  limit: int = Query(default=50, ge=1, le=100),
  offset: int = Query(default=0, ge=0)
):
  return TimelineService(db).get_posts(current_user_id, limit=limit, offset=offset)
