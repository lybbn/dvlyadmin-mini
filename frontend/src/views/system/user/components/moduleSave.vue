<template>
    <ly-dialog :title="titleMap[mode]" v-model="visible" width="50%" destroy-on-close @closed="emits('closed')">
        <el-form :model="formData" :rules="rules" :disabled="mode=='detail'" ref="dialogForm" label-width="auto">
            <el-row :gutter="20">
                <el-col :span="12">
                    <el-form-item label="用户账号" prop="username">
                        <el-input v-model="formData.username" placeholder="请输入用户账号" clearable></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="用户姓名" prop="name">
                        <el-input v-model="formData.name" placeholder="请输入用户姓名" clearable></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12" v-if="mode=='add'">
                    <el-form-item label="登录密码" prop="password" :rules="mode=='add'?loginpassword:[]">
                        <el-input v-model.trim="formData.password" clearable show-password placeholder="请输入登录密码"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="用户角色" prop="role">
                        <el-select v-model="formData.role" multiple filterable clearable placeholder="请选择角色" style="width:100%">
                            <el-option
                                v-for="item in rolelist"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                            />
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="所属部门" prop="dept">
                        <el-tree-select v-model="formData.dept" node-key="id" :data="deptList" default-expand-all
                                        check-strictly filterable clearable :render-after-expand="false"
                                        :props="{label:'name',value: 'id'}"
                                        style="width: 100%" placeholder="请选择部门" >
                            <template #default="{ data: { name,sort } }">
                                {{ name }}
                            </template>
                        </el-tree-select>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="用户电话" prop="mobile">
                        <el-input v-model="formData.mobile" placeholder="请输入用户电话" clearable></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="用户邮箱" prop="email">
                        <el-input v-model="formData.email" placeholder="请输入用户邮箱" clearable></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="用户性别" prop="gender">
                       <el-radio-group v-model="formData.gender">
                            <el-radio-button v-for="gl in genderList" :key="gl.id" :value="gl.id">
                                {{ gl.name }}
                            </el-radio-button>
                        </el-radio-group>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="用户状态" prop="status">
                        <el-switch v-model="formData.status" inline-prompt active-text="启用" inactive-text="禁用"></el-switch>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="用户头像" prop="status">
                        <pictureSingleUpload ref="lyfieldEditor" v-model="formData.avatar"
                               :disabled="false" :round="false" :cropper="true"
                               title="" :show-file-list="false"
                               :width="90" :height="90"></pictureSingleUpload>
                    </el-form-item>
                </el-col>
            </el-row>
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
    import {deepClone,safeDelete} from "@/utils/util.js"
    import Api from "@/api/api.js"
    import { ElMessage, ElMessageBox } from 'element-plus'
    import XEUtils from "xe-utils";
    import { createCrudConfig } from '../crud.js'
    import pictureSingleUpload from '@/components/upload/single-picture.vue'

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

    let rolelist = ref([])
    
    // 表单数据
    let formData = ref({
        avatar:"",
        dept: "",
        name: "",
        sort: 1,
        email:"",
        mobile:"",
        gender:2,
        password:"",
        status: true,
    })

    let loginpassword = [{required: true, message: '请输入密码',trigger: 'blur'}]
    
    // 验证规则
    let rules = {
        username: [{required: true, message: '请输入用户账号', trigger: 'change'}],
        name: [{required: true, message: '请输入用户姓名', trigger: 'blur' }],
        dept: [{ required: true, message: '请选择所属部门', trigger: 'blur' }],
    }
    
    // 所需数据选项()
    const deptList = ref([])

    let genderList = [
        {id:2,name:"男"},
        {id:1,name:"女"},
        {id:0,name:"未知"},
    ]
    
    // 方法
    const handleOpen = (item = null,modeType = 'add') => {
        mode.value = modeType
        visible.value = true
        if(item){
            formData.value = deepClone(item)
        }
    }
    
    const getGroup = async () => {
        Api.apiSystemDept({page:1,limit:999,status:1}).then(res=>{
            if(res.code === 2000){
                deptList.value = XEUtils.toArrayTree(res.data.data, { parentKey: 'parent', strict: false })
            }
        })
    }

    function getapiSystemRole(){
        Api.apiSystemRole({page:1,limit:999,status:1}).then(res=>{
            if(res.code ==2000) {
                rolelist.value = res.data.data
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
                    safeDelete(formData.value,'password')
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
        getapiSystemRole()
    })

    defineExpose({
        handleOpen
    })
</script>

<style>
</style>