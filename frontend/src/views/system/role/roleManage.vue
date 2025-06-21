<template>
    <div :class="{'ly-is-full':isFull}" class="lycontainer">
        <el-card class="tableSelect" ref="tableSelect" shadow="hover">
            <el-form :inline="true" :model="formInline" label-position="left">
                <el-form-item label="角色名称">
                    <el-input v-model.trim="formInline.name" maxlength="60"  clearable placeholder="角色名称" style="width:160px"></el-input>
                </el-form-item>
                <el-form-item label="">
                    <el-button  @click="search" type="primary" icon="Search" v-show="hasPermission(route.name,'Search')">查询</el-button>
                    <el-button  @click="handleEdit('','reset')" icon="Refresh">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>
        <el-card class="lytable" shadow="hover">
            <ly-table tableName="roleManageTable" showSelectable row-key="id" :defaultExpandAll="true" :pageSize="10" :is-tree="true" :apiObj="Api.apiSystemRole" :params="formInline" ref="tableref" :column="column" @selection-change="selectionChange" border>
                <template v-slot:topbar>
                    <el-button type="primary" icon="plus"  @click="handleAddClick" v-show="hasPermission(route.name,'Create')">新增</el-button>
                    <el-button type="danger" plain icon="delete" :disabled="selection.length==0" title="批量删除"  @click="batch_del"></el-button>
                </template>
                <template #status="scope">
                    <el-switch v-model="scope.row.status" active-color="#13ce66" inactive-color="#ff4949" @change="changeStatus(scope.row)"></el-switch>
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
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'edit')" v-show="hasPermission(route.name,'Update')">编辑</span>
                        <span class="table-operate-btn delete" @click="handleEdit(scope.row,'delete')" v-show="hasPermission(route.name,'Delete')">删除</span>
                    </template>
                </el-table-column>
            </ly-table>
        </el-card>
        <saveDialog ref="saveDialogRef" @refreshData="getData" v-if="isDialogVisible" @closed="isDialogVisible = false"></saveDialog>
    </div>
</template>

<script setup>
    import { ref, onMounted, onUnmounted, nextTick } from 'vue'
    import { useRoute } from 'vue-router'
    import { ElMessage, ElMessageBox } from 'element-plus'
    import { FullScreen } from '@element-plus/icons-vue'
    import Api from '@/api/api'
    import saveDialog from "./components/moduleSave.vue"

    const route = useRoute()

    // 状态管理
    const isFull = ref(false)
    const isDialogVisible = ref(false)
    const formInline = ref({})
    const timers = ref([])
    const tableSelect = ref(null)
    const tableref = ref(null)
    const saveDialogRef = ref(null)
    let selection = ref([])

    const statusList = [
        { id: 1, name: '正常' },
        { id: 0, name: '禁用' }
    ]

    const column = [
        {
            label: "角色名称",
            prop: "name",
            minWidth: "110"
        },
        {
            label: "权限字符",
            prop: "key",
            minWidth: "110"
        },
        {
            label: "状态",
            prop: "status",
            width: "100"
        },
        {
            label: "排序",
            prop: "sort",
            width: "100"
        },
        {
            label: "创建时间",
            prop: "create_datetime",
            minWidth: "180"
        }
    ]

    function selectionChange(selections){
        selection.value = selections;
    }

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
            Api.apiSystemRoleDelete({id:ids}).then(res=>{
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
                    Api.apiSystemRoleDelete({ id: row.id }).then(res => {
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
                timers.value = []
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
            Api.apiSystemRoleSetStatus({ id: row.id }).then(res => {
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

    // 权限检查函数
    const hasPermission = (routeName, action) => {
        // 实现你的权限检查逻辑
        return true
    }
</script>