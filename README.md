# 在线教育学习平台

前后端分离架构的在线教育平台，支持课程管理、视频学习、笔记、问答、考试等功能。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue3 + Vite + Element Plus + Axios + Pinia + video.js 8.x |
| 后端 | Python 3.13 + FastAPI + SQLAlchemy 2.0 + JWT |
| 数据库 | MySQL 8.4 |

---

## 项目进度

### ✅ 已完成

| 模块 | 功能 | 状态 |
|------|------|------|
| **用户认证** | 注册、登录（OAuth2 + JSON）、JWT 令牌、角色权限（admin/teacher/student） | ✅ |
| **课程管理** | 课程列表（分页/搜索/分类）、课程详情、创建/编辑/删除（教师/admin） | ✅ |
| **章节管理** | 树形章节目录（二级嵌套）、CRUD、排序、视频绑定 | ✅ |
| **在线学习** | video.js 播放器、断点续播（自动保存/恢复）、倍速播放、章节切换 | ✅ |
| **学习进度** | 进度保存（每10秒）、课程进度概览、学习历史、章节完成标记 | ✅ |
| **学习笔记** | 添加（关联视频时间点）、列表、编辑、删除、点击时间点跳转 | ✅ |
| **视频上传** | 拖拽上传、进度条、500MB 限制 | ✅ |
| **数据库** | 9 张表全部建表脚本 + SQLAlchemy ORM 模型 | ✅ |

### ⬜ 待开发

| 模块 | 说明 |
|------|------|
| 问答系统 | 课程问答提问/回答 |
| 题库管理 | 单选/多选/判断/填空 CRUD |
| 在线考试 | 考试创建、限时答题、自动判分 |
| 个人中心 | 学习数据统计、个人资料编辑页 |
| 课程分类 | 分类管理 CRUD |
| 管理员面板 | 用户管理、数据统计 |

---

## 项目结构

