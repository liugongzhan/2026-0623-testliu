"""笔记管理 API (占位 — 待完整实现)"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/chapters/{chapter_id}/notes")
def list_notes(chapter_id: int):
    """获取某章节下的笔记"""
    return {"message": f"章节 {chapter_id} 笔记列表 API — 待实现", "items": []}


@router.post("/chapters/{chapter_id}/notes")
def create_note(chapter_id: int):
    """创建笔记"""
    return {"message": f"为章节 {chapter_id} 创建笔记 API — 待实现"}
