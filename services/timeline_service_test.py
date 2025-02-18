import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from ..models import Base, Post, User, UserConnection
from ..config import TEST_DATABASE_URL
from .timeline_service import TimelineService

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
def timeline_service(db_session):
  return TimelineService(db_session)

@pytest.fixture
def sample_data(db_session):
  # create 3 users
  user1 = User(id=1, name="John")
  user2 = User(id=2, name="Mark")
  user3 = User(id=3, name="Amy")
  db_session.add_all([user1, user2, user3])

  # make user1 follow user2 and user3
  connection1 = UserConnection(follower_id=1, following_id=2)
  connection2 = UserConnection(follower_id=1, following_id=3)
  db_session.add_all([connection1, connection2])

  now = datetime.now()
  posts = []
  # user1 has a scheduled post and a published post
  posts.append(Post(
    content="John's scheduled post",
    post_at=now + timedelta(days=1),
    user_id=1,
  ))
  posts.append(Post(
    content="John's published post",
    post_at=now - timedelta(days=1),
    user_id=1,
  ))
  # user2 has 2 published posts
  posts.append(Post(
    content="Mark's published post 1",
    post_at=now - timedelta(days=1),
    user_id=2,
  ))
  posts.append(Post(
    content="Mark's published post 2",
    post_at=now - timedelta(days=2),
    user_id=2,
  ))

  # # user3 has 1 published posts
  posts.append(Post(
    content="Amy's published post 1",
    post_at=now - timedelta(days=3),
    user_id=3,
  ))

  db_session.add_all(posts)
  db_session.commit()

def test_get_posts(timeline_service, sample_data, db_session):
    posts = timeline_service.get_posts(user_id=1)

    assert len(posts) == 4
    assert posts[0].content == "John's published post"
    assert posts[1].content == "Mark's published post 1"
    assert posts[2].content == "Mark's published post 2"
    assert posts[3].content == "Amy's published post 1"

def test_get_posts_pagination(timeline_service, sample_data, db_session):
    # Test with limit
    posts = timeline_service.get_posts(user_id=1, limit=2)
    assert len(posts) == 2
    assert posts[0].content == "John's published post"
    assert posts[1].content == "Mark's published post 1"

    # Test with offset
    posts = timeline_service.get_posts(user_id=1, limit=2, offset=1)
    assert len(posts) == 2
    assert posts[0].content == "Mark's published post 1"
    assert posts[1].content == "Mark's published post 2"

def test_get_posts_no_followers(timeline_service, sample_data, db_session):
    posts = timeline_service.get_posts(user_id=3)
    assert len(posts) == 1
    assert posts[0].content == "Amy's published post 1"
