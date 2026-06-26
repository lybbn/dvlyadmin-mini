---
name: "dvlyadmin-pagination-habits"
description: "指导如何在项目中使用 Pagination.vue 分页组件。当新建页面或需要分页功能时，必须调用此 skill 获取正确的使用方式。"
---

# Pagination 分页组件使用指南

## 组件位置
`frontend/src/components/Pagination.vue`

## 何时使用
- 新建页面需要分页功能时
- 列表数据需要分页展示时
- 需要统一分页样式和交互时

## 基本用法

### 1. 导入组件
```vue
<script setup>
import Pagination from '@/components/Pagination.vue'
</script>
```

### 2. 模板中使用
```vue
<template>
  <div class="page-container">
    <!-- 表格或其他列表内容 -->
    <el-table :data="tableData">
      <!-- 列定义 -->
    </el-table>
    
    <!-- 分页组件 -->
    <Pagination v-bind:child-msg="pageparm" @callFather="callFather"/>
  </div>
</template>
```

### 3. 数据定义
```vue
<script setup>
import { ref } from 'vue'

// 分页参数
const pageparm = ref({
  page: 1,      // 当前页码
  limit: 20,    // 每页条数
  total: 0      // 总条数
})

// 查询参数
const formInline = ref({
  page: 1,
  limit: 20,
  // 其他查询条件...
})

// 表格数据
const tableData = ref([])
</script>
```

### 4. 方法实现
```vue
<script setup>
// 处理分页变化
const callFather = (parm) => {
  formInline.value.page = parm.page
  formInline.value.limit = parm.limit
  getData()
}

// 获取数据
const getData = async () => {
  try {
    loading.value = true
    const res = await Api.getList(formInline.value)
    if (res.code == 2000) {
      tableData.value = res.data.data
      pageparm.value.page = res.data.page
      pageparm.value.limit = res.data.limit
      pageparm.value.total = res.data.total
    }
  } finally {
    loading.value = false
  }
}

// 搜索（重置分页）
const search = () => {
  formInline.value.page = 1
  formInline.value.limit = 20
  getData()
}
</script>
```

## 组件 Props

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| childMsg | Object | {} | 分页数据对象，包含 page、limit、total |
| pageSizes | Array | [10,20,30,40,50,100,200,500] | 每页显示条数选项 |
| layout | String | "total, sizes, prev, pager, next, jumper" | 分页组件布局 |
| small | Boolean | false | 是否使用小尺寸 |
| border | Boolean | true | 是否显示边框 |
| position | String | "center" | 分页位置：center/left/right |
| hideOnSinglePage | Boolean | false | 只有一页时是否隐藏 |

## 完整示例

```vue
<template>
  <div class="page-container">
    <el-table :data="tableData" v-loading="loading">
      <el-table-column type="index" label="序号" width="60">
        <template #default="{ $index }">
          {{ getIndex($index) }}
        </template>
      </el-table-column>
      <!-- 其他列 -->
    </el-table>
    
    <Pagination v-bind:child-msg="pageparm" @callFather="callFather"/>
  </div>
</template>

<script setup name="YourPageName">
import { ref, onMounted } from 'vue'
import Pagination from '@/components/Pagination.vue'
import Api from '@/api/api'

const loading = ref(false)
const tableData = ref([])
const pageparm = ref({
  page: 1,
  limit: 20,
  total: 0
})

const formInline = ref({
  page: 1,
  limit: 20
})

// 获取序号
const getIndex = (index) => {
  return (pageparm.value.page - 1) * pageparm.value.limit + index + 1
}

// 分页回调
const callFather = (parm) => {
  formInline.value.page = parm.page
  formInline.value.limit = parm.limit
  getData()
}

// 获取数据
const getData = async () => {
  try {
    loading.value = true
    const res = await Api.getList(formInline.value)
    if (res.code == 2000) {
      tableData.value = res.data.data
      pageparm.value.page = res.data.page
      pageparm.value.limit = res.data.limit
      pageparm.value.total = res.data.total
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  getData()
})
</script>
```

## 注意事项

1. **必须使用 `v-bind:child-msg`** 绑定分页数据，不能直接写 `:child-msg`
2. **必须监听 `@callFather` 事件** 处理分页变化
3. **搜索时要重置分页**：将 page 设为 1
4. **后端返回数据格式**：
   ```json
   {
     "code": 2000,
     "data": {
       "data": [],
       "page": 1,
       "limit": 20,
       "total": 100
     }
   }
   ```
