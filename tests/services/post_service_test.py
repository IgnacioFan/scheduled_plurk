import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from schemas import PostCreate, PostUpdate
from models import Base, Post, User
from config import TEST_DATABASE_URL
from services.post_service import PostService
from datetime import datetime, timedelta
# Setup test database
engine = create_engine(TEST_DATABASE_URL)
if not database_exists(TEST_DATABASE_URL):
    create_database(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
  Base.metadata.create_all(bind=engine)
  session = TestingSessionLocal()
  try:
    yield session
  finally:
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def post_service(db_session):
  return PostService(db_session)

@pytest.fixture
def sample_user(db_session):
  user = User(id=1, name="John")
  db_session.add(user)
  db_session.commit()
  return user

@pytest.fixture
def sample_posts(db_session, sample_user):
  now = datetime.now()
  posts = [
    Post(
        id=1,
        content="John's published post",
        user_id=sample_user.id,
        post_at=now - timedelta(days=1),
    ),
    Post(
        id=2,
        content="John's lastest scheduled post",
        user_id=sample_user.id,
        post_at=now + timedelta(days=2),
    ),
    Post(
        id=3,
        content="John's recent scheduled post",
        user_id=sample_user.id,
        post_at=now + timedelta(days=1),
    )
  ]
  db_session.add_all(posts)
  db_session.commit()
  return posts

# Error messages
NOT_FOUND_ERROR = {"error": "Post not found"}

def test_get_scheduled_posts(post_service, sample_posts, sample_user):
  posts = post_service.get_scheduled_posts(sample_user.id)
  print(posts)
  assert len(posts) == 2
  assert posts[0].content == "John's lastest scheduled post"
  assert posts[1].content == "John's recent scheduled post"

def test_get_posts_pagination(post_service, sample_posts, sample_user):
  posts = post_service.get_scheduled_posts(sample_user.id, limit=1, offset=1)
  assert len(posts) == 1
  assert posts[0].content == "John's recent scheduled post"

def test_create_scheduled_post(post_service, sample_user):
  data = PostCreate(
    content="Test test",
    post_at=datetime.now() + timedelta(days=1)
  )
  new_post = post_service.create_scheduled_post(data, sample_user.id)
  assert new_post.content == "Test test"
  assert new_post.user_id == sample_user.id

def test_edit_scheduled_post(post_service, sample_posts, sample_user):
  data = PostUpdate(content="Updated test")
  updated_post, error = post_service.edit_scheduled_post(2, sample_user.id, data)
  assert error is None
  assert updated_post.id == 2
  assert updated_post.content == "Updated test"

def test_edit_non_scheduled_post(post_service, sample_posts, sample_user):
  data = PostUpdate(content="Updated test")
  updated_post, error = post_service.edit_scheduled_post(1, sample_user.id, data)
  assert updated_post is None
  assert error == NOT_FOUND_ERROR

def test_edit_nonexistent_post(post_service, sample_user, db_session):
  data = PostUpdate(content="Updated test")
  updated_post, error = post_service.edit_scheduled_post(999, sample_user.id, data)
  assert updated_post is None
  assert error == NOT_FOUND_ERROR

def test_edit_other_users_post(post_service, sample_posts):
  data = PostUpdate(content="Updated test")
  updated_post, error = post_service.edit_scheduled_post(1, 3, data)
  assert updated_post is None
  assert error == NOT_FOUND_ERROR

def test_delete_scheduled_post(post_service, sample_posts, sample_user, db_session):
  res = post_service.delete_scheduled_post(2, sample_user.id)
  deleted_post = db_session.query(Post).filter(Post.id == 2).first()
  assert res == {"message": "Scheduled post deleted successfully"}
  assert deleted_post is None

def test_delete_published_post(post_service, sample_posts, sample_user, db_session):
  res = post_service.delete_scheduled_post(1, sample_user.id)
  deleted_post = db_session.query(Post).filter(Post.id == 1).first()
  assert res == NOT_FOUND_ERROR
  assert deleted_post is not None

def test_delete_nonexistent_post(post_service, sample_user, db_session):
  res = post_service.delete_scheduled_post(999, sample_user.id)
  assert res == NOT_FOUND_ERROR

def test_delete_other_users_post(post_service, sample_posts, db_session):
  res = post_service.delete_scheduled_post(1, 3)
  deleted_post = db_session.query(Post).filter(Post.id == 1).first()
  assert res == NOT_FOUND_ERROR
  assert deleted_post is not None
