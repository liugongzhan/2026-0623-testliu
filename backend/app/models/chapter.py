from sqlalchemy import Column, BigInteger, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Chapter(Base):
    __tablename__ = "chapter"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_id = Column(BigInteger, ForeignKey("course.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    parent_id = Column(BigInteger, ForeignKey("chapter.id", ondelete="SET NULL"), default=None)
    video_url = Column(String(500), default=None)
    duration = Column(Integer, default=0)
    is_free = Column(Boolean, nullable=False, default=False)

    # Relationships
    course = relationship("Course", back_populates="chapters")
    parent = relationship("Chapter", remote_side=[id], backref="children")
    learning_records = relationship("LearningRecord", back_populates="chapter")
    notes = relationship("Note", back_populates="chapter")
    qas = relationship("QA", back_populates="chapter")
