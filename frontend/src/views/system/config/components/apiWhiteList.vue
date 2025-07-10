<template>
    <div>
        <el-alert type="info" show-icon>请正确填写（后端config.py也有白名单配置，建议后端配置）,匹配使用正则,如:/api/xxx/{id}/</el-alert>
        <el-table :data="dataList" v-loading="loading" class="lyapitable">
            <template #empty>
                <el-empty></el-empty>
            </template>
            <!-- <el-table-column min-width="120" label="名称" prop="label"></el-table-column> -->
            <el-table-column min-width="150" label="Api地址" prop="api" show-overflow-tooltip></el-table-column>
            <el-table-column min-width="90" label="请求方法" prop="method">
                <template #default="{ row, $index }">
                    <el-tag :type="getMethodTagType(row.method)">{{ methodLabel(row.method) }}</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right" width="90">
                <template #header>
                    <div class="lycaozuol">
                        <span>操作</span>
                        <el-button circle  size="small"  type="primary" icon="Plus" @click="handleOpenCT"></el-button>
                    </div>
                </template>
                <template #default="{ row, $index }">
                    <div>
                        <el-popconfirm title="确定删除吗？" @confirm="handleDelete(row,$index )">
                            <template #reference>
                                <el-button link type="danger" v-auth="'systemConfig:Delete'">删除</el-button>
                            </template>
                        </el-popconfirm>
                    </div>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog v-model="dialogVisible" title="添加Api白名单" width="580px" :fullscreen="isMobile" :close-on-click-modal="false">
            <el-form ref="formRefb" :model="formData" :rules="apiRules" label-width="auto">
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="接口地址" prop="api">
                            <el-select  v-model.trim="formData.api" filterable clearable  allow-create style="margin-bottom: 5px;width: 100%;" placeholder="请选择或手动输入">
                                <el-option
                                    v-for="item in apiList"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                            <el-alert title="请正确填写(或选择)，匹配使用正则,如:/api/xxx/{id}/" type="info" show-icon/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="请求方法" prop="method">
                            <el-select v-model="formData.method" placeholder="请选择" style="width: 100%">
                                <el-option v-for="item in methodList" :label="item.label" :value="item.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="saveSubmit" :loading="isDialogLoading">提交</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
    import {ref, onMounted,computed, nextTick} from 'vue'
    import { useWindowSize } from '@vueuse/core'
    import Api from "@/api/api"
    import { ElMessage } from 'element-plus'
    import {deepClone} from '@/utils/util' 

    const emit = defineEmits(['refreshData'])

    const props = defineProps({
        options: {
            type: Object,
            default: () => ({})
        }
    })
    // 响应式窗口大小
    const { width } = useWindowSize()
    const isMobile = computed(() => width.value < 768)
    let loading = ref(false)
    let dataList =  computed(() => {
        if(props.options?.value){
            return props.options?.value
        }else{
            return []
        }
    })
    let apiList = ref([])
    let dialogVisible = ref(false)
    let formRefb = ref(null)
    let isDialogLoading = ref(false)
    let formData = ref({})
    let methodList = [
        {value:"GET",label:"GET"},
        {value:"POST",label:"POST"},
        {value:"PUT",label:"PUT"},
        {value:"DELETE",label:"DELETE"},
        {value:"OPTIONS",label:"OPTIONS"},
        {value:"ALL",label:"ALL"},
    ]
    let apiRules = {
        api: [
            {required: true, message: '请输入接口地址',trigger: 'blur'}
        ],
        method: [
            {required: true, message: '请选择接口方法',trigger: 'blur'}
        ],
    }

    function methodLabel(md) {
      const method = methodList.find(item => item.value === md);
      return method ? method.label : "未知方法";
    }

    function getMethodTagType(method) {
        switch (method) {
            case "GET": return 'success'
            case "POST": return 'primary'
            case "PUT": return 'warning'
            case "DELETE": return 'danger'
            default: return ''
        }
    }

    const handleDelete = async (row,index) => {
        let newData = dataList.value
        newData.splice(index, 1)
        loading.value=true
        let param = {
            id:props.options.id,
            value: convertToString(newData)
        }
        let apiObj = Api.platformsettingsSysconfigEdit
        apiObj(param).then(res=>{
            loading.value=false
            if (res.code === 2000) {
                ElMessage.success('删除成功')
            } else {
                ElMessage.warning(res.msg)
            }
        })

    }

    function handleOpenCT(){
        formData.value = {}
        dialogVisible.value = true
        getSchemeJson()
        nextTick(()=>{
            formRefb.value.resetFields()
        })
    }

    function getSchemeJson(){
        Api.apiSchemeJson().then(res=>{
            var result = Object.keys(res.paths)
            var data = []
            for (const item of result) {
                const obj = {}
                obj.label = item
                obj.value = item
                data.push(obj)
            }
            apiList.value = data
        })
    }

    function convertToString(val){
        if(val == undefined || val == null || typeof val !== 'object'){
            return ""
        }
        if (!Array.isArray(val)) {
            return ""
        }
        if (val.length > 0 && typeof val[0] !== 'object') {
            return ""
        }
        return JSON.stringify(val);
    }

    async function saveSubmit(){
        try {
            await formRefb.value.validate()
            isDialogLoading.value=true
            let newdatalist = [...dataList.value,formData.value]
            let param = {
                id:props.options.id,
                value: convertToString(newdatalist)
            }
            let apiObj = Api.platformsettingsSysconfigEdit
            apiObj(param).then(res=>{
                isDialogLoading.value=false
                if (res.code === 2000) {
                    ElMessage.success('保存成功')
                    dialogVisible.value = false
                    emit("refreshData")
                } else {
                    ElMessage.warning(res.msg)
                }
            })
            
        } catch (error) {
            // console.log('表单验证失败！', error)
            return
        }
    }

    onMounted(() => {
    })

</script>

<style lang="scss" scoped>
    .lycaozuol{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .lyapitable{
        width: 100%;
        overflow-x: auto;
        :deep(.is-vertical) {
            display: none !important;
        }
    }
</style>