from sqlalchemy import text, Column, Integer, BigInteger, String, SmallInteger, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class SysUser(Base):
    __tablename__ = "sys_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(100), default=None)
    email = Column(String(100), unique=True, default=None)
    avatar = Column(String(500), default=None)
    role = Column(String(20), nullable=False, default="student", index=True)
    status = Column(SmallInteger, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    courses = relationship("Course", back_populates="teacher")
    learning_records = relationship("LearningRecord", back_populates="user")
    notes = relationship("Note", back_populates="user")
    exam_records = relationship("ExamRecord", back_populates="user")
