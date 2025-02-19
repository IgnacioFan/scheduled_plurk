# Scheduled Plurk

A FastAPI-based service that enables users to schedule and manage posts (plurks). Posts (Plurks) are automatically published at specified times and appear in the timelines of the plurk owners and their followers.

## Features

- Create scheduled posts (plurks)
- Retrieve scheduled posts (plurks)
- Edit or cancel scheduled posts before they go public
- Timeline view showing published posts (plurks) from author and author's followings

## Tech Stack

- Python 3.10.12
- FastAPI
- SQLAlchemy (PostgreSQL)
- pytest (for testing)

## Setup

1. Clone the repository

```bash
git clone https://github.com/IgnacioFan/scheduled_plurk.git
cd scheduled_plurk
```

2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and set the environment variables

```bash
# Database
DATABASE_URL="postgresql://username:password@localhost:5432/plurk"
TEST_DATABASE_URL="postgresql://username:password@localhost:5432/plurk_test"

# JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

5. Run migrations and start FastAPI server

```bash
alembic upgrade head
uvicorn main:app --reload
# local: http://127.0.0.1:8000
# live docs: http://127.0.0.1:8000/docs
```

## Run Tests

```bash
pytest
```

## API Endpoints

### Posts

#### Get Scheduled Posts

Query parameters:

- `limit` (default: 50)
- `offset` (default: 0)

```bash
GET api/v1/scheduled-posts?limit=10&offset=0
```

#### Create Scheduled Post

```bash
POST api/v1/scheduled-posts
```

```json
{
    "content": "Post content",
    "post_at": "2024-01-01T12:00:00Z"
}
```

#### Edit Scheduled Post

```bash
PATCH api/v1/scheduled-posts/{id}
```

```json
{
    "content": "Updated post content", # optional
    "post_at": "2024-01-01T12:00:00Z" # optional
}
```

#### Delete Scheduled Post

```bash
DELETE api/v1/scheduled-posts/{id}
```

### Timeline

#### Get Timeline Posts

Query parameters:

- `limit` (default: 50)
- `offset` (default: 0)

```bash
GET api/v1/timeline?limit=10&offset=0
```

## Data Models

### User

- `id`: Primary key
- `name`: Name of the user

### Post

- `id`: Primary key
- `content`: Content of the post
- `post_at`: Date and time when the post will be published
- `user_id`: Foreign key to the user who created the post

### UserConnection

- `id`: Primary key
- `follower_id`: Foreign key to the follower user
- `following_id`: Foreign key to the following user
- `status`: Status of the user connection (fan, friend)
