# 调试记录

本文档记录在开发过程中发现的所有错误及其修复方案。

---

## 错误 1：ChapterTreeResponse 前向声明导致 NameError

**错误信息：**
```
NameError: name 'ChapterTreeResponse' is not defined. Did you mean: 'ChapterResponse'?
```

**出现位置：** [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py#L48)

**原因：** `ChapterTreeResponse` 类的 `children` 字段自引用 `List[ChapterTreeResponse]`，但类定义尚未完成，Python 无法解析该名称。

**修复方案：** 在文件顶部添加 `from __future__ import annotations`，将所有注解转为延迟求值的字符串形式。

**修改文件：**
- `backend/app/schemas/chapter.py` — 第1行添加 `from __future__ import annotations`

---

## 错误 2：路由函数名冲突

**错误表现：** FastAPI 生成 OpenAPI 文档时，多个路由的操作 ID (operation_id) 冲突。

**出现位置：**
- [backend/app/api/v1/qa.py](backend/app/api/v1/qa.py#L14) — `def create_question()`
- [backend/app/api/v1/questions.py](backend/app/api/v1/questions.py#L14) — `def create_question()`

**原因：** FastAPI 使用函数名作为路由的唯一操作 ID。两个不同路由使用了相同的函数名 `create_question`，导致 OpenAPI 模式生成错误。

**修复方案：** 将 `qa.py` 中的函数改名为 `create_qa_question`，保持全局唯一。

**修改文件：**
- `backend/app/api/v1/qa.py` — `create_question` → `create_qa_question`

---

## 错误 3：BigInteger 在 SQLite 中无法自增

**错误信息：**
```
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: sys_user.id
```

**出现位置：** 所有 9 个模型文件的 `id` 字段

**原因：** SQLite 的 `AUTOINCREMENT` 机制仅对 `INTEGER PRIMARY KEY` 生效。SQLAlchemy 的 `BigInteger` 类型在 SQLite 中映射为 `BIGINT`，不会被 SQLite 识别为可自增的 `INTEGER` 类型，导致插入时 `id` 为 NULL。MySQL 无此限制。

**修复方案：** 将所有模型的主键 `id` 字段从 `BigInteger` 改为 `Integer`；同时将所有外键引用从 `BigInteger` 改为 `Integer` 保持类型一致。

**修改文件（9 个模型 + SQL 脚本）：**
- `backend/app/models/user.py` — `id` 列类型
- `backend/app/models/course.py` — `id` 和 `teacher_id` 列类型
- `backend/app/models/chapter.py` — `id`, `course_id`, `parent_id` 列类型
- `backend/app/models/learning_record.py` — `id`, `user_id`, `course_id`, `chapter_id` 列类型
- `backend/app/models/note.py` — `id`, `user_id`, `chapter_id` 列类型
- `backend/app/models/qa.py` — `id`, `user_id`, `chapter_id` 列类型
- `backend/app/models/question.py` — `id`, `course_id` 列类型
- `backend/app/models/exam.py` — `id`, `course_id` 列类型
- `backend/app/models/exam_record.py` — `id`, `exam_id`, `user_id` 列类型
- `backend/sql/init.sql` — 所有 `BIGINT` → `INT`

---

## 错误 4：CURRENT_TIMESTAMP 跨数据库兼容性

**错误信息：**
```
Invalid isoformat string: 'CURRENT_TIMESTAMP'
```

**出现位置：** 所有使用 `server_default="CURRENT_TIMESTAMP"` 的模型

**原因：** `server_default` 接受字符串字面值时，SQLAlchemy 将其作为字面 SQL 默认值传递给 DDL。SQLite 将未加括号的 `CURRENT_TIMESTAMP` 作为字符串字面值存储，导致 Pydantic 验证 `DateTime` 字段时收到字符串 `"CURRENT_TIMESTAMP"` 而非 datetime 对象。MySQL 能正确评估。

**修复方案：** 使用 SQLAlchemy 的 `text()` 函数包装 SQL 表达式，告知数据库引擎这是一个 SQL 函数调用而非字符串字面值。

**修改前：**
```python
created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")
```

**修改后：**
```python
from sqlalchemy import text
created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
```

**修改文件：**
- `backend/app/models/user.py`
- `backend/app/models/course.py`
- `backend/app/models/learning_record.py`
- `backend/app/models/note.py`
- `backend/app/models/qa.py`

---

## 错误 5：缺少测试依赖 httpx

**错误信息：**
```
RuntimeError: The starlette.testclient module requires the httpx package to be installed.
```

**出现位置：** 运行测试时

**原因：** FastAPI/Starlette 的 `TestClient` 依赖 `httpx` 库，但 `requirements.txt` 中未包含。

**修复方案：** 在 `requirements.txt` 中添加 `httpx>=0.27.0` 和 `aiofiles>=24.0`。

**修改文件：**
- `backend/requirements.txt` — 添加 `httpx` 和 `aiofiles`

---

## 错误 6：Windows 端口 8000 被系统保留导致无法启动

**错误信息：**
```
ERROR: [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。
```

**出现位置：** 运行 `python -m app.main` 启动后端时

**原因：** Windows 的 Hyper-V / WSL / NAT 驱动会保留一部分动态端口范围。通过 `netsh interface ipv4 show excludedportrange protocol=tcp` 查看发现端口 **7979-8078** 被系统排除，端口 8000 正好落入该范围，导致应用无法绑定。

```
协议 tcp 端口排除范围
开始端口    结束端口
----------   --------
    ...
    7979        8078
    ...
```

**修复方案：** 将后端端口从 8000 改为 8090（避开系统保留范围）。涉及文件：

- `backend/app/main.py` — uvicorn 监听端口 `8000` → `8090`
- `frontend/vite.config.js` — 代理 target `localhost:8000` → `localhost:8090`
- `README.md` — 所有 URL 中的 `8000` → `8090`

> **提示：** 如果端口 8090 也不可用，可通过 `netsh interface ipv4 show excludedportrange protocol=tcp` 查看当前排除范围，选择一个范围外的端口。常见安全选择：3000、5000、8080、8090、9000。

**修改文件：**
- `backend/app/main.py` — 端口变更
- `frontend/vite.config.js` — 代理目标端口变更
- `README.md` — 文档端口更新

---

## 错误 7：NoteCreate schema 多余字段导致 422 验证错误

**错误信息：**
```json
{"detail": [{"type": "missing", "loc": ["body", "chapter_id"], "msg": "Field required"}]}
```

**出现位置：** `POST /chapters/{chapter_id}/notes` 创建笔记时

**原因：** `NoteCreate` schema 定义了 `chapter_id: int` 必填字段，但 `chapter_id` 实际从 URL 路径获取（`/chapters/{chapter_id}/notes`），无需在请求体中重复传入。前端只发送 `{ content, timestamp }`，导致 Pydantic 验证失败。

**修复方案：** 从 `NoteCreate` schema 中移除 `chapter_id` 字段。

**修改前：**
```python
class NoteCreate(BaseModel):
    chapter_id: int
    content: str
    timestamp: Optional[int] = None
```

**修改后：**
```python
class NoteCreate(BaseModel):
    content: str
    timestamp: Optional[int] = None
```

**修改文件：**
- `backend/app/schemas/note.py`

---

## 错误 8：Player.vue 章节切换双重触发

**错误表现：** 用户在侧边栏点击章节时，`switchChapter()` 被调用两次——第一次来自 `@click` 事件，第二次来自 `router.replace()` 触发的 `watch(route.params.chapterId)`，导致不必要的重复操作。

**出现位置：** [frontend/src/views/course/Player.vue](frontend/src/views/course/Player.vue)

**原因：** `switchChapter()` 中调用 `router.replace()` 修改了路由参数，而 `watch(() => route.params.chapterId)` 监听到变化后又调用了一次 `switchChapter()`，形成双重触发链。

**修复方案：**
1. `switchChapter` 顶层添加重复判断：`if (currentChapter.value?.id === ch.id) return`
2. `watch` 回调内同样添加重复判断，避免对已激活的章节重复赋值
3. 将位置恢复逻辑统一交给 `onPlayerReady`（`:key` 变化导致组件重载后自动触发）

**修改文件：**
- `frontend/src/views/course/Player.vue`

---

## 错误 9：学习进度断点续播位置恢复时序不稳定

**错误表现：** 切换章节后，通过 `setTimeout(500)` 恢复播放位置，但 video.js 初始化时间不固定，可能恢复失败或跳到错误位置。

**出现位置：** [frontend/src/views/course/Player.vue](frontend/src/views/course/Player.vue#L162-L168)（已修复）

**原因：** `switchChapter()` 中用硬编码的 500ms 延迟去设置播放位置，但 `:key` 变化导致 `VideoPlayer` 组件完全销毁重建，video.js 的 `ready` 事件触发时间受网络、视频时长等因素影响，500ms 不一定够。

**修复方案：** 断点续播统一在 `onPlayerReady` 事件中处理。当 `:key` 变化 → 旧组件 dispose → 新组件 mount → video.js 初始化完成 → 触发 `@ready` → `onPlayerReady` 从 `chapterProgressMap` 读取 `last_position` 并 seek。

**修改文件：**
- `frontend/src/views/course/Player.vue` — 移除 `setTimeout` 逻辑，依赖 `onPlayerReady`

---

## 验证结果

后端 15 项 E2E 测试全部通过：
```
[PASS] 1: Health GET /
[PASS] 2: Save progress
[PASS] 4: Get course progress
[PASS] 5: Learning history
[PASS] 6: Complete chapter
[PASS] 8: Create note
[PASS] 9: List notes
[PASS] 10: Update note
[PASS] 11: Delete note
[PASS] 12: GET /users (admin)
[PASS] 13: Course list
[PASS] 14: Course detail
[PASS] 15: Chapter tree
=== ALL 15 TESTS PASSED ===
```

后端启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

基础功能测试全部通过：

```
[PASS] 1: GET /
[PASS] 2: Register
[PASS] 3: Login
[PASS] 4: GET /auth/me
[PASS] 5: List courses empty
[PASS] 6: Student cannot create
[PASS] 7: Course 404
[PASS] 8: Chapter 404
```

前端生产构建成功：
```
✓ 1742 modules transformed.
✓ built in 13.08s
```

---

## 修改文件汇总

| 文件 | 错误编号 | 修改内容 |
|------|---------|---------|
| `backend/app/schemas/chapter.py` | 1 | 添加 `from __future__ import annotations` |
| `backend/app/api/v1/qa.py` | 2 | 函数名 `create_question` → `create_qa_question` |
| `backend/app/models/user.py` | 3, 4 | `BigInteger`→`Integer`，`server_default`→`text()` |
| `backend/app/models/course.py` | 3, 4 | `BigInteger`→`Integer`，`server_default`→`text()` |
| `backend/app/models/chapter.py` | 3 | `BigInteger`→`Integer` |
| `backend/app/models/learning_record.py` | 3, 4 | `BigInteger`→`Integer`，`server_default`→`text()` |
| `backend/app/models/note.py` | 3, 4 | `BigInteger`→`Integer`，`server_default`→`text()` |
| `backend/app/models/qa.py` | 3, 4 | `BigInteger`→`Integer`，`server_default`→`text()` |
| `backend/app/models/question.py` | 3 | `BigInteger`→`Integer` |
| `backend/app/models/exam.py` | 3 | `BigInteger`→`Integer` |
| `backend/app/models/exam_record.py` | 3 | `BigInteger`→`Integer` |
| `backend/sql/init.sql` | 3 | 所有 `BIGINT` → `INT` |
| `backend/requirements.txt` | 5 | 添加 `httpx` 和 `aiofiles` |
| `backend/app/main.py` | 6 | 端口 `8000` → `8090` |
| `frontend/vite.config.js` | 6 | 代理 target 端口 `8000` → `8090` |
| `README.md` | 6 | 文档中所有端口 `8000` → `8090` |
| `backend/app/schemas/note.py` | 7 | 移除 `NoteCreate.chapter_id` 字段 |
| `frontend/src/views/course/Player.vue` | 8, 9 | 修复章节切换双重触发 + 位置恢复时序 |
