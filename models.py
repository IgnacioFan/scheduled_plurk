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

class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True)
  content = Column(Text, nullable=False)
  post_at = Column(DateTime, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  created_at = Column(DateTime, nullable=False, default=func.now())
  updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

  user = relationship("User", back_populates="posts")
