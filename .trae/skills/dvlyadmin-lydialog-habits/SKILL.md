---
name: "dvlyadmin-lydialog-habits"
description: "提供 dvlyadmin 框架中 lydialog 组件的使用习惯和最佳实践指南。当需要使用 lydialog 组件编写弹窗功能时调用。"
---

# dvlyadmin lydialog 组件使用习惯指南

## 1. 基本使用规范

### 1.1 组件导入

- 导入位置：`frontend\src\components\dialog\dialog.vue`
- 导入方式：使用 `import LyDialog from '@/components/dialog/dialog.vue'`

### 1.2 父组件引用

- 使用 `<组件名 v-if="dialogVisiable" @closed="dialogVisiable=true" ref="lydialogRef"/>` 的方式引用
- 必须使用 `v-if` 控制组件的渲染
- 必须添加 `@closed` 事件处理器，设置 `dialogVisiable=true`
- 必须添加 `ref` 属性，用于后续调用组件的 `open()` 方法

### 1.3 打开关闭组件

使用以下方式打开关闭组件：

```javascript
const showDialog = () => {
    dialogVisiable.value = true
    nextTick(() => {
        lydialogRef.value?.open()
    })
}
```

## 2. 子组件结构

### 2.1 模板结构

```vue
<template>
    <LyDialog 
        v-model="visible" 
        :title="titleMap[mode]"
        :fullscreen="ismobile?true:isFullScreen"
        :append-to-body="true"
        bodyPadding="10px"
        width="730px"
        @closed="handleDialogClosed"
        @onChangeFullScreen="handleChangeFullScreen"
    >
        <!-- 内容区域 -->
        <div class="dialog-content">
            <!-- 表单或其他内容 -->
        </div>

        <!-- 底部按钮 -->
        <template #footer>
            <el-button @click="handleCancel" :disabled="loading">取消</el-button>
            <el-button type="primary" @click="handleSave" :loading="loading">保存</el-button>
        </template>
    </LyDialog>
</template>
```

### 2.2 脚本结构

```vue
<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import LyDialog from '@/components/dialog/dialog.vue'
import { deepClone } from "@/utils/util.js"
import { ElMessage } from 'element-plus'
import { useSiteThemeStore } from "@/store/siteTheme";

const emit = defineEmits(['refresh', 'closed'])

const visible = ref(false)
const loading = ref(false)
const mode = ref("add")
const isFullScreen = ref(false)

// 响应式数据
let ismobile = computed(() => {
    return siteThemeStore.ismobile
})

// 标题映射
const titleMap = {
  add: '添加xxx',
  edit: '编辑xxx'
}

// 默认表单数据
const defaultFormData = {
    // 表单字段
}

// 表单数据
const formData = ref(deepClone(defaultFormData))

// 动态验证规则
const currentRules = computed(() => ({
    // 验证规则
}))

// 处理全屏切换
function handleChangeFullScreen(fullscreen) {
    isFullScreen.value = fullscreen
}

// 打开弹窗
const open = async (item = null, modeType = 'add') => {
    mode.value = modeType
    visible.value = true
    
    await nextTick()
    
    if (item) {
        formData.value = deepClone(item)
    }
}

// 处理弹窗关闭
const handleDialogClosed = () => {
    emit('closed')
}

// 取消操作
const handleCancel = () => {
    visible.value = false
}

// 保存操作
const handleSave = async () => {
    // 表单验证和保存逻辑
}

// 暴露方法
defineExpose({
    open
})
</script>
```

## 3. 组件配置

### 3.1 基本配置

- `v-model="visible"`：控制弹窗的显示/隐藏
- `:title="titleMap[mode]"`：根据模式动态设置标题
- `:fullscreen="ismobile?true:isFullScreen"`：移动端自动全屏，PC端可切换
- `:append-to-body="true"`：将弹窗 append 到 body
- `bodyPadding="10px"`：设置弹窗内容区域的内边距
- `width="730px"`：设置弹窗宽度

### 3.2 事件处理

- `@closed="handleDialogClosed"`：处理弹窗关闭事件
- `@onChangeFullScreen="handleChangeFullScreen"`：处理全屏切换事件

## 4. 表单处理

### 4.1 表单结构

```vue
<el-form 
    ref="dialogFormRef" 
    :model="formData" 
    :rules="currentRules" 
    label-width="auto"
    label-position="top"
    class="settings-form"
>
    <el-form-item label="名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入名称" />
    </el-form-item>
    <!-- 其他表单项 -->
</el-form>
```

### 4.2 表单验证

```javascript
const currentRules = computed(() => ({
    name: [
        { required: true, message: '请输入名称', trigger: 'blur' }
    ],
    // 其他验证规则
}))

const handleSave = async () => {
    if (!dialogFormRef.value) return
    
    try {
        loading.value = true
        
        const valid = await dialogFormRef.value.validate()
        if (!valid) {
            ElMessage.warning('请检查填写是否正确')
            return
        }
        // 保存逻辑
    } catch (error) {

    } finally {
        loading.value = false
    }
}
```

## 5. 模式处理

### 5.1 模式定义

- `add`：添加模式
- `edit`：编辑模式

### 5.2 模式切换

```javascript
const open = async (item = null, modeType = 'add') => {
    mode.value = modeType
    visible.value = true
    
    await nextTick()
    
    if (item) {
        formData.value = deepClone(item)
    }
}
```

## 6. 最佳实践

### 6.1 代码组织

