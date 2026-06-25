from sqlalchemy import Column, Integer, DECIMAL, JSON, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class ExamRecord(Base):
    __tablename__ = "exam_record"
    __table_args__ = (
        UniqueConstraint("exam_id", "user_id", name="uk_exam_user"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exam.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(DECIMAL(5, 1), default=None)
    answers = Column(JSON, default=None)
    start_time = Column(DateTime, nullable=False)
    submit_time = Column(DateTime, default=None)

    # Relationships
    exam = relationship("Exam", back_populates="exam_records")
    user = relationship("SysUser", back_populates="exam_records")
