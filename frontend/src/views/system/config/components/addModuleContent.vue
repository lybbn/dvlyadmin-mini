<template>
    <div>
        <ly-dialog 
        v-model="dialogVisible" 
        :title="loadingTitle" 
        width="560px" 
        :before-close="handleClose"
        >
        <el-form 
            :inline="false" 
            :model="formData" 
            :rules="rules" 
            ref="formRef" 
            label-position="right" 
            label-width="auto"
        >
            <!-- 所属分组 -->
            <el-form-item label="所属分组" prop="parent">
                <el-select 
                    v-model="formData.parent" 
                    placeholder="请选择分组" 
                    clearable 
                    style="width: 100%"
                >
                    <el-option 
                    v-for="(item, index) in groupList"
                    :key="index"
                    :label="item.title"
                    :value="item.id"
                    />
                </el-select>
            </el-form-item>

            <!-- 标题 -->
            <el-form-item label="标题" prop="title">
                <el-input v-model="formData.title" placeholder="请输入" clearable />
            </el-form-item>

            <!-- key值 -->
            <el-form-item label="key值" prop="key">
                <el-input v-model="formData.key" placeholder="请输入" clearable />
            </el-form-item>

            <!-- 表单类型 -->
            <el-form-item label="表单类型" prop="form_item_type">
                <el-select 
                    v-model="formData.form_item_type" 
                    placeholder="请选择" 
                    clearable 
                    style="width: 100%"
                >
                    <el-option 
                    v-for="(item, index) in formTypeList"
                    :key="index"
                    :label="item.name"
                    :value="item.id"
                    />
                </el-select>
            </el-form-item>

            <!-- 选项字典 (仅当表单类型为checkbox或radio时显示) -->
            <el-form-item 
            label="选项字典" 
            prop="data_options" 
            v-if="[5, 6].includes(formData.form_item_type)"
            >
                <el-input 
                    v-model="formData.data_options" 
                    type="textarea" 
                    :rows="2" 
                    placeholder="请输入如[{'label':'启用','value':'1'},{'label':'禁用','value':'0'}]" 
                />
            </el-form-item>

            <!-- 校验规则 (隐藏) -->
            <el-form-item label="校验规则" v-show="false">
                <el-select 
                    v-model="formData.rule" 
                    multiple 
                    placeholder="请选择(可多选)" 
                    clearable 
                    style="width: 100%"
                >
                    <el-option 
                    v-for="(item, index) in ruleOptions"
                    :key="index"
                    :label="item.label"
                    :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <!-- 提示信息 -->
            <el-form-item label="提示信息" prop="placeholder">
                <el-input v-model="formData.placeholder" placeholder="请输入" clearable />
            </el-form-item>

            <!-- 底部说明 -->
            <el-form-item label="底部说明" prop="tip">
                <el-input v-model="formData.tip" placeholder="为空则不显示" clearable />
            </el-form-item>

            <!-- 排序 -->
            <el-form-item label="排序" prop="sort">
                <el-input-number v-model="formData.sort" :min="0" :max="999" />
            </el-form-item>
        </el-form>

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

    // 定义组件发射的事件
    const emit = defineEmits(['refreshData'])

    const dialogVisible = ref(false)
    const loadingSave = ref(false)
    const loadingTitle = ref('')
    const formRef = ref(null)

    // 表单数据
    const formData = ref({
        parent: null,
        title: null,
        key: null,
        form_item_type: null,
        rule: null,
        placeholder: null,
        data_options: null,
        tip: null,
        sort: 0
    })

    // 表单验证规则
    const rules = {
        title: [
            { required: true, message: '请输入分组名称', trigger: 'blur' }
        ],
        key: [
            { required: true, message: '请输入key值', trigger: 'blur' }
        ],
        form_item_type: [
            { required: true, message: '请选择表单类型', trigger: 'blur' }
        ]
    }

    // 分组列表
    const groupList = ref([])

    // 校验规则选项
    const ruleOptions = ref([
        {
            label: '必填项',
            value: '{"required": true, "message": "必填项不能为空"}'
        },
        {
            label: '邮箱',
            value: '{ "type": "email", "message": "请输入正确的邮箱地址"}'
        },
        {
            label: 'URL地址',
            value: '{ "type": "url", "message": "请输入正确的URL地址"}'
        },
        {
            label: '数字',
            value: '{"type": "number", "message": "请输入正确的数字"}'
        }
    ])

    // 表单类型列表
    const formTypeList = ref([
        {id:0, name:"text"},
        {id:3, name:"textarea"},
        {id:5, name:"checkbox"},
        {id:6, name:"radio"},
        {id:7, name:"image"},
        {id:8, name:"singlefile"},
        {id:9, name:"switch"},
        {id:10, name:"number"},
        {id:14, name:"richtext"},
    ])

    // 完整表单类型列表
    const formTypeList2 = ref([
        {id:0, name:"text"},
        {id:1, name:"datetime"},
        {id:2, name:"date"},
        {id:3, name:"textarea"},
        {id:4, name:"select"},
        {id:5, name:"checkbox"},
        {id:6, name:"radio"},
        {id:7, name:"image"},
        {id:8, name:"file"},
        {id:9, name:"switch"},
        {id:10, name:"number"},
        {id:11, name:"array"},
        {id:12, name:"images"},
        {id:13, name:"time"},
        {id:14, name:"richtext"},
    ])

    /**
     * 关闭对话框处理
     */
    const handleClose = () => {
        dialogVisible.value = false
        loadingSave.value = false
        // 重置表单数据
        formData.value = {
            parent: null,
            title: null,
            key: null,
            form_item_type: null,
            rule: null,
            placeholder: null,
            data_options: null,
            tip: null,
            sort: 0
        }
    }

    /**
     * 获取分组列表
     */
    const getGroups = async () => {
        try {
            const res = await Api.platformsettingsSysconfig({ limit: 999, parent__isnull: true })
            if (res.code === 2000) {
                groupList.value = res.data.data
            }
        } catch (error) {
            console.error('获取分组列表失败:', error)
        }
    }

    /**
     * 初始化数据
     */
    const getData = () => {
        getGroups()
    }

    /**
     * 打开对话框方法
     * @param {Object} item - 编辑时的数据对象
     * @param {String} flag - 对话框标题
     */
    const addModuleFn = (item, flag) => {
        loadingTitle.value = flag
        dialogVisible.value = true
        // 如果是编辑模式，填充表单数据
        if (item) {
            formData.value = deepClone(item)
        }
        getData()
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
                // 触发父组件刷新数据
                const targetItem = groupList.value.find(item => item.id === formData.value.parent);
                emit('refreshData',targetItem)
                handleClose()
            } else {
                ElMessage.warning(res.msg)
            }
        } catch (error) {
            console.error('表单提交错误:', error)
            ElMessage.error('操作失败')
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