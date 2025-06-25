<template>
    <div :class="{'ly-is-full':isFull}" class="lycontainer">
        <el-card class="tableSelect" ref="tableSelect" shadow="hover" v-if="crudOptions.searchBar.showSearchBar">
            <lySearchBar :model="formInline" @search="search" @reset="handleEdit('','reset')">
                <!-- 自定义默认搜索项 -->
                <template #default>
                    <el-form-item label="部门名称">
                        <el-input v-model.trim="formInline.name" maxlength="60" clearable style="width:160px" placeholder="部门名称"></el-input>
                    </el-form-item>
                </template>
            </lySearchBar>
        </el-card>
        <el-card class="lytable" shadow="hover">
            <ly-table v-bind="tableBindProps" ref="tableref" @selection-change="selectionChange">
                <template v-slot:topbar>
                    <el-button type="primary" icon="plus"  @click="handleAddClick" v-auth="'Create'">新增</el-button>
                    <el-button type="danger" plain icon="delete" :disabled="selection.length==0" title="批量删除" @click="batch_del" v-auth="'Delete'"></el-button>
                </template>
                <template #status="scope">
                    <el-switch v-model="scope.row.status" active-color="#13ce66" inactive-color="#ff4949" @change="changeStatus(scope.row)" :disabled="!hasBtnPermission('SetStatus')"></el-switch>
                </template>
                <el-table-column label="操作" fixed="right" width="150">
                    <template #header>
                        <div style="display: flex;justify-content: space-between;align-items: center;">
                            <div>操作</div>
                            <div @click="setFull">
                                <el-tooltip content="全屏" placement="bottom">
                                    <el-icon style="cursor: pointer;"><full-screen /></el-icon>
                                </el-tooltip>
                            </div>
                        </div>
                    </template>
                    <template #default="scope">
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'edit')" v-auth="'Update'">编辑</span>
                        <span class="table-operate-btn delete" @click="handleEdit(scope.row,'delete')" v-auth="'Delete'">删除</span>
                    </template>
                </el-table-column>
            </ly-table>
        </el-card>
        <saveDialog ref="saveDialogRef" @refreshData="getData" v-if="isDialogVisible" @closed="isDialogVisible = false"></saveDialog>
    </div>
</template>

<script setup name="deptManage">
    import { ref, onMounted, onUnmounted, nextTick,computed } from 'vue'
    import { ElMessage, ElMessageBox } from 'element-plus'
    import saveDialog from "./components/moduleSave.vue"
    import lySearchBar from '@/components/lySearchBar.vue'
    import { createCrudConfig } from './crud.js'
    import { useUserState } from '@/store/userState' 
    import { useRoute } from 'vue-router'

    const route = useRoute()
    const userState = useUserState()

    let crudOptions = ref(createCrudConfig().crudOptions)
    
    const hasBtnPermission = (btnCode) => {
        return userState.hasButtonPermission(route.name, btnCode)
    }

    // 状态管理
    const isFull = ref(false)
    const isDialogVisible = ref(false)
    const formInline = ref({})
    const tableSelect = ref(null)
    const tableref = ref(null)
    const saveDialogRef = ref(null)
    let selection = ref([])

    function selectionChange(selections){
        selection.value = selections;
    }

    let tableBindProps= computed(() => (
        {
            ...crudOptions.value.table,
            apiObj:crudOptions.value.request.list,
            apiImportObj:crudOptions.value.request.import,
            apiExportObj:crudOptions.value.request.export,
            apiTemplateObj:crudOptions.value.request.dltemplate,
            params:formInline.value,
            column:crudOptions.value.columns,
            hideExport:!hasBtnPermission('Export'),
            hideImport:!hasBtnPermission('Import')
        }
    ))

    // 方法
    const setFull = () => {
        isFull.value = !isFull.value
        window.dispatchEvent(new Event('resize'))
    }

    const handleAddClick = () => {
        isDialogVisible.value = true
        nextTick(() => {
            saveDialogRef.value.handleOpen(null, "add")
        })
    }

    function batch_del(){
        ElMessageBox.confirm(`确定删除选中的 ${selection.value.length} 项吗？`, '提示', {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: 'warning'
        }).then(() => {
            let ids = selection.value.map(item => item.id);
            crudOptions.value.request.del({id:ids}).then(res=>{
                if(res.code == 2000) {
                    search()
                    ElMessage.success("操作成功")
                } else {
                    ElMessage.warning(res.msg)
                }
            })
        }).catch(() => {

        })
    }

    const handleEdit = (row, flag) => {
        switch (flag) {
            case 'edit':
                isDialogVisible.value = true
                nextTick(() => {
                    saveDialogRef.value.handleOpen(row, "edit")
                })
                break
            case 'delete':
                ElMessageBox.confirm('您确定要删除选中的数据吗？', "警告", {
                    closeOnClickModal: false,
                    type: "warning",
                }).then(() => {
                    crudOptions.value.request.del({ id: row.id }).then(res => {
                    if (res.code == 2000) {
                        ElMessage.success(res.msg)
                        search()
                    } else {
                        ElMessage.warning(res.msg)
                    }
                    })
                }).catch(() => {})
                break
            case 'reset':
                formInline.value = {}
                search()
                break
        }
    }

    const changeStatus = (row) => {
        let originalStatus = row.status
        row.status = !row.status
        
        ElMessageBox.confirm('确定修改状态吗？', '提醒', {
            closeOnClickModal: false,
            type: "warning"
        }).then(() => {
            crudOptions.value.request.setStatus({ id: row.id }).then(res => {
                if (res.code == 2000) {
                    originalStatus ? row.status = true : row.status = false
                    ElMessage.success(res.msg)
                    getData()
                } else {
                    ElMessage.warning(res.msg)
                }
            })
        })
    }

    const search = () => {
        tableref.value.reload(formInline.value)
    }

    const getData = () => {
        tableref.value.getData()
    }

    onMounted(() => {
    })

    onUnmounted(() => {
    })
</script>