<template>
    <ly-dialog v-model="dialogVisible" :title="dialogTitle" width="640px" :before-close="handleClose">
        <el-form
        :inline="false"
        :model="formData"
        :rules="rules"
        ref="formRef"
        label-position="right"
        label-width="auto"
        >
        <el-form-item label="所属字典：" prop="parent">
            <el-select
            v-model="formData.parent"
            placeholder="请选择"
            clearable
            filterable
            style="width:100%"
            >
            <el-option
                v-for="item in dictionaryList"
                :key="item.id"
                :label="item.label"
                :value="item.id"
            />
            </el-select>
        </el-form-item>
        
        <el-form-item label="项名称" prop="label">
            <el-input v-model="formData.label" clearable />
        </el-form-item>
        
        <el-form-item label="数据值" prop="value">
            <el-input v-model="formData.value" clearable />
        </el-form-item>
        
        <el-form-item label="是否有效" prop="status">
            <el-switch v-model="formData.status" />
        </el-form-item>
        
        <el-form-item label="排序：" prop="sort">
            <el-input-number v-model="formData.sort" :min="0" :max="9999" />
        </el-form-item>
        
        <el-form-item label="备注：" prop="remark">
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
    import { ref, reactive, defineEmits, nextTick } from 'vue'
    import { deepClone } from '@/utils/util'
    import Api from '@/api/api'
    import LyDialog from '@/components/dialog/dialog.vue'
    import {ElMessage} from 'element-plus'

    const emit = defineEmits(['refreshData'])

    // 组件状态
    const dialogVisible = ref(false)
    const loading = ref(false)
    const dialogTitle = ref('')
    const formRef = ref(null)

    // 表单数据
    const formData = reactive({
        parent: '',
        label: '',
        value: '',
        sort: 1,
        status: true,
        remark: ''
    })

    // 表单验证规则
    const rules = reactive({
        parent: [
            { required: true, message: '请选择所属字典', trigger: 'blur' }
        ],
        label: [
            { required: true, message: '请输入项名称', trigger: 'blur' }
        ],
        value: [
            { required: true, message: '请输入数据值', trigger: 'blur' }
        ]
    })

    // 字典列表
    const dictionaryList = ref([])

    // 打开弹窗方法
    const addModuleFn = async (item, flag, parent) => {
        dialogVisible.value = true
        dialogTitle.value = flag
        await fetchDictionaryList()
        
        if (item) {
            Object.assign(formData, deepClone(item))
            // 确保状态是布尔值
            formData.status = !!item.status
        } else {
            formData.parent = parent
        }
        
        // 重置表单验证
        nextTick(() => {
            if (formRef.value) {
                formRef.value.clearValidate()
            }
        })
    }

    // 获取字典列表
    const fetchDictionaryList = async () => {
        try {
            const res = await Api.systemDictionary({
                parent_isnull: true,
                page: 1,
                limit: 999
            })
            
            if (res.code === 2000) {
                dictionaryList.value = res.data.data
            }
        } catch (error) {
            console.error('获取字典列表失败:', error)
        }
    }

    // 关闭弹窗
    const handleClose = () => {
        // 重置表单
        Object.assign(formData, {
            parent: '',
            label: '',
            value: '',
            sort: 1,
            status: true,
            remark: ''
        })
        
        dialogVisible.value = false
    }

    // 提交表单
    const submitForm = async () => {
        try {
            // 验证表单
            const valid = await formRef.value.validate()
            if (!valid) return
            
            loading.value = true
            
            const params = {
            ...formData,
            // 确保状态是字符串形式
            status: formData.status ? '1' : '0'
            }
            
            // 根据是否有ID决定是新增还是编辑
            const apiMethod = formData.id 
            ? Api.systemDictionaryEdit 
            : Api.systemDictionaryAdd
            
            const res = await apiMethod(params)
            
            if (res.code === 2000) {
                ElMessage.success(res.msg)
                emit('refreshData',formData.parent)
                handleClose()
            } else {
                ElMessage.warning(res.msg)
            }
        } catch (error) {
            console.error('提交表单失败:', error)
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