"""笔记管理 API"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.note import Note
from app.models.user import SysUser
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/chapters/{chapter_id}/notes", response_model=List[NoteResponse])
def list_notes(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """获取当前用户在某章节下的所有笔记（按时间点排序）。"""
    notes = (
        db.query(Note)
        .filter(
            Note.user_id == current_user.id,
            Note.chapter_id == chapter_id,
        )
        .order_by(Note.timestamp)
        .all()
    )
    return notes


@router.post("/chapters/{chapter_id}/notes", response_model=NoteResponse, status_code=201)
def create_note(
    chapter_id: int,
    data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """添加笔记（关联视频时间点）。"""
    note = Note(
        user_id=current_user.id,
        chapter_id=chapter_id,
        content=data.content,
        timestamp=data.timestamp,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """编辑笔记。"""
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    if data.content is not None:
        note.content = data.content
    if data.timestamp is not None:
        note.timestamp = data.timestamp
    db.commit()
    db.refresh(note)
    return note


@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(get_current_active_user),
):
    """删除笔记。"""
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    db.delete(note)
    db.commit()
    return {"message": "笔记已删除"}
