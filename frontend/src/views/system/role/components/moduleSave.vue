<template>
    <ly-dialog :title="titleMap[mode]" v-model="visible" width="500px" destroy-on-close @closed="emits('closed')">
        <el-form :model="formData" :rules="rules" :disabled="mode=='show'" ref="dialogForm" label-width="auto">
            <el-form-item label="角色名称" prop="name">
                <el-input v-model="formData.name" placeholder="请输入角色名称" clearable></el-input>
            </el-form-item>
            <el-form-item label="权限字符" prop="key">
                <el-input v-model="formData.key" placeholder="请输入权限标识，如：admin" clearable></el-input>
            </el-form-item>
            <el-form-item label="排序" prop="sort">
                <el-input-number v-model="formData.sort" controls-position="right" :min="1" style="width: 100%;"></el-input-number>
            </el-form-item>
            <el-form-item label="状态" prop="status">
                <el-switch v-model="formData.status" inline-prompt active-text="启用" inactive-text="禁用"></el-switch>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="visible=false">取 消</el-button>
            <el-button v-if="mode!='show'" type="primary" :loading="isSaveing" @click="submit()">保 存</el-button>
        </template>
    </ly-dialog>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import lyDialog from "@/components/dialog/dialog.vue"
    import {deepClone} from "@/utils/util.js"
    import Api from "@/api/api.js"
    import { ElMessage, ElMessageBox } from 'element-plus'
    import XEUtils from "xe-utils";

    const emits = defineEmits(['refreshData', 'closed'])

    let mode = ref("add")
    const titleMap = {
        add: '新增',
        edit: '编辑',
        detail: '查看'
    }
    let visible = ref(false)
    let isSaveing = ref(false)
    let dialogForm = ref(null)
    
    // 表单数据
    let formData = ref({
        id: "",
        key: "",
        name: "",
        sort: 1,
        status: true,
    })
    
    // 验证规则
    let rules = {
        sort: [
            {required: true, message: '请输入排序', trigger: 'change'}
        ],
        name: [
            {required: true, message: '请输入角色名称'}
        ],
        key: [
            {required: true, message: '请输入权限字符'}
        ]
    }
    
    // 所需数据选项
    const groups = ref([])
    
    // 方法
    const handleOpen = (item = null,modeType = 'add') => {
        mode.value = modeType
        visible.value = true
        if(item){
            formData.value = deepClone(item)
        }
    }
    
    const submit = () => {
        dialogForm.value.validate(async (valid) => {
            if (valid) {
                isSaveing.value = true
                let apiObj = Api.apiSystemRoleAdd
                if(mode.value == "edit"){
                    apiObj = Api.apiSystemRoleEdit
                }
                const res = await apiObj(formData.value)
                isSaveing.value = false
                if(res.code == 2000) {
                    emits('refreshData')
                    visible.value = false
                    ElMessage.success("操作成功")
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