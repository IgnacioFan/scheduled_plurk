from fastapi import FastAPI, Body

app = FastAPI()

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
