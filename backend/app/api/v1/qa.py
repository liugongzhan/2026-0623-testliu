"""问答管理 API (占位 — 待完整实现)"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/chapters/{chapter_id}/qa")
def list_qa(chapter_id: int):
    """获取某章节的问答列表"""
    return {"message": f"章节 {chapter_id} 问答列表 API — 待实现", "items": []}


@router.post("/chapters/{chapter_id}/qa")
def create_qa_question(chapter_id: int):
    """提问"""
    return {"message": f"在章节 {chapter_id} 提问 API — 待实现"}
