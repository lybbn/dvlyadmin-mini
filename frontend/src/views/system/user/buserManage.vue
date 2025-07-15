<template>
    <div :class="{'ly-is-full':isFull}" class="lycontainer">
        <div class="lycontainer-wrapper">
            <el-card shadow="hover" class="ly-aside" v-loading="showDeptloading">
                <el-container>
                    <el-header>
                        <el-input placeholder="输入关键字" v-model="groupFilterText" clearable style="width:180px;" @change="handelFilterDept">
                            <template #append>
                                <el-button icon="Search" @click="handelFilterDept"/>
                            </template>
                        </el-input>
                    </el-header>
                    <el-main class="nopadding">
                        <el-tree ref="groupRef" node-key="id" default-expand-all :props="{ label: 'name',children: 'children'}" :data="deptOptions" :current-node-key="''" :highlight-current="true" :expand-on-click-node="false" :filter-node-method="groupFilterNode" @node-click="groupClick"></el-tree>
                    </el-main>
                </el-container>
            </el-card>
            <div class="lycontainer-right">
                <el-card class="tableSelect" ref="tableSelect" shadow="hover" v-if="crudOptions.searchBar.showSearchBar">
                    <lySearchBar :model="formInline" @search="search" @reset="handleEdit('','reset')">
                        <!-- 自定义默认搜索项 -->
                        <template #default>
                            <el-form-item label="账号">
                                <el-input v-model.trim="formInline.username" maxlength="60" clearable style="width:120px" placeholder="账号"></el-input>
                            </el-form-item>
                            <el-form-item label="姓名">
                                <el-input v-model.trim="formInline.name" maxlength="60" clearable style="width:120px" placeholder="姓名"></el-input>
                            </el-form-item>
                            <el-form-item label="状态">
                                <el-select v-model="formInline.is_active" placeholder="请选择" clearable style="width: 120px">
                                    <el-option
                                            v-for="item in statusList"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id">
                                    </el-option>
                                </el-select>
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
                        <template #avatar="scope">
                            <ly-image  :src="scope.row.avatar ? scope.row.avatar : defaultAvatar" :preview-src-list="[scope.row.avatar]" style="width: 30px;height: 30px" preview-teleported v-if="scope.row.avatar"></ly-image>
                        </template>
                        <template #dept="scope">
                            <el-tag v-if="!!scope.row.deptName">{{scope.row.deptName}}</el-tag>
                        </template>
                        <template #role="scope">
                            <el-tag v-for="(item,index) in scope.row.roleNames" :key="index" v-if="!isEmpty(scope.row.roleNames)">{{item}}</el-tag>
                        </template>
                        <template #is_active="scope">
                            <el-switch v-model="scope.row.is_active" active-color="#13ce66" inactive-color="#ff4949" @change="changeStatus(scope.row)" :disabled="!hasBtnPermission('SetStatus')"></el-switch>
                        </template>
                        <el-table-column label="操作" :fixed="crudOptions.rowHandle.fixed" :width="crudOptions.rowHandle.width">
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
                                <span class="table-operate-btn" @click="handleEdit(scope.row,'resetpass')" v-auth="'ResetPass'">重置密码</span>
                            </template>
                        </el-table-column>
                    </ly-table>
                </el-card>
            </div>
        </div>
        <saveDialog ref="saveDialogRef" @refreshData="getData" v-if="isDialogVisible" @closed="isDialogVisible = false"></saveDialog>
        <passDialog ref="passDialogRef" v-if="isDialogPassVisible" @closed="isDialogPassVisible = false"></passDialog>
    </div>
</template>

