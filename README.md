# 在线教育学习平台

前后端分离架构的在线教育平台，支持课程管理、视频学习、笔记、问答、考试等功能。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue3 + Vite + Element Plus + Axios + Pinia + video.js |
| 后端 | Python + FastAPI + SQLAlchemy + JWT |
| 数据库 | MySQL 8.4 |

## 项目结构

```
.
├── README.md
├── backend/
│   ├── .env                          # 环境变量（密钥、数据库 URL）
│   ├── .env.example                  # 环境变量模板
│   ├── requirements.txt              # Python 依赖
│   ├── sql/
│   │   └── init.sql                  # MySQL 8.4 建库建表脚本（9 张表）
│   └── app/
│       ├── __init__.py
│       ├── main.py                   # FastAPI 入口，CORS，路由挂载
│       ├── config.py                 # pydantic-settings 配置
│       ├── database.py               # SQLAlchemy engine / session / Base
│       ├── core/
│       │   ├── __init__.py
│       │   └── security.py           # JWT 创建/验证、bcrypt 密码哈希
│       ├── models/
│       │   ├── __init__.py           # 统一导入所有模型
│       │   ├── user.py               # sys_user — 用户表
│       │   ├── course.py             # course — 课程表
│       │   ├── chapter.py            # chapter — 章节表（自引用树形结构）
│       │   ├── learning_record.py    # learning_record — 学习记录
│       │   ├── note.py               # note — 学习笔记
│       │   ├── qa.py                 # qa — 课程问答
│       │   ├── question.py           # question — 题库
│       │   ├── exam.py               # exam — 考试
│       │   └── exam_record.py        # exam_record — 考试记录
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── user.py               # UserCreate / Login / Response / Token
│       │   ├── course.py             # CourseCreate / Update / Response
│       │   ├── chapter.py            # ChapterCreate / Update / Tree
│       │   ├── learning_record.py    # LearningRecord CRUD schemas
│       │   ├── note.py               # Note CRUD schemas
│       │   ├── qa.py                 # QA CRUD schemas
│       │   ├── question.py           # Question + StudentQuestion
│       │   ├── exam.py               # Exam + ExamSubmit
│       │   └── exam_record.py        # ExamRecordResponse
│       ├── api/
│       │   ├── __init__.py
│       │   ├── deps.py               # get_current_user / require_role 依赖
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── router.py         # 汇总所有 v1 子路由
│       │       ├── auth.py           # POST /register  /login  /login/json  GET /me
│       │       ├── users.py          # 用户 CRUD（admin 权限控制）
│       │       ├── courses.py        # 课程 API（占位）
│       │       ├── chapters.py       # 章节 API（占位）
│       │       ├── learning.py       # 学习记录 API（占位）
│       │       ├── notes.py          # 笔记 API（占位）
│       │       ├── qa.py             # 问答 API（占位）
│       │       ├── questions.py      # 题库 API（占位）
│       │       └── exams.py          # 考试 API（占位）
│       └── services/
│           ├── __init__.py
│           └── auth.py               # AuthService 业务逻辑层
└── frontend/
    ├── .env.development              # VITE_API_BASE_URL（开发环境）
    ├── .env.production               # VITE_API_BASE_URL（生产环境）
    ├── index.html                    # HTML 入口
    ├── package.json                  # npm 依赖与脚本
    ├── vite.config.js                # Vite 配置 + /api 代理
    └── src/
        ├── main.js                   # Vue 入口（Pinia → Router → ElementPlus）
        ├── App.vue                   # 根组件（AppHeader + router-view）
        ├── router/
        │   └── index.js              # 路由表 + 登录守卫
        ├── store/
        │   ├── index.js              # Pinia 实例
        │   └── modules/
        │       ├── user.js           # 用户状态（token/userInfo/login/logout）
        │       └── app.js            # 全局 UI 状态（侧栏/加载/面包屑）
        ├── api/
        │   ├── request.js            # Axios 实例 + JWT 拦截器 + 错误处理
        │   └── auth.js               # login / register / getMe
        ├── views/
        │   ├── Login.vue             # 登录页（表单校验）
        │   ├── Register.vue          # 注册页（确认密码）
        │   └── Home.vue              # 首页（Hero Banner + 统计数据）
        ├── components/
        │   ├── common/
        │   │   └── VideoPlayer.vue   # video.js 8.x Vue3 封装组件
        │   └── layout/
        │       └── AppHeader.vue     # 顶部导航栏（登录态切换）
        ├── utils/
        │   └── auth.js               # token 读写（localStorage）
        └── assets/
            └── styles/
                └── main.css          # 全局样式 + CSS 变量 + 滚动条美化
```

## 数据库表

| 表名 | 说明 |
|------|------|
| sys_user | 用户表（admin/teacher/student） |
| course | 课程表 |
| chapter | 章节表（支持二级嵌套） |
| learning_record | 学习记录表 |
| note | 笔记表 |
| qa | 问答表 |
| question | 题库表（单选/多选/判断/填空） |
| exam | 考试表 |
| exam_record | 考试记录表 |

## 快速开始

### 1. 初始化数据库

```bash
mysql -u root -p < backend/sql/init.sql
```

### 2. 启动后端

```bash
cd backend
python -m app.main
# 服务运行在 http://localhost:8090
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
# 服务运行在 http://localhost:5173
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

## API 接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/v1/auth/register | 用户注册 | 否 |
| POST | /api/v1/auth/login | 登录（OAuth2表单） | 否 |
| POST | /api/v1/auth/login/json | 登录（JSON） | 否 |
| GET | /api/v1/auth/me | 获取当前用户 | 是 |
| GET | /api/v1/users | 用户列表 | admin |
| GET | /api/v1/users/{id} | 用户详情 | 是 |
| PUT | /api/v1/users/me | 更新个人信息 | 是 |
| PUT | /api/v1/users/{id}/status | 修改用户状态 | admin |
