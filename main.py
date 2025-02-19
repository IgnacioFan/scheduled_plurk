from fastapi import FastAPI, Depends, HTTPException, Query, Body, Path
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user_id
from services.post_service import PostService
from services.timeline_service import TimelineService
from schemas import Post, PostCreate, PostUpdate

app = FastAPI()

@app.get("/api/v1/scheduled-posts", response_model=list[Post])
def get_scheduled_posts(
  db: Session = Depends(get_db),
  current_user_id: int = Depends(get_current_user_id),
  limit: int = Query(default=50, ge=1, le=100),
  offset: int = Query(default=0, ge=0)
):
  return PostService(db).get_scheduled_posts(current_user_id, limit=limit, offset=offset)

@app.post("/api/v1/scheduled-posts", status_code=201, response_model=Post)
def create_scheduled_post(
  db: Session = Depends(get_db),
  post: PostCreate = Body(...),
  current_user_id: int = Depends(get_current_user_id)
):
  return PostService(db).create_scheduled_post(post, current_user_id)

@app.patch("/api/v1/scheduled-posts/{id}", response_model=Post)
def edit_scheduled_post(
  db: Session = Depends(get_db),
  id: int = Path(...),
  post_update: PostUpdate = Body(...),
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
