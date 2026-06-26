---
name: "dvlyadmin-element-plus-icons-habits"
description: "指导 lyadmin 项目中正确使用 @element-plus/icons-vue 图标库。禁止使用不存在的图标如 Global 等。Invoke when importing or using icons from @element-plus/icons-vue."
---

# Element Plus Icons Vue 使用规范

## 禁止使用的图标

以下图标在 `@element-plus/icons-vue` 中**不存在**，禁止使用：

| 错误图标名 | 说明 | 替代方案 |
|-----------|------|---------|
| `Global` | 不存在 | 使用 `Monitor` 或 `Connection` |
| `GlobalIcon` | 不存在 | 使用 `Monitor` 或 `Connection` |

## 常用有效图标列表

```javascript
// ✅ 正确导入
import {
  Document,           // 文档
  ChatLineRound,      // 对话
  Connection,         // 连接/网络
  DataLine,           // 数据/图表
  CircleCheck,        // 勾选
  ChatDotRound,       // 会话/消息
  Monitor,            // 监控/全局
  Plus,               // 加号
  Delete,
  Edit,
  Search,
  Setting,
  Close,
  ArrowRight,
  ArrowLeft,
  ArrowUp,
  ArrowDown,
  CaretRight,
  CaretBottom,
  Loading,
  Warning,
  InfoFilled,
  SuccessFilled,
  CircleCloseFilled,
  QuestionFilled,
  // ... 其他 Element Plus 标准图标
} from '@element-plus/icons-vue'
```

## 如何查找可用图标

1. **官方文档**: https://element-plus.org/zh-CN/component/icon.html
2. **在线搜索**: 在 Element Plus 官网图标页面搜索需要的图标
3. **IDE 提示**: 输入 `import { ` 后查看 IDE 自动补全列表

## 使用示例

```vue
<template>
  <el-icon><Monitor /></el-icon>        <!-- 全局/监控 -->
  <el-icon><ChatDotRound /></el-icon>  <!-- 会话 -->
  <el-icon><Document /></el-icon>      <!-- 文档 -->
</template>

<script setup>
import { Monitor, ChatDotRound, Document } from '@element-plus/icons-vue'
</script>
```

## 图标选择建议

| 场景 | 推荐图标 |
|-----|---------|
| 全局变量 | `Monitor` 或 `Connection` |
| 会话变量 | `ChatDotRound` |
| 开始节点 | `CircleCheck` 或 `VideoPlay` |
| AI对话 | `ChatLineRound` |
| 知识库 | `Document` 或 `Reading` |
| HTTP请求 | `Connection` |
| 工具/设置 | `Tools` 或 `Setting` |

## 错误示例 ❌

```javascript
// 错误！Global 不存在
import { Global } from '@element-plus/icons-vue'
```

## 正确示例 ✅

```javascript
// 正确！使用 Monitor 代替 Global
import { Monitor } from '@element-plus/icons-vue'
```
