<template>
    <ly-dialog :title="titleMap[mode]" v-model="visible" width="568px" destroy-on-close @closed="emits('closed')">
        <el-form :model="formData" :rules="rules" :disabled="mode=='detail'" ref="dialogForm" label-width="auto">
            <el-form-item label="新密码" prop="newPassword">
                <el-input
                v-model="formData.newPassword"
                type="password"
                show-password
                placeholder="请输入新密码"
                />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
                <el-input
                v-model="formData.confirmPassword"
                type="password"
                show-password
                placeholder="请再次输入新密码"
                />
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="visible=false">取 消</el-button>
            <el-button v-if="mode!='detail'" type="primary" :loading="isSaveing" @click="submit()">确 定</el-button>
        </template>
    </ly-dialog>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import lyDialog from "@/components/dialog/dialog.vue"
    import {deepClone} from "@/utils/util.js"
    import { ElMessage, ElMessageBox } from 'element-plus'
    import { createCrudConfig } from '../crud.js'

    const emits = defineEmits(['refreshData', 'closed'])

    let crudOptions = ref(createCrudConfig().crudOptions)

    let mode = ref("add")
    const titleMap = {
        pass:"重置密码",
        add: '新增',
        edit: '编辑',
        detail: '查看'
    }
    let visible = ref(false)
    let isSaveing = ref(false)
    let dialogForm = ref(null)
    
    // 表单数据
    let formData = ref({
        newPassword:"",
        confirmPassword: "",
    })
    
    // 验证规则
    let rules = {
        newPassword: [{required: true, message: '请输入密码', trigger: 'blur'}],
        confirmPassword: [{required: true, message: '请输入确认密码', trigger: 'blur' }],
    }
    
    
    // 方法
    const handleOpen = (item = null,modeType = 'pass') => {
        mode.value = modeType
        visible.value = true
        if(item){
            formData.value.id = deepClone(item).id
        }
    }
    
    
    const submit = () => {
        dialogForm.value.validate(async (valid) => {
            if (valid) {
                if (formData.value.newPassword !== formData.value.confirmPassword) {
                    ElMessage.error('两次输入的密码不一致')
                    return
                }
                isSaveing.value = true
                let apiObj = crudOptions.value.request.resetPass
                const res = await apiObj(formData.value)
                isSaveing.value = false
                if(res.code == 2000) {
                    emits('refreshData')
                    visible.value = false
                    ElMessage.success("设置成功")
                } else {
                    ElMessageBox.alert(res.msg, "提示", {type: 'error'})
                }
            }
        })
    }
    
    onMounted(() => {
    })

    defineExpose({
        handleOpen
    })
</script>

<style>
</style>