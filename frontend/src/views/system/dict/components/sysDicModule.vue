<template>
    <ly-dialog v-model="dialogVisible" :title="dialogTitle" width="640px" :before-close="handleClose">
        <el-form :inline="false" :model="formData" :rules="rules" ref="formRef" label-position="right" label-width="auto">
        <el-form-item label="字典名称" prop="label">
            <el-input v-model.trim="formData.label" placeholder="字典名称"/>
        </el-form-item>
        
        <el-form-item label="字典编号" prop="value">
            <el-input v-model.trim="formData.value" placeholder="字典编号"/>
        </el-form-item>
        
        <el-form-item label="排序" prop="sort">
            <el-input-number v-model="formData.sort" :min="0" :max="9999" />
        </el-form-item>
        
        <el-form-item label="备注" prop="remark">
            <el-input type="textarea" :rows="2" v-model="formData.remark" />
        </el-form-item>
        </el-form>
        
        <template #footer>
            <el-button @click="handleClose" :loading="loading">关闭</el-button>
            <el-button type="primary" @click="submitForm" :loading="loading">保存</el-button>
        </template>
    </ly-dialog>
</template>

<script setup>
    import { ref, reactive } from 'vue'
    import { deepClone } from '@/utils/util'
    import Api from '@/api/api'
    import LyDialog from '@/components/dialog/dialog.vue'
    import {ElMessage} from 'element-plus'

    const emit = defineEmits(['refreshData'])

    const dialogVisible = ref(false)
    const loading = ref(false)
    const dialogTitle = ref('')
    const formRef = ref(null)

    const formData = reactive({
        label: '',
        value: '',
        sort: 1,
        remark: ''
    })

    // Validation rules
    const rules = reactive({
        label: [
            { required: true, message: '请输入名称', trigger: 'blur' }
        ],
        value: [
            { required: true, message: '请输入key值', trigger: 'blur' }
        ]
    })

    // Open dialog method
    const addModuleFn = (item, flag) => {
        dialogVisible.value = true
        dialogTitle.value = flag
        
        if (item) {
            Object.assign(formData, deepClone(item))
        } else {
            resetForm()
        }
    }

    // Reset form data
    const resetForm = () => {
        Object.assign(formData, {
            label: '',
            value: '',
            sort: 1,
            remark: ''
        })
    }

    const handleClose = () => {
        resetForm()
        dialogVisible.value = false
    }

    const submitForm = async () => {
        try {
            const valid = await formRef.value.validate()
            if (!valid) return
            
            loading.value = true
            
            const params = { ...formData }
            
            const apiMethod = formData.id 
            ? Api.systemDictionaryEdit 
            : Api.systemDictionaryAdd
            
            const res = await apiMethod(params)
            
            if (res.code === 2000) {
                ElMessage.success(res.msg)
                emit('refreshData')
                handleClose()
            } else {
                ElMessage.warning(res.msg)
            }
        } catch (error) {
            console.error('提交失败:', error)
        } finally {
            loading.value = false
        }
    }

    defineExpose({
        addModuleFn
    })
</script>

<style scoped>
    .el-form-item {
        margin-bottom: 18px;
    }

    .el-input-number {
        width: 100%;
    }

    .el-textarea {
        width: 100%;
    }
</style>