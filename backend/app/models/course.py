from sqlalchemy import Column, BigInteger, String, Text, Integer, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "course"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, default=None)
    cover_image = Column(String(500), default=None)
    category_id = Column(BigInteger, default=None)
    teacher_id = Column(BigInteger, ForeignKey("sys_user.id", ondelete="RESTRICT"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    status = Column(String(20), nullable=False, default="draft", index=True)
    student_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    # Relationships
    teacher = relationship("SysUser", back_populates="courses")
    chapters = relationship("Chapter", back_populates="course")
    questions = relationship("Question", back_populates="course")
    exams = relationship("Exam", back_populates="course")
