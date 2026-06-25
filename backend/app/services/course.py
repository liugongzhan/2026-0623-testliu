"""课程管理业务逻辑"""
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.models.course import Course
from app.models.chapter import Chapter
from app.models.user import SysUser
from app.schemas.course import CourseCreate, CourseUpdate


class CourseService:

    @staticmethod
    def list_courses(
        db: Session,
        page: int = 1,
        page_size: int = 12,
        keyword: Optional[str] = None,
        category_id: Optional[int] = None,
        status: Optional[str] = "published",
        teacher_id: Optional[int] = None,
    ):
        """分页查询课程列表"""
        query = db.query(Course)

        # 公开列表只看已发布课程
        if status:
            query = query.filter(Course.status == status)

        if keyword:
            query = query.filter(Course.title.contains(keyword))
        if category_id:
            query = query.filter(Course.category_id == category_id)
        if teacher_id:
            query = query.filter(Course.teacher_id == teacher_id)

        total = query.count()
        items = (
            query.options(joinedload(Course.teacher))
            .order_by(Course.updated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return {"total": total, "items": items}

    @staticmethod
    def get_course(db: Session, course_id: int) -> Course:
        course = (
            db.query(Course)
            .options(joinedload(Course.teacher), joinedload(Course.chapters))
            .filter(Course.id == course_id)
            .first()
        )
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="课程不存在")
        return course

    @staticmethod
    def create_course(db: Session, data: CourseCreate, teacher_id: int) -> Course:
        course = Course(
            title=data.title,
            description=data.description,
            cover_image=data.cover_image,
            category_id=data.category_id,
            teacher_id=teacher_id,
            price=data.price,
            status=data.status,
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def update_course(db: Session, course_id: int, data: CourseUpdate, current_user: SysUser) -> Course:
        course = CourseService.get_course(db, course_id)

        # 权限：仅教师本人或管理员
        if current_user.role != "admin" and course.teacher_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权修改此课程")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)

        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete_course(db: Session, course_id: int, current_user: SysUser) -> None:
        course = CourseService.get_course(db, course_id)

        if current_user.role != "admin" and course.teacher_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权删除此课程")

        db.delete(course)
        db.commit()
