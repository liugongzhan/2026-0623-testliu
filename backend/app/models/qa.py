from sqlalchemy import text, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class QA(Base):
    __tablename__ = "qa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id", ondelete="CASCADE"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, default=None)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    user = relationship("SysUser")
    chapter = relationship("Chapter", back_populates="qas")
