from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.courses import router as courses_router
from app.api.v1.chapters import router as chapters_router
from app.api.v1.learning import router as learning_router
from app.api.v1.notes import router as notes_router
from app.api.v1.qa import router as qa_router
from app.api.v1.questions import router as questions_router
from app.api.v1.exams import router as exams_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(users_router, prefix="/users", tags=["用户管理"])
api_router.include_router(courses_router, prefix="/courses", tags=["课程管理"])
api_router.include_router(chapters_router, prefix="", tags=["章节管理"])
api_router.include_router(learning_router, prefix="/learning", tags=["学习记录"])
api_router.include_router(notes_router, prefix="", tags=["笔记管理"])
api_router.include_router(qa_router, prefix="", tags=["问答管理"])
api_router.include_router(questions_router, prefix="", tags=["题库管理"])
api_router.include_router(exams_router, prefix="", tags=["考试管理"])
