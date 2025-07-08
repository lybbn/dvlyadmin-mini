<template>
    <div>
        <!-- 对话框组件 -->
        <ly-dialog 
        v-model="dialogVisible" 
        :title="loadingTitle" 
        width="560px" 
        :before-close="handleClose"
        >
        <!-- 表单区域 -->
        <el-form 
            :inline="false" 
            :model="formData" 
            :rules="rules" 
            ref="formRef" 
            label-position="right" 
            label-width="auto"
        >
            <!-- 分组名称输入 -->
            <el-form-item label="分组名称" prop="title">
            <el-input v-model="formData.title" placeholder="请输入分组名称" />
            </el-form-item>
            
            <!-- key值输入 -->
            <el-form-item label="key值" prop="key">
            <el-input v-model="formData.key" placeholder="请输入key值" />
            </el-form-item>
        </el-form>
        
        <!-- 对话框底部按钮 -->
        <template #footer>
                <el-button @click="handleClose" :loading="loadingSave">取消</el-button>
                <el-button type="primary" @click="submitForm" :loading="loadingSave">确定</el-button>
        </template>
        </ly-dialog>
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { ElMessage } from 'element-plus'
    import Api from "@/api/api"
    import LyDialog from "@/components/dialog/dialog.vue"
    import { deepClone } from '@/utils/util.js'

    const emit = defineEmits(['refreshData'])

    // 对话框显示状态
    const dialogVisible = ref(false)
    // 加载状态
    const loadingSave = ref(false)
    // 对话框标题
    const loadingTitle = ref('')
    // 表单引用
    const formRef = ref(null)

    // 表单数据
    const formData = ref({
        title: '',
        key: '',
    })

    // 表单验证规则
    const rules = {
        title: [
            { required: true, message: '请输入分组名称', trigger: 'blur' }
        ],
        key: [
            { required: true, message: '请输入key值', trigger: 'blur' }
        ]
    }
    /**
     * 关闭对话框处理
     */
    const handleClose = () => {
        dialogVisible.value = false
        loadingSave.value = false
        // 重置表单数据
        formData.value = {
            title: '',
            key: ''
        }
        // 触发父组件刷新数据
        emit('refreshData')
    }

    /**
     * 打开对话框方法
     * @param {Object} item - 编辑时的数据对象
     * @param {String} flag - 对话框标题
     */
    const addModuleFn = (item, flag) => {
        loadingTitle.value = flag
        dialogVisible.value = true
        if (item) {
            formData.value = deepClone(item)
        }
    }

    /**
     * 提交表单处理
     */
    const submitForm = async () => {
    try {
        // 验证表单
        const valid = await formRef.value.validate()
        if (!valid) return
        
        loadingSave.value = true
        
        // 准备提交参数
        const params = { ...formData.value }
        
        // 根据是否有id决定是新增还是编辑
        const apiFn = params.id ? Api.platformsettingsSysconfigEdit : Api.platformsettingsSysconfigAdd
        
        // 调用API
        const res = await apiFn(params)
        
        if (res.code === 2000) {
            ElMessage.success(res.msg)
            handleClose()
        } else {
            ElMessage.warning(res.msg)
        }
    } catch (error) {
        console.error('表单提交错误:', error)
    } finally {
        loadingSave.value = false
    }
    }

    defineExpose({
        addModuleFn
    })
</script>

<style scoped>
</style>