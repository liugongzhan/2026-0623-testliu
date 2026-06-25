from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title="在线教育平台 API",
    description="在线教育学习平台后端接口",
    version="1.0.0",
)

# CORS middleware
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded content
import os
uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=uploads_dir), name="static")

# Include API v1 router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "ok", "message": "在线教育平台 API 运行中"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8090, reload=True)