<script setup name="buserManage">
    import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
    import { ElMessage, ElMessageBox } from 'element-plus'
    import saveDialog from "./components/moduleSave.vue"
    import passDialog from "./components/modulePass.vue"
    import lySearchBar from '@/components/lySearchBar.vue'
    import { createCrudConfig } from './crud.js'
    import { useUserState } from '@/store/userState' 
    import { useRoute } from 'vue-router'
    import Api from '@/api/api.js'
    import XEUtils from 'xe-utils'
    import defaultAvatar from '@/assets/lybbn/imgs/avatar.jpg'
    import {isEmpty} from "@/utils/util.js"

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
    let isDialogPassVisible = ref(false)
    let passDialogRef = ref(null)

    let showDeptloading = ref(false)
    let groupFilterText = ref("")
    let deptOptions = ref([])

    let statusList = [
        {id:1,name:'正常'},
        {id:0,name:'禁用'}
    ]

    function selectionChange(selections){
        selection.value = selections;
    }

    let tableBindProps= computed(() => (
        {
            ...crudOptions.value.table,
            ...crudOptions.value.pagination,
            apiObj:crudOptions.value.request.list,
            apiImportObj:crudOptions.value.request.import,
            apiExportObj:crudOptions.value.request.export,
            apiTemplateObj:crudOptions.value.request.dltemplate,
            params:formInline.value,
            column:crudOptions.value.columns,
            hideExport:!hasBtnPermission('Export'),
            hideImport:!hasBtnPermission('Import'),
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

    const handleResetPassClick = (item) => {
        isDialogPassVisible.value = true
        nextTick(() => {
            passDialogRef.value.handleOpen(item)
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
            case 'resetpass':
                handleResetPassClick(row)
                break
            case 'reset':
                formInline.value = {}
                search()
                break
        }
    }

    const changeStatus = (row) => {
        let originalStatus = row.is_active
        row.is_active = !row.is_active
        
        ElMessageBox.confirm('确定修改状态吗？', '提醒', {
            closeOnClickModal: false,
            type: "warning"
        }).then(() => {
            crudOptions.value.request.setStatus({ id: row.id }).then(res => {
                if (res.code == 2000) {
                    originalStatus ? row.status = true : row.is_active = false
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

    const fetchDeptData = async () => {
        try {
            showDeptloading.value = true
            const res = await Api.apiSystemDept({ page: 1, limit: 9999 })
            // 处理部门数据为树形结构
            deptOptions.value = XEUtils.toArrayTree(res.data.data,{ parentKey: 'parent', strict: false })
        } catch (error) {
            ElMessage.error('获取部门数据失败')
        }
        showDeptloading.value = false
    }

    let groupRef = ref(null)
    function handelFilterDept(){
        groupRef.value.filter(groupFilterText.value)
    }   
    //树过滤
    const groupFilterNode = (value, data) => {
        if (!value) return true
        return data.name.toLowerCase().includes(value.toLowerCase())
    }

    //树点击事件
    function groupClick(data){
        var params = {
            dept_id: data.id
        }
        tableref.value.reload(params)
    }

    onMounted(() => {
        fetchDeptData()
    })

    onUnmounted(() => {
    })
</script>

<style lang="scss" scoped>
.lycontainer {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
}

.lycontainer-wrapper {
    display: flex;
    flex: 1;
    overflow-x: hidden;
    flex-direction: row;
    gap: 10px;
}

.ly-aside {
    transition: all 0.3s;
    overflow: auto;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    width: 210px;
    :deep(.el-card__body){
        padding:0 !important;
    }
}

.lycontainer-right {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: auto;
}

.tableSelect {
    margin-bottom: 10px;
}


/* 移动端适配 */
@media screen and (max-width: 768px) {
    .lycontainer-wrapper {
        flex-direction: column;
    }
    
    .ly-aside {
        width: 100% !important;
        :deep(.el-select) {
            width: 100% !important;
        }
        :deep(.el-input) {
            width: 100% !important;
        }
    }
    
    .lycontainer-right {
        padding: 0;
    }
    
    .el-form-item {
        margin-bottom: 10px;
    }
    
    
}

.nopadding {
    padding: 0;
}

.table-operate-btn {
    color: var(--el-color-primary);
    cursor: pointer;
    margin-right: 10px;
}

.table-operate-btn.delete {
    color: var(--el-color-danger);
}
</style>