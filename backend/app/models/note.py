from sqlalchemy import text, Column, BigInteger, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapter.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(Integer, default=None)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    user = relationship("SysUser", back_populates="notes")
    chapter = relationship("Chapter", back_populates="notes")
