-- =============================================
-- 在线教育平台 数据库初始化脚本
-- 数据库: MySQL 8.4
-- =============================================

CREATE DATABASE IF NOT EXISTS edu_platform
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE edu_platform;

-- ---------------------------------------------
-- 1. 用户表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS sys_user (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)     NOT NULL UNIQUE COMMENT '用户名',
    password    VARCHAR(255)    NOT NULL COMMENT '密码(加密)',
    nickname    VARCHAR(100)    DEFAULT NULL COMMENT '昵称',
    email       VARCHAR(100)    DEFAULT NULL UNIQUE COMMENT '邮箱',
    avatar      VARCHAR(500)    DEFAULT NULL COMMENT '头像URL',
    role        VARCHAR(20)     NOT NULL DEFAULT 'student' COMMENT '角色: admin/teacher/student',
    status      TINYINT         NOT NULL DEFAULT 1 COMMENT '状态: 1=正常 0=禁用',
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_sys_user_username (username),
    INDEX idx_sys_user_role (role),
    INDEX idx_sys_user_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ---------------------------------------------
-- 2. 课程表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS course (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(200)    NOT NULL COMMENT '课程名称',
    description     TEXT            DEFAULT NULL COMMENT '课程描述',
    cover_image     VARCHAR(500)    DEFAULT NULL COMMENT '封面图片URL',
    category_id     INT DEFAULT NULL COMMENT '分类ID',
    teacher_id      INT NOT NULL COMMENT '讲师ID',
    price           DECIMAL(10,2)   NOT NULL DEFAULT 0.00 COMMENT '价格',
    status          VARCHAR(20)     NOT NULL DEFAULT 'draft' COMMENT '状态: draft/published/archived',
    student_count   INT             NOT NULL DEFAULT 0 COMMENT '学习人数',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_course_teacher (teacher_id),
    INDEX idx_course_category (category_id),
    INDEX idx_course_status (status),
    INDEX idx_course_title (title),
    CONSTRAINT fk_course_teacher FOREIGN KEY (teacher_id) REFERENCES sys_user(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程表';

-- ---------------------------------------------
-- 3. 章节表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS chapter (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    course_id   INT NOT NULL COMMENT '所属课程ID',
    title       VARCHAR(200)    NOT NULL COMMENT '章节标题',
    sort_order  INT             NOT NULL DEFAULT 0 COMMENT '排序',
    parent_id   INT DEFAULT NULL COMMENT '父章节ID(支持二级结构)',
    video_url   VARCHAR(500)    DEFAULT NULL COMMENT '视频URL',
    duration    INT             DEFAULT 0 COMMENT '视频时长(秒)',
    is_free     TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '是否免费: 0=否 1=是',
    INDEX idx_chapter_course (course_id),
    INDEX idx_chapter_sort (course_id, sort_order),
    INDEX idx_chapter_parent (parent_id),
    CONSTRAINT fk_chapter_course FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE,
    CONSTRAINT fk_chapter_parent FOREIGN KEY (parent_id) REFERENCES chapter(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='章节表';

-- ---------------------------------------------
-- 4. 学习记录表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS learning_record (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL COMMENT '用户ID',
    course_id       INT NOT NULL COMMENT '课程ID',
    chapter_id      INT NOT NULL COMMENT '章节ID',
    progress        FLOAT       NOT NULL DEFAULT 0 COMMENT '学习进度(0-100)',
    last_position   FLOAT       NOT NULL DEFAULT 0 COMMENT '上次播放位置(秒)',
    completed       TINYINT(1)  NOT NULL DEFAULT 0 COMMENT '是否完成: 0=否 1=是',
    created_at      DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_user_chapter (user_id, chapter_id),
    INDEX idx_learning_user_course (user_id, course_id),
    CONSTRAINT fk_learning_user FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_learning_course FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE,
    CONSTRAINT fk_learning_chapter FOREIGN KEY (chapter_id) REFERENCES chapter(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习记录表';

-- ---------------------------------------------
-- 5. 笔记表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS note (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL COMMENT '用户ID',
    chapter_id  INT NOT NULL COMMENT '章节ID',
    content     TEXT        NOT NULL COMMENT '笔记内容',
    timestamp   INT         DEFAULT NULL COMMENT '视频时间点(秒)',
    created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_note_user_chapter (user_id, chapter_id),
    CONSTRAINT fk_note_user FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_note_chapter FOREIGN KEY (chapter_id) REFERENCES chapter(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='笔记表';

-- ---------------------------------------------
-- 6. 问答表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS qa (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL COMMENT '提问用户ID',
    chapter_id  INT NOT NULL COMMENT '所属章节ID',
    question    TEXT        NOT NULL COMMENT '问题内容',
    answer      TEXT        DEFAULT NULL COMMENT '回答内容',
    created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_qa_chapter (chapter_id),
    INDEX idx_qa_user (user_id),
    CONSTRAINT fk_qa_user FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_qa_chapter FOREIGN KEY (chapter_id) REFERENCES chapter(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='问答表';

-- ---------------------------------------------
-- 7. 题库表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS question (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    course_id   INT NOT NULL COMMENT '所属课程ID',
    type        VARCHAR(20)     NOT NULL COMMENT '题型: single/multi/judge/fill',
    content     TEXT            NOT NULL COMMENT '题目内容',
    options     JSON            DEFAULT NULL COMMENT '选项(单选/多选题使用)',
    answer      TEXT            NOT NULL COMMENT '正确答案',
    analysis    TEXT            DEFAULT NULL COMMENT '题目解析',
    difficulty  TINYINT         NOT NULL DEFAULT 1 COMMENT '难度: 1=简单 2=中等 3=困难',
    INDEX idx_question_course (course_id),
    INDEX idx_question_type (type),
    CONSTRAINT fk_question_course FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题库表';

-- ---------------------------------------------
-- 8. 考试表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS exam (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    course_id       INT NOT NULL COMMENT '所属课程ID',
    title           VARCHAR(200)    NOT NULL COMMENT '考试名称',
    duration        INT             NOT NULL DEFAULT 60 COMMENT '考试时长(分钟)',
    total_score     DECIMAL(5,1)    NOT NULL DEFAULT 100.0 COMMENT '总分',
    passing_score   DECIMAL(5,1)    NOT NULL DEFAULT 60.0 COMMENT '及格分',
    start_time      DATETIME        DEFAULT NULL COMMENT '开始时间',
    end_time        DATETIME        DEFAULT NULL COMMENT '结束时间',
    status          VARCHAR(20)     NOT NULL DEFAULT 'draft' COMMENT '状态: draft/ongoing/ended',
    INDEX idx_exam_course (course_id),
    INDEX idx_exam_status (status),
    CONSTRAINT fk_exam_course FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试表';

-- ---------------------------------------------
-- 9. 考试记录表
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS exam_record (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    exam_id     INT NOT NULL COMMENT '考试ID',
    user_id     INT NOT NULL COMMENT '用户ID',
    score       DECIMAL(5,1)    DEFAULT NULL COMMENT '得分',
    answers     JSON            DEFAULT NULL COMMENT '用户答案(JSON格式)',
    start_time  DATETIME        NOT NULL COMMENT '开始答题时间',
    submit_time DATETIME        DEFAULT NULL COMMENT '提交时间',
    UNIQUE KEY uk_exam_user (exam_id, user_id),
    INDEX idx_exam_record_user (user_id),
    CONSTRAINT fk_exam_record_exam FOREIGN KEY (exam_id) REFERENCES exam(id) ON DELETE CASCADE,
    CONSTRAINT fk_exam_record_user FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试记录表';
