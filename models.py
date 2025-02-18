from sqlalchemy import Column, Integer, String, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String(255), nullable=False)
  created_at = Column(DateTime, nullable=False, default=func.now())
  updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

  posts = relationship("Post", back_populates="user")
  followers = relationship("UserConnection", foreign_keys="UserConnection.following_id", back_populates="following")
  followings = relationship("UserConnection", foreign_keys="UserConnection.follower_id", back_populates="follower")

class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True)
  content = Column(Text, nullable=False)
  post_at = Column(DateTime, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  created_at = Column(DateTime, nullable=False, default=func.now())
  updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

  user = relationship("User", back_populates="posts")

class UserConnection(Base):
  __tablename__ = 'user_connections'

  id = Column(Integer, primary_key=True)
  follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  following_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  status = Column(String(20), nullable=False, default='fan') # fan, friend
  created_at = Column(DateTime, nullable=False, default=func.now())
  updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

  follower = relationship("User", foreign_keys=[follower_id], back_populates="followings")
  following = relationship("User", foreign_keys=[following_id], back_populates="followers")
