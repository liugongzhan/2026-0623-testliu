"""课程管理 API (占位 — 待完整实现)"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_courses():
    """获取课程列表"""
    return {"message": "课程列表 API — 待实现", "items": []}


@router.post("/")
def create_course():
    """创建课程"""
    return {"message": "创建课程 API — 待实现"}


@router.get("/{course_id}")
def get_course(course_id: int):
    """获取课程详情"""
    return {"message": f"课程 {course_id} 详情 API — 待实现"}
