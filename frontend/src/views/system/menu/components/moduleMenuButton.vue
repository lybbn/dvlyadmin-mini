<template>
    <div>
        <ly-dialog v-model="dialogVisible" :title="loadingTitle" width="560px" :before-close="handleClose" :showFullScreen="false">
            <el-form :inline="false" :model="formData" :rules="rules" ref="rulesForm" label-position="right" label-width="auto">
                <el-form-item label="按钮名称" prop="name">
                    <el-input v-model="formData.name" clearable placeholder="请输入按钮名称"></el-input>
                </el-form-item>
                <el-form-item label="权限值" prop="value">
                    <el-input v-model="formData.value" clearable placeholder="请输入权限值"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="handleClose" :loading="loadingSave">取消</el-button>
                <el-button type="primary" @click="submitData" :loading="loadingSave">保存</el-button>
            </template>
        </ly-dialog>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import Api from "@/api/api";
    import LyDialog from "@/components/dialog/dialog.vue";
    import { ElMessage } from 'element-plus'
    import { deepClone } from "@/utils/util"

    const emits = defineEmits(['refreshData','closed'])

    let dialogVisible = ref(false)
    let loadingSave = ref(false)
    let loadingTitle = ref('')
    let formData = ref({
        name:'',
        value:''
    })

    let rules = ref({
        name: [
            {required: true, message: '请输入按钮名称',trigger: 'blur'}
        ],
        value: [
            {required: true, message: '请输入权限值',trigger: 'blur'}
        ],
    })

    function handleClose() {
        emits('closed')
    }

    function handleOpen(item,flag) {
        loadingTitle.value=flag
        dialogVisible.value=true
        if(item){
            formData.value = deepClone(item)
        }
    }

    let rulesForm = ref(null)
    function submitData() {
        rulesForm.value.validate(obj=>{
            if(obj) {
                loadingSave.value=true
                let param = {
                    ...formData.value
                }
                if(formData.value.id){
                    Api.apiSystemButtonTemplateEdit(param).then(res=>{
                        loadingSave.value=false
                        if(res.code ==2000) {
                            ElMessage.success(res.msg)
                            handleClose()
                            emits('refreshData')
                        } else {
                            ElMessage.warning(res.msg)
                        }
                    })
                }else{
                    Api.apiSystemButtonTemplateAdd(param).then(res=>{
                        loadingSave.value=false
                        if(res.code ==2000) {
                            ElMessage.success(res.msg)
                            handleClose()
                            emits('refreshData')
                        } else {
                            ElMessage.warning(res.msg)
                        }
                    })
                }

            }
        })
    }


    defineExpose({
        handleOpen
    })
</script>