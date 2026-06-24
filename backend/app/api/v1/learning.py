"""学习记录 API (占位 — 待完整实现)"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/record")
def save_learning_record():
    """保存/更新学习进度"""
    return {"message": "保存学习进度 API — 待实现"}


@router.get("/progress/{course_id}")
def get_learning_progress(course_id: int):
    """获取用户在某课程中的学习进度"""
    return {"message": f"课程 {course_id} 学习进度 API — 待实现"}
