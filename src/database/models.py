from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from .gen_uuid import gen_uuid

from .base import Base


class Theme(Base):
  __tablename__ = "themes"

  id = Column(String, primary_key=True, default=gen_uuid)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  name = Column(String)


class Question(Base):
  __tablename__ = "questions"

  id = Column(String, primary_key=True, default=gen_uuid)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  themeId = Column(ForeignKey("themes.id", ondelete="CASCADE"))
  question = Column(String)
  answer = Column(String)
  hasCode = Column(Boolean)
