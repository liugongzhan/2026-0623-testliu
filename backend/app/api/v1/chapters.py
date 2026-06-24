"""章节管理 API (占位 — 待完整实现)"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/courses/{course_id}/chapters")
def list_chapters(course_id: int):
    """获取课程的章节列表（树形结构）"""
    return {"message": f"课程 {course_id} 章节列表 API — 待实现", "items": []}


@router.post("/courses/{course_id}/chapters")
def create_chapter(course_id: int):
    """创建章节"""
    return {"message": f"为课程 {course_id} 创建章节 API — 待实现"}
