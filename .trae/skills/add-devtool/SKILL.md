---
name: "add-devtool"
description: "Step-by-step recipe for adding a new online tool to the PluginCenter frontend DevTools toolbox (registry, component conventions, SSR/fullscreen pitfalls, build verification). Invoke when user asks to add/create a new 在线工具/devtools tool."
---

# 添加 DevTools 在线工具

给 `frontend/` 的在线工具箱（DevTools，44+ 个工具）新增一个工具的完整步骤。工具箱架构：**配置驱动 + 懒加载分包**，页面（列表页/独立页）全部从配置自动派生，不需要改任何页面文件。

## 一、必改的两个文件（且仅有这两处）

### 1. `frontend/components/devtools/registry.ts` — 注册 loader

在 `toolLoaders` 中按**字母序**插入一行（key 与组件文件名一致）：

```ts
PortScanner: () => import('./PortScanner.vue'),
```

> `componentMap`（独立页用的异步组件+骨架屏）由 `toolLoaders` 自动派生，无需单独改。**两处 key 必须一致**的约束因此天然满足；新工具只需改这一处。

### 2. `frontend/components/devtools/devtools.config.ts` — 配置条目

把工具加入**最贴切分类**的 `tools` 数组：

```ts
{
  id: 'port-scan',            // 路由 id（/devtools/<id>），kebab-case，全局唯一
  name: '端口扫描',            // 卡片/独立页标题
  desc: '一句话功能描述',
  icon: 'DataLine',           // Element Plus 图标名（@element-plus/icons-vue 必须真实存在，先 node -e "require('@element-plus/icons-vue')" 验证；语义必须贴合功能，如端口扫描用 DataLine 而非泛用的 Position）
  iconClass: 'icon-ops',      // 分类统一色类，随分类固定（见下表）
  component: 'PortScanner',   // 必须与 registry key / 组件文件名一致
  tags: ['port', '扫描', ...], // 搜索关键词，中英混合
  // mode: 'local'（默认，可省略）| 'hybrid'（依赖后端时才标）
}
```

**7 个分类与 iconClass 对照**（icon 同分类内不得重复，跨分类可复用）：

| 分类 id | 名称 | iconClass | 色 |
|---|---|---|---|
| code | 代码工具 | icon-code | info |
| security | 编码与安全 | icon-lock | danger |
| converter | 数据转换 | icon-convert | primary |
| api | API调试 | icon-api | warning |
| image | 图片处理 | icon-image | success |
| design | 前端与设计 | icon-design | secondary |
| ops | 运维与部署 | icon-ops | info |

## 二、组件规范（`frontend/components/devtools/<ComponentName>.vue`）

**必须遵守 uniform 模式**（参照 `WebSocketTester.vue` 或最近新增的 `PortScanner.vue`）：

1. **模板**：根节点用共享 `ToolDialog`：

```vue
<ToolDialog
  :visible="visible" title="工具名" width="860px" icon="DataLine"
  :close-on-click-modal="false" append-to-body destroy-on-close
  @update:visible="$emit('update:visible', $event)"
>
```

2. **脚本**：
   - `props: { visible: Boolean, tool: Object }`；`emits: ['update:visible']`。
   - watch 必须写 `watch(() => props.visible, ...)`——**setup 里裸引用 prop 名是 ReferenceError**（历史踩坑）。
   - 关闭/卸载时清理资源（watch visible=false + onUnmounted 双保险）：关闭连接、clearInterval、abort 请求等。
   - **SSR 安全**：`window/location/document/localStorage` 只能出现在 `onMounted`、事件回调或函数体内，禁止 setup 顶层执行；`localStorage` 必须 try/catch（隐私模式会炸）；`crypto.randomUUID` 需 `typeof === 'function'` 回退。
3. **样式**：
   - scoped + 主题变量（`var(--el-color-*)` / `var(--color-brand)`），禁止硬编码主题色。
   - 全屏钩子写**整体单括号** `:global(.tool-dialog.is-fullscreen .xxx)`——**禁止 `:global(X) Y` 链式**，尾部选择器会被编译器丢弃（历史 81 处泄漏教训）。
   - 全屏时用 flex 链让主内容区（表格/编辑器/画布）`flex:1; min-height:0` 撑满。
4. **重依赖**（jszip/qrcode/yaml/sql-formatter 等）只在组件内 import——每个工具是独立 chunk，别把依赖提到全局。
5. 文件名 PascalCase，与 `component` 字段完全一致。

## 三、验证（必做）

```bash
cd frontend && npm run build
```

构建全绿后产物冒烟（可选但推荐）：

```bash
PORT=3210 node .output/server/index.mjs   # 任选空闲端口
curl -s http://localhost:3210/devtools/<tool-id> | grep -o "tool-skeleton" | head -1   # 200 且含骨架屏
curl -s http://localhost:3210/devtools | grep -o "<tool-name>" | head -1                  # 列表页有卡片
```

- `/devtools/[tool]` 页面的 SEO（title/description/面包屑/相关工具）由配置自动生成，无需新建页面文件。
- 工具 JS 应独立分包（构建产物里能看到以组件名命名的 chunk）；若其它工具 chunk 变大，说明把重依赖提升到了共享层，需回头检查 import 位置。

## 四、检查清单

- [ ] registry.ts `toolLoaders` 已加（字母序）
- [ ] devtools.config.ts 条目：id 唯一 / icon 真实存在且分类内不重复 / iconClass 对应分类 / tags 含中英文
- [ ] 组件遵守 ToolDialog uniform 模式 + `() => props.visible` 写法
- [ ] 浏览器 API 无 SSR 泄漏；关闭/卸载有清理
- [ ] 全屏 `:global()` 为整体单括号写法
- [ ] `npm run build` 全绿 + 冒烟 200
