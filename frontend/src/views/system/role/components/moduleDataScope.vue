<template>
    <ly-dialog :title="titleMap[mode]" v-model="visible" width="500px" destroy-on-close @closed="emits('closed')">
        <el-form :model="formData" :rules="rules" :disabled="mode=='detail'" ref="dialogForm" label-width="auto">
            <el-form-item label="" prop="data_scope">
                <el-select v-model="formData.data_scope" @change="dataScopeSelectChange">
                    <el-option
                        v-for="item in dataScopeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
            <el-form-item label="" prop="dept" v-if="formData.data_scope == 3">
                <el-tree-select
                    node-key="id"
                    v-model="formData.dept"
                    :props="defaultTreeProps"
                    :data="deptData"
                    multiple
                    check-strictly
                    :render-after-expand="false"
                    show-checkbox
                />
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="visible=false">取 消</el-button>
            <el-button type="primary" :loading="isSaveing" @click="submit()">确 认</el-button>
        </template>
    </ly-dialog>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import lyDialog from "@/components/dialog/dialog.vue"
    import {deepClone,isEmpty} from "@/utils/util.js"
    import { ElMessage, ElMessageBox } from 'element-plus'
    import Api from "@/api/api.js"
    import XEUtils from "xe-utils";

    const emits = defineEmits(['refreshData', 'closed'])

    let mode = ref("now")
    const titleMap = {
        now:'数据权限配置',
        add: '新增',
        edit: '编辑',
        detail: '查看'
    }
    let visible = ref(false)
    let isSaveing = ref(false)
    let dialogForm = ref(null)
    let deptData = ref([])

    const fetchDeptData = async () => {
        try {
            const res = await Api.apiSystemDept({ page: 1, limit: 9999 })
            // 处理部门数据为树形结构
            deptData.value = XEUtils.toArrayTree(
            res.data.data.map(item => ({ ...item, disabled: false })),
            { parentKey: 'parent', strict: false }
            )
        } catch (error) {
            ElMessage.error('获取部门数据失败')
        }
    }

    const dataScopeOptions = [
        { value: 0, label: '仅本人数据权限' },
        { value: 1, label: '本部门数据权限' },
        { value: 2, label: '本部门及以下' },
        { value: 3, label: '自定义部门数据权限' },
        { value: 4, label: '全部数据权限' },
        { value: 5, label: '同全局数据权限' }
    ]

    const defaultTreeProps = {
        children: 'children',
        label: 'name',
        value: 'id',
    };
    
    // 表单数据
    let formData = ref({
        data_scope: 5,
        dept: [],
    })

    const dataScopeSelectChange = (value) => {
        if (value !== 3) {
            formData.value.dept = []
        }
    }
    
    // 验证规则
    let rules = {
        data_scope: [
            {required: true, message: '请选择数据权限', trigger: 'change'}
        ],
    }
    
    // 方法
    const handleOpen = (item = null) => {
        visible.value = true
        fetchDeptData()
        if(item){
            formData.value = deepClone(item)
            if(isEmpty(formData.value.data_scope)){
                formData.value.data_scope = 5
            }
        }
    }
    
    const submit = () => {
        dialogForm.value.validate(async (valid) => {
            if (valid) {
                emits('refreshData',formData.value)
                visible.value = false
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