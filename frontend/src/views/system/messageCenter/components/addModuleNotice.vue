<template>
    <div>
        <ly-dialog v-model="dialogVisible" :title="titleMap[mode]" width="50%" @closed="emits('closed')">
            <el-form :inline="false" :model="formData" :rules="rules" ref="rulesForm" label-position="right" label-width="auto" :disabled="mode == 'detail'">
                <el-form-item label="消息标题" prop="title">
                    <el-input type="text" v-model.trim="formData.title"></el-input>
                </el-form-item>
                <el-form-item label="目标类型" prop="target_type" v-if="!isUserOwnMsg">
                    <el-radio-group v-model="formData.target_type">
                        <el-radio :value="0" border>平台公告</el-radio>
                        <el-radio :value="1" border>按用户</el-radio>
                        <!-- <el-radio :value="2" border>按部门</el-radio>
                        <el-radio :value="3" border>按角色</el-radio> -->
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="发送对象" prop="users" v-if="formData.target_type == 1 && !isUserOwnMsg" class="is-required">
                    <ly-table-select v-model="formData.users" :apiObj="Api.apiSystemUser" multiple clearable collapse-tags collapse-tags-tooltip :props="tableSelectProps">
                        <template #header="{form, submit}">
                            <el-form :inline="true" :model="form">
                                <el-form-item>
                                    <el-input type="text" v-model="form.username" placeholder="请输入用户名"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="primary" @click="submit">查询</el-button>
                                </el-form-item>
                            </el-form>
                        </template>
                        <!-- <el-table-column prop="id" label="ID" width="100" show-overflow-tooltip></el-table-column> -->
                        <el-table-column prop="username" label="用户名" min-width="100" show-overflow-tooltip></el-table-column>
                        <el-table-column prop="nickname" label="昵称" min-width="100"></el-table-column>
                        <el-table-column prop="mobile" label="手机号" min-width="150"></el-table-column>
                        <!-- <el-table-column prop="create_datetime" label="注册时间" min-width="160"></el-table-column> -->
                    </ly-table-select>
                </el-form-item>
                <el-form-item label="消息内容" prop="content">
                    <RichTextEditor v-model="formData.content" :readOnly="mode == 'detail'"></RichTextEditor>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="handleClose" :loading="loadingSave">取消</el-button>
                <el-button type="primary" @click="submitData" :loading="loadingSave" v-if="mode != 'detail'">确定</el-button>
            </template>
        </ly-dialog>
    </div>
</template>

<script setup>
    import { ref, onMounted, onUnmounted } from 'vue'
    import { ElMessage, ElMessageBox } from 'element-plus'
    import Api from "@/api/api"
    import RichTextEditor from '@/components/editor/wangEditor.vue'
    import LyDialog from "@/components/dialog/dialog.vue"
    import { deepClone } from "@/utils/util"
    import LyTableSelect from "@/components/lyTableSelect.vue";

    // 定义emit事件
    const emits = defineEmits(['refreshData', 'closed'])

    // 响应式数据
    const dialogVisible = ref(false)
    const loadingSave = ref(false)
    const loadingTitle = ref('')
    const rulesForm = ref(null)

    let isUserOwnMsg = ref(false)
    let mode = ref("add")
    const titleMap = {
        add: '新增',
        edit: '编辑',
        detail: '详情'
    }

    const formData = ref({
        title: '',
        content: '',
        target_type: 0,
        users: [],
    })

    const rules = ref({
        title: [
            { required: true, message: '请填写公告标题', trigger: 'blur' }
        ],
        content: [
            { required: true, message: '请填写公告内容', trigger: 'blur' }
        ]
    })

    const tableSelectProps = ref({
        label: 'username',
        value: 'id'
    })

    // 方法定义
    const onFocusIn = (e) => {
        e.stopImmediatePropagation() // 阻止当前和后面的一系列事件
    }

    const handleClose = () => {
        dialogVisible.value = false
        loadingSave.value = false
        formData.value = {
            msg_title: '',
            to_path: '',
            msg_content: '',
            target_type: 1,
            target_user: [],
            status: true
        }
    }

    const addModuleFn = (item, modeType = 'add') => {
        mode.value = modeType
        dialogVisible.value = true
        if (item) {
            formData.value = deepClone(item)
        }
    }

    function readMsg(){
        Api.readOwnMessage({id:formData.value.id}).then(res => {
            if(res.code ==2000) {
            }else{
                ElMessage.warning(res.msg)
            }
        })
    }

    const submitData = () => {
        rulesForm.value.validate((valid) => {
            if (valid) {
                loadingSave.value = true
                const param = {
                    ...formData.value
                }
                
                // 处理表单组件返回的选中数据(去除杂数据)为id数组['1','2']
                if (param.users.length > 0) {
                    param.users = param.users.map(item => item.id)
                }
                
                const apiCall = param.id ? Api.messagesMessagenoticeEdit : Api.messagesMessagenoticeAdd
                
                apiCall(param).then(res => {
                    loadingSave.value = false
                    if (res.code == 2000) {
                        ElMessage.success(res.msg)
                        emits('refreshData')
                        handleClose()
                    } else {
                        ElMessage.warning(res.msg)
                    }
                })
            }
        })
    }

    // 生命周期钩子
    onMounted(() => {
        window.addEventListener("focusin", onFocusIn, true)
    })

    onUnmounted(() => {
        window.removeEventListener("focusin", onFocusIn)
    })

    // 暴露方法给父组件
    defineExpose({
        addModuleFn,
        readMsg,
        isUserOwnMsg
    })
</script>

<style scoped>
    .set-specs .el-form-item__content {
        background: #e6e6e6 !important;
    }
</style>