- 将弹窗相关的逻辑封装到独立的组件中
- 使用 `defineExpose` 暴露 `open` 方法，方便父组件调用
- 使用 `computed` 计算属性处理动态数据

### 6.2 性能优化

- 使用 `v-if` 控制组件的渲染，而不是 `v-show`
- 使用 `nextTick` 确保组件渲染完成后再调用 `open()` 方法
- 使用 `deepClone` 深拷贝数据，避免直接修改原始数据

### 6.3 用户体验

- 添加 `loading` 状态，防止重复提交
- 使用 `ElMessage` 显示操作结果
- 提供清晰的标题和操作按钮

## 7. 完整示例

### 7.1 子组件完整示例

```vue
<template>
    <LyDialog 
        v-model="visible" 
        :title="titleMap[mode]"
        :fullscreen="ismobile?true:isFullScreen"
        :append-to-body="true"
        bodyPadding="10px"
        width="730px"
        @closed="handleDialogClosed"
        @onChangeFullScreen="handleChangeFullScreen"
    >
        <div class="dialog-content">
            <el-form 
                ref="dialogFormRef" 
                :model="formData" 
                :rules="currentRules" 
                label-width="auto"
                label-position="top"
                class="settings-form"
            >
                <el-form-item label="名称" prop="name">
                    <el-input v-model="formData.name" placeholder="请输入名称" />
                </el-form-item>
                <el-form-item label="描述" prop="desc">
                    <el-input
                        v-model="formData.desc"
                        type="textarea"
                        placeholder="请输入描述"
                        :rows="2"
                        maxlength="256"
                        show-word-limit
                    />
                </el-form-item>
            </el-form>
        </div>

        <template #footer>
            <el-button @click="handleCancel" :disabled="loading">取消</el-button>
            <el-button type="primary" @click="handleSave" :loading="loading">保存</el-button>
        </template>
    </LyDialog>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import LyDialog from '@/components/dialog/dialog.vue'
import { deepClone } from "@/utils/util.js"
import { ElMessage } from 'element-plus'
import { useSiteThemeStore } from "@/store/siteTheme";
import Api from '@/api/api'

const siteThemeStore = useSiteThemeStore()

const emit = defineEmits(['refresh', 'closed'])

const visible = ref(false)
const loading = ref(false)
const mode = ref("add")
const dialogFormRef = ref(null)
let ismobile = computed(() => {
    return siteThemeStore.ismobile
})
const isFullScreen = ref(false)

const titleMap = {
  add: '添加数据',
  edit: '编辑数据'
}

// 默认表单数据
const defaultFormData = {
    name: '',
    desc: ''
}

// 表单数据
const formData = ref(deepClone(defaultFormData))

// 动态验证规则
const currentRules = computed(() => ({
    name: [
        { required: true, message: '请输入名称', trigger: 'blur' }
    ],
    desc: [
        { required: true, message: '请输入描述', trigger: 'blur' }
    ]
}))

function handleChangeFullScreen(fullscreen) {
    isFullScreen.value = fullscreen
}

const open = async (item = null, modeType = 'add') => {
    mode.value = modeType
    visible.value = true
    
    await nextTick()
    
    if (item) {
        formData.value = deepClone(item)
    }
}

const handleDialogClosed = () => {
    emit('closed')
}

const handleCancel = () => {
    visible.value = false
}

const handleSave = async () => {
    if (!dialogFormRef.value) return
    
    try {
        loading.value = true
        
        const valid = await dialogFormRef.value.validate()
        if (!valid) {
            ElMessage.warning('请检查填写是否正确')
            return
        }
        const apiObj = mode.value === 'add' ? Api.addData : Api.editData
        const res = await apiObj(formData.value)
        if(res.code === 2000){
            ElMessage.success(res.msg || '保存成功')
            emit('refresh')
            emit('closed')
        }else{
            ElMessage.error(res.msg || '保存失败')
        }
        
    } catch (error) {

    } finally {
        loading.value = false
    }
}

defineExpose({
    open
})
</script>

<style lang="scss" scoped>

</style>
```

### 7.2 父组件使用示例

```vue
<template>
    <div>
        <el-button type="primary" @click="showDialog">打开弹窗</el-button>
        <MyDialog 
            v-if="dialogVisiable" 
            @closed="dialogVisiable=true" 
            ref="lydialogRef"
            @refresh="handleRefresh"
        />
    </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import MyDialog from './components/MyDialog.vue'

const dialogVisiable = ref(false)
const lydialogRef = ref(null)

const showDialog = () => {
    dialogVisiable.value = true
    nextTick(() => {
        lydialogRef.value?.open()
    })
}

const handleRefresh = () => {
    // 刷新数据
}
</script>
```

## 8. 常见问题与解决方案

### 8.1 弹窗无法打开

- 检查 `dialogVisiable` 是否正确设置为 `true`
- 检查 `lydialogRef` 是否正确引用
- 检查是否使用了 `nextTick` 确保组件渲染完成

### 8.2 弹窗关闭后无法重新打开

- 检查 `@closed` 事件处理器是否正确设置 `dialogVisiable=true`
- 检查 `handleDialogClosed` 方法是否正确调用 `emit('closed')`

### 8.3 表单验证失败

- 检查 `currentRules` 是否正确定义
- 检查 `dialogFormRef` 是否正确引用
- 检查表单字段是否与验证规则对应

## 9. 总结

遵循以上使用习惯和最佳实践，可以确保 lydialog 组件的正确使用，提高代码的一致性和可维护性。在使用 lydialog 组件编写弹窗功能时，请始终参考本指南，确保代码质量和用户体验。