```
.
├── README.md
├── DEBUG.md                              # 调试记录（所有错误及修复方案）
├── backend/                              # Python FastAPI 后端
│   ├── .env                              # 环境变量（密钥、数据库 URL）
│   ├── .env.example                      # 环境变量模板
│   ├── requirements.txt                  # Python 依赖
│   ├── sql/
│   │   └── init.sql                      # MySQL 8.4 建库建表脚本（9 张表）
│   └── app/
│       ├── __init__.py
│       ├── main.py                       # FastAPI 入口（CORS、静态文件、路由）
│       ├── config.py                     # pydantic-settings 配置
│       ├── database.py                   # SQLAlchemy engine / session / Base
│       ├── core/
│       │   ├── __init__.py
│       │   └── security.py               # JWT 创建/验证、bcrypt 密码哈希
│       ├── models/                       # SQLAlchemy ORM 模型
│       │   ├── __init__.py               # 统一导出所有模型
│       │   ├── user.py                   # sys_user
│       │   ├── course.py                 # course
│       │   ├── chapter.py                # chapter（自引用树形结构）
│       │   ├── learning_record.py        # learning_record
│       │   ├── note.py                   # note
│       │   ├── qa.py                     # qa
│       │   ├── question.py               # question
│       │   ├── exam.py                   # exam
│       │   └── exam_record.py            # exam_record
│       ├── schemas/                      # Pydantic 请求/响应模型
│       │   ├── __init__.py
│       │   ├── user.py                   # UserCreate / Login / Response / Token
│       │   ├── course.py                 # CourseCreate / Update / Response / List
│       │   ├── chapter.py                # ChapterCreate / Update / Tree / Response
│       │   ├── learning_record.py        # Progress / History / ChapterProgress
│       │   ├── note.py                   # NoteCreate / Update / Response
│       │   ├── qa.py                     # QACreate / Update / Response
│       │   ├── question.py               # Question + StudentQuestion
│       │   ├── exam.py                   # Exam + ExamSubmit
│       │   └── exam_record.py            # ExamRecordResponse
│       ├── api/                          # API 路由层
│       │   ├── __init__.py
│       │   ├── deps.py                   # get_current_user / require_role 依赖
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── router.py             # 汇总所有 v1 子路由
│       │       ├── auth.py               # 认证 API（注册/登录/获取当前用户）
│       │       ├── users.py              # 用户管理 API（CRUD + 状态）
│       │       ├── courses.py            # 课程 API（分页/搜索/分类/CRUD）
│       │       ├── chapters.py           # 章节 API（树形 CRUD + 排序）
│       │       ├── learning.py           # 学习进度 API（保存/概览/历史/完成）
│       │       ├── notes.py              # 笔记 API（CRUD + 时间点关联）
│       │       ├── upload.py             # 视频上传 API
│       │       ├── qa.py                 # 问答 API（占位）
│       │       ├── questions.py          # 题库 API（占位）
│       │       └── exams.py              # 考试 API（占位）
│       └── services/                     # 业务逻辑层
│           ├── __init__.py
│           ├── auth.py                   # AuthService（注册/认证）
│           └── course.py                 # CourseService（课程 CRUD + 权限）
└── frontend/                             # Vue3 + Vite 前端
    ├── .env.development                  # 开发环境变量
    ├── .env.production                   # 生产环境变量
    ├── index.html                        # HTML 入口
    ├── package.json                      # npm 依赖与脚本
    ├── vite.config.js                    # Vite 配置 + /api → 8090 代理
    └── src/
        ├── main.js                       # Vue 入口（Pinia → Router → ElementPlus）
        ├── App.vue                       # 根组件
        ├── router/
        │   └── index.js                  # 路由表 + 登录/角色守卫
        ├── store/
        │   ├── index.js                  # Pinia 实例
        │   └── modules/
        │       ├── user.js               # 用户状态（token / userInfo / login / logout）
        │       └── app.js                # 全局 UI 状态
        ├── api/                          # Axios API 封装
        │   ├── request.js                # Axios 实例 + JWT 拦截器 + 错误处理
        │   ├── auth.js                   # 认证 API（login / register / getMe）
        │   ├── course.js                 # 课程 + 章节 API
        │   └── learning.js               # 学习进度 + 笔记 API
        ├── views/                        # 页面组件
        │   ├── Home.vue                  # 首页（Hero + 最新课程）
        │   ├── Login.vue                 # 登录页（表单校验）
        │   ├── Register.vue              # 注册页（确认密码）
        │   ├── CourseList.vue            # 课程列表（卡片网格/搜索/分类/分页）
        │   ├── CourseDetail.vue          # 课程详情（信息 + 章节目录）
        │   ├── CourseManage.vue          # 课程管理（表格 + 创建/编辑 + 章节管理弹窗）
        │   ├── VideoLearn.vue            # [旧] 视频学习页（已被 Player.vue 替代）
        │   └── course/
        │       └── Player.vue            # 视频播放页（断点续播/倍速/笔记/进度）
        ├── components/
        │   ├── common/
        │   │   ├── VideoPlayer.vue       # video.js 8.x Vue3 封装组件
        │   │   └── VideoUpload.vue       # 视频上传组件（拖拽/进度条/URL复制）
        │   ├── layout/
        │   │   └── AppHeader.vue         # 顶部导航栏（登录态切换/角色菜单）
        │   └── Learning/
        │       ├── ProgressBar.vue       # 学习进度（总进度 + 章节状态）
        │       └── NotePanel.vue         # 笔记面板（添加/列表/时间点跳转）
        ├── utils/
        │   └── auth.js                   # token 读写（localStorage）
        └── assets/
            └── styles/
                └── main.css              # 全局样式 + CSS 变量 + 滚动条美化
```

---

## 数据库表

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| `sys_user` | 用户表 | role (admin/teacher/student), status |
| `course` | 课程表 | teacher_id FK, status (draft/published/archived) |
| `chapter` | 章节表 | parent_id 自引用, is_free, video_url, duration |
| `learning_record` | 学习记录 | user_id+chapter_id 唯一, progress, last_position |
| `note` | 笔记表 | user_id+chapter_id, timestamp (视频时间点) |
| `qa` | 问答表 | user_id+chapter_id, question, answer |
| `question` | 题库表 | type (single/multi/judge/fill), options JSON |
| `exam` | 考试表 | duration, total_score, passing_score, start/end_time |
| `exam_record` | 考试记录 | exam_id+user_id 唯一, score, answers JSON |

---

## 快速开始

### 1. 初始化数据库

```bash
mysql -u root -p < backend/sql/init.sql
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python -m app.main
# 服务运行在 http://localhost:8090
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
# 服务运行在 http://localhost:5173
# 前端通过 Vite proxy 将 /api 请求转发到后端 :8090
```

### 4. 验证

```bash
# 健康检查
curl http://localhost:8090/

# 注册用户
curl -X POST http://localhost:8090/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'

# 登录
curl -X POST http://localhost:8090/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'
```

### 5. 创建讲师账户（用于创建课程）

