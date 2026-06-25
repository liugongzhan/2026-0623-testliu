from sqlalchemy import text, Column, Integer, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class LearningRecord(Base):
    __tablename__ = "learning_record"
    __table_args__ = (
        UniqueConstraint("user_id", "chapter_id", name="uk_user_chapter"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapter.id", ondelete="CASCADE"), nullable=False)
    progress = Column(Float, nullable=False, default=0)
    last_position = Column(Float, nullable=False, default=0)
    completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    user = relationship("SysUser", back_populates="learning_records")
    course = relationship("Course")
    chapter = relationship("Chapter", back_populates="learning_records")
