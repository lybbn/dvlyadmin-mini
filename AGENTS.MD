# AGENTS.md — AI Agent 引导

dvlyadmin-mini：Django + DRF 后端（`backend/`），Vue3 + Element Plus 前端（`frontend/`）。

## 目录结构（规则与技能入口）

```
.trae/
├── rules/                     # 项目强制规则，动手前必读
│   └── AGENTS.md              # Django Migration 文件保护规则
└── skills/                    # 技能库，每个子目录一个 SKILL.md
```

## 必守规则

**严禁编辑/删除/手动创建** `apps/*/migrations/` 下任何文件，模型变更只跑 `python manage.py makemigrations <app>`。详见 `.trae/rules/AGENTS.md`。

## Skills（任务命中场景时，先读对应 `.trae/skills/<name>/SKILL.md` 再写代码）

## 原则

优先用框架内置能力，不改底层源码；组件用法不确定时查 SKILL.md，不猜测。
