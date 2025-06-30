<template>
    <ly-dialog :title="titleMap[mode]" v-model="visible" width="500px" destroy-on-close @closed="emits('closed')">
        <el-form :model="formData" :rules="rules" :disabled="mode=='detail'" ref="dialogForm" label-width="auto">
            <el-form-item label="上级部门" prop="parent">
                <el-tree-select v-model="formData.parent" node-key="id" :data="groups" default-expand-all
                                check-strictly filterable clearable :render-after-expand="false"
                                :props="{label:'name',value: 'id'}"
                                style="width: 100%" placeholder="请选择/为空则为顶级" >
                    <template #default="{ data: { name,sort } }">
                        {{ name }}
                    </template>
                </el-tree-select>
            </el-form-item>
            <el-form-item label="部门名称" prop="name">
                <el-input v-model="formData.name" placeholder="请输入部门名称" clearable></el-input>
            </el-form-item>
            <el-form-item label="标识字符" prop="key">
                <el-input v-model="formData.key" placeholder="请输入标识字符" clearable></el-input>
            </el-form-item>
            <el-form-item label="负责人" prop="owner">
                <el-input v-model="formData.owner" placeholder="请输入负责人" clearable></el-input>
            </el-form-item>
            
            <!-- <el-form-item label="联系电话" prop="phone">
                <el-input v-model="formData.phone" placeholder="请输入联系电话" clearable></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="formData.email" placeholder="请输入邮箱" clearable></el-input>
            </el-form-item> -->
            <el-form-item label="排序" prop="sort">
                <el-input-number v-model="formData.sort" controls-position="right" :min="1" style="width: 100%;"></el-input-number>
            </el-form-item>
            <el-form-item label="状态" prop="status">
                <el-switch v-model="formData.status" inline-prompt active-text="启用" inactive-text="禁用"></el-switch>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="visible=false">取 消</el-button>
            <el-button v-if="mode!='detail'" type="primary" :loading="isSaveing" @click="submit()">保 存</el-button>
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
    import { createCrudConfig } from '../crud.js'

    const emits = defineEmits(['refreshData', 'closed'])

    let crudOptions = ref(createCrudConfig().crudOptions)

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
        parent: "",
        name: "",
        sort: 1,
        email:"",
        owner:"",
        phone:"",
        status: true,
    })
    
    // 验证规则
    let rules = {
        sort: [{required: true, message: '请输入排序', trigger: 'change'}],
        name: [{required: true, message: '请输入部门名称'}],
        key: [{ required: true, message: '请输入标识字符', trigger: 'blur' }],
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
    
    const getGroup = async () => {
        crudOptions.value.request.list({page:1,limit:999,status:1}).then(res=>{
            if(res.code === 2000){
                groups.value = XEUtils.toArrayTree(res.data.data, { parentKey: 'parent', strict: false })
            }
        })
    }
    
    const submit = () => {
        dialogForm.value.validate(async (valid) => {
            if (valid) {
                isSaveing.value = true
                let apiObj = crudOptions.value.request.add
                if(mode.value == "edit"){
                    apiObj = crudOptions.value.request.edit
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
        getGroup()
    })

    defineExpose({
        handleOpen
    })
</script>

<style>
</style>