```bash
# 先注册，再通过数据库直接改 role
mysql -u root -p edu_platform -e "UPDATE sys_user SET role='teacher' WHERE username='test';"
```

---

## API 接口

### 认证（Auth）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `POST` | `/api/v1/auth/register` | 用户注册 | 否 |
| `POST` | `/api/v1/auth/login` | 登录（OAuth2 表单） | 否 |
| `POST` | `/api/v1/auth/login/json` | 登录（JSON） | 否 |
| `GET` | `/api/v1/auth/me` | 获取当前用户信息 | Bearer Token |

### 用户管理（Users）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `GET` | `/api/v1/users` | 用户列表（分页） | admin |
| `GET` | `/api/v1/users/{id}` | 用户详情 | 登录 |
| `PUT` | `/api/v1/users/me` | 更新个人信息 | 登录 |
| `PUT` | `/api/v1/users/{id}/status` | 修改用户状态 | admin |

### 课程管理（Courses）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `GET` | `/api/v1/courses` | 课程列表（分页/搜索/分类/状态过滤） | 否 |
| `GET` | `/api/v1/courses/my` | 我的课程 | teacher/admin |
| `POST` | `/api/v1/courses` | 创建课程 | teacher/admin |
| `GET` | `/api/v1/courses/{id}` | 课程详情 | 否 |
| `PUT` | `/api/v1/courses/{id}` | 更新课程 | 讲师本人/admin |
| `DELETE` | `/api/v1/courses/{id}` | 删除课程 | 讲师本人/admin |

### 章节管理（Chapters）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `GET` | `/api/v1/courses/{id}/chapters` | 章节列表（树形结构） | 否 |
| `POST` | `/api/v1/courses/{id}/chapters` | 创建章节（支持 parent_id） | teacher/admin |
| `PUT` | `/api/v1/chapters/{id}` | 更新章节 | teacher/admin |
| `DELETE` | `/api/v1/chapters/{id}` | 删除章节（级联删除子节） | teacher/admin |
| `PUT` | `/api/v1/chapters/{id}/sort` | 调整排序 | teacher/admin |

### 学习进度（Learning）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `POST` | `/api/v1/learning/progress` | 保存进度 (course_id, chapter_id, position, progress) | 登录 |
| `GET` | `/api/v1/learning/progress/{courseId}` | 课程进度概览（各章节状态） | 登录 |
| `GET` | `/api/v1/learning/history` | 学习历史列表 | 登录 |
| `POST` | `/api/v1/learning/complete/{chapterId}` | 标记章节完成 | 登录 |

### 笔记（Notes）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `GET` | `/api/v1/chapters/{chapterId}/notes` | 笔记列表（按时间点排序） | 登录 |
| `POST` | `/api/v1/chapters/{chapterId}/notes` | 创建笔记（关联 timestamp） | 登录 |
| `PUT` | `/api/v1/notes/{id}` | 编辑笔记 | 登录 |
| `DELETE` | `/api/v1/notes/{id}` | 删除笔记 | 登录 |

### 文件上传（Upload）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `POST` | `/api/v1/upload/video` | 上传视频（≤500MB） | teacher/admin |

---

## 前端路由

| 路径 | 页面 | 权限 |
|------|------|------|
| `/` | 首页 | 公开 |
| `/login` | 登录 | 游客 |
| `/register` | 注册 | 游客 |
| `/courses` | 课程列表 | 公开 |
| `/courses/:id` | 课程详情 | 公开 |
| `/courses/:id/learn/:chapterId` | 视频学习 | 登录 |
| `/manage/courses` | 课程管理 | teacher/admin |

---

## 调试记录

详见 [DEBUG.md](DEBUG.md)，记录了开发过程中遇到的所有错误、原因分析和修复方案（共 9 个错误）。

---

## 架构特点

- **服务层分离** — API 路由薄层 + Service 业务逻辑层，便于测试
- **JWT 无状态认证** — python-jose + passlib(bcrypt)，OAuth2 标准兼容
- **跨数据库兼容** — SQLAlchemy `text()` 包装 + `Integer` PK，MySQL/SQLite 均能运行
- **自动保存进度** — 播放时每 10 秒自动保存，离开页面强制保存
- **断点续播** — 进入章节自动跳转到上次播放位置
- **树形章节** — `parent_id` 自引用，支持无限级嵌套
- **Vite 代理** — 开发环境 `/api` 代理到后端，无 CORS 困扰
- **角色路由守卫** — 前端路由级权限控制，后端 API 双重校验
