"""文件上传 API"""
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse

from app.models.user import SysUser
from app.api.deps import require_role

router = APIRouter()

# 上传文件存储目录
UPLOAD_DIR = Path("uploads/videos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_UPLOAD_SIZE = 500 * 1024 * 1024  # 500MB


@router.post("/upload/video")
async def upload_video(
    file: UploadFile = File(...),
    current_user: SysUser = Depends(require_role("teacher", "admin")),
):
    """上传视频文件（教师/管理员）。"""
    # 验证文件类型
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="仅支持视频文件")

    # 生成唯一文件名
    ext = os.path.splitext(file.filename or "video.mp4")[1] or ".mp4"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = UPLOAD_DIR / filename

    # 分块写入文件
    file_size = 0
    with open(filepath, "wb") as f:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            file_size += len(chunk)
            if file_size > MAX_UPLOAD_SIZE:
                f.close()
                filepath.unlink(missing_ok=True)
                raise HTTPException(status_code=400, detail="文件超过 500MB 限制")
            f.write(chunk)

    # 返回可访问的 URL
    video_url = f"/static/videos/{filename}"

    return JSONResponse({
        "url": video_url,
        "filename": filename,
        "size": file_size,
    })
