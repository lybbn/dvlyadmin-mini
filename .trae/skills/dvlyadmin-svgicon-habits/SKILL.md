---
name: "dvlyadmin-svgicon-habits"
description: "指导 lyadmin 项目中 SvgIcon 自定义图标组件的使用方式。Invoke when using custom SVG icons or the SvgIcon component in lyadmin project."
---

# lyadmin SvgIcon 自定义图标使用指南

## 组件概述

SvgIcon 组件位于 `frontend/src/components/icons/SvgIcon.vue`，支持两种图标类型：
1. **Element Plus 图标** - 直接使用图标名称
2. **自定义 SVG 图标** - 使用 `lyicon-` 前缀

## 使用方法

### 1. 引入组件

```javascript
import SvgIcon from '@/components/icons/SvgIcon.vue'
```

### 2. 使用 Element Plus 图标

直接使用 Element Plus 的图标名称（无需前缀）：

```vue
<template>
  <!-- Element Plus 图标 -->
  <SvgIcon icon-class="Search" />
</template>
```

### 3. 使用自定义 SVG 图标

自定义图标需要添加 `lyicon-` 前缀：

```vue
<template>
  <!-- 自定义 SVG 图标 -->
  <SvgIcon icon-class="lyicon-more" />
  <SvgIcon icon-class="lyicon-new-chat" />
</template>
```

## 自定义图标存放位置

自定义 SVG 图标文件存放在：
```
frontend/src/assets/lybbn/icons/svg/
```

例如：
- `more.svg` → 使用 `lyicon-more`
- `new-chat.svg` → 使用 `lyicon-new-chat`

## 组件 Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| iconClass | String | 是 | '' | 图标名称（Element Plus 图标直接写名称，自定义图标加 lyicon- 前缀） |
| className | String | 否 | '' | 自定义 CSS 类名 |
| style | Object | 否 | - | 行内样式 |

## 完整示例

```vue
<template>
  <div>
    <!-- Element Plus 图标 -->
    <SvgIcon icon-class="Search" style="font-size: 20px;" />
    
    <!-- 自定义图标 -->
    <SvgIcon 
      icon-class="lyicon-more" 
      style="font-size: 22px; cursor: pointer;"
      class-name="my-custom-icon"
    />
  </div>
</template>

<script setup>
import SvgIcon from '@/components/icons/SvgIcon.vue'
</script>
```

## 添加新的自定义图标

1. 将 SVG 文件放入 `frontend/src/assets/lybbn/icons/svg/` 目录
2. 文件名即为图标标识，如 `my-icon.svg`
3. 使用时添加 `lyicon-` 前缀：`lyicon-my-icon`

## 注意事项

1. **必须区分图标类型**：Element Plus 图标直接使用名称，自定义图标必须加 `lyicon-` 前缀
2. **SVG 文件命名**：使用小写字母和连字符，如 `new-chat.svg`
3. **样式设置**：可通过 `style` 属性设置 `font-size` 来调整图标大小
