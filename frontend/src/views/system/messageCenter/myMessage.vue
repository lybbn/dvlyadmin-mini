<template>
    <div :class="['message-manage-container', { 'ly-is-full': isFull }]">
        <el-card class="tableSelect" ref="tableSelect" shadow="hover">
            <lySearchBar :model="formInline" @search="search" @reset="handleEdit('','reset')">
                <!-- <template #actions-right>
                    <el-button icon="Plus" @click="addModule" type="primary" v-auth="'Create'">新增</el-button>
                </template> -->
                <!-- 自定义默认搜索项 -->
                <template #default>
                    <el-form-item label="关键词">
                        <el-input
                            v-model.trim="formInline.search"
                            maxlength="60"
                            clearable
                            placeholder="消息标题、内容"
                            style="width:160px"
                        />
                    </el-form-item>
                    <el-form-item label="状态">
                        <el-select v-model="formInline.is_read" placeholder="请选择" clearable style="width: 120px">
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
        <div class="table-container">
            <el-table  border :data="tableData" ref="tableref" style="width: 100%;height:100%;" v-loading="loadingPage">
                <el-table-column type="index" width="60" align="center" label="序号">
                    <template #default="scope">
                        <span v-text="getIndex(scope.$index)"></span>
                    </template>
                </el-table-column>
                <el-table-column min-width="150" prop="notification.title" label="标题" show-overflow-tooltip></el-table-column>
                <el-table-column min-width="200" prop="notification.content" show-overflow-tooltip label="内容">
                    <template #default="scope">
                        <div v-html="customEllipsis(scope.row.notification.content)" class="ellipsis"></div>
                </template>
                </el-table-column>
                <el-table-column min-width="100" label="目标类型">
                    <template #default="scope">
                        <el-tag v-if="scope.row.notification.target_type == 0">平台公告</el-tag>
                        <el-tag v-else-if="scope.notification.row.target_type == 1" type="primary">按用户</el-tag>
                        <el-tag v-else-if="scope.notification.row.target_type == 2" type="primary">按部门</el-tag>
                        <el-tag v-else-if="scope.notification.row.target_type == 3" type="primary">按角色</el-tag>
                    </template>
                </el-table-column>
                <el-table-column min-width="90" label="是否已读">
                    <template #default="scope">
                        <el-tag v-if="scope.row.is_read">已读</el-tag>
                        <el-tag v-else type="danger">未读</el-tag>
                    </template>
                </el-table-column>
                <el-table-column min-width="150" prop="notification.create_datetime" label="创建时间"></el-table-column>
                <el-table-column label="操作" fixed="right" width="180">
                    <template #header>
                        <div style="display: flex;justify-content: space-between;align-items: center;">
                            <div>操作</div>
                            <div @click="setFull">
                                <el-tooltip content="全屏" placement="bottom">
                                    <el-icon ><FullScreen /></el-icon>
                                </el-tooltip>
                            </div>
                        </div>
                    </template>
                    <template #default="scope">
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'detail')" v-auth="'Detail'">详情</span>
                        <span class="table-operate-btn delete" @click="handleEdit(scope.row,'delete')" v-auth="'Delete'">删除</span>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <Pagination v-bind:child-msg="pageparm" @callFather="callFather"></Pagination>
        <addModuleNotice ref="addModuleFlag" @refreshData="getData" v-if="isDialogVisible" @closed="isDialogVisible = false"></addModuleNotice>
    </div>
</template>

<script setup name="myMessage">
    import { ref, onMounted, onUnmounted, nextTick } from 'vue'
    import { useRoute } from 'vue-router'
    import addModuleNotice from "./components/addModuleNotice.vue"
    import Pagination from "@/components/Pagination.vue"
    import Api from '@/api/api'
    import { FullScreen } from '@element-plus/icons-vue'
    import lySearchBar from '@/components/lySearchBar.vue'
    import {deepClone} from "@/utils/util"
    import { ElMessage, ElMessageBox } from 'element-plus'

    // 路由
    const route = useRoute()

    // 响应式数据
    const isFull = ref(false)
    const tableHeight = ref(500)
    const loadingPage = ref(false)
    const formInline = ref({
        page: 1,
        limit: 10,
        search: ''
    })
    const pageparm = ref({
        page: 1,
        limit: 10,
        total: 0
    })
    const statusList = ref([
        {id:true, name:'已读'},
        {id:false, name:'未读'}
    ])
    const tableData = ref([])
    const tableSelect = ref(null)
    const tableref = ref(null)
    const addModuleFlag = ref(null)
    let isDialogVisible = ref(false)

    // 方法定义
    // 表格序列号
    const getIndex = ($index) => {
        return (pageparm.value.page-1)*pageparm.value.limit + $index +1
    }

    // 切换全屏
    const setFull = () => {
        isFull.value = !isFull.value
        window.dispatchEvent(new Event('resize'))
    }

    // 文字超出10字显示省略号
    const customEllipsis = (value) => {
        if (!value) return ""
        value = value.replace(/<.*?>/ig,"") // 移除HTML标签
        return value.length > 18 ? value.slice(0, 18) + "..." : value
    }

    // 新增模块
    const addModule = () => {
        isDialogVisible.value = true
        nextTick(()=>{
            addModuleFlag.value.addModuleFn(null, 'add')
        })
    }

    // 编辑/删除/重置操作
    const handleEdit = (row, flag) => {
        if (flag === 'detail') {
            isDialogVisible.value = true
            nextTick(()=>{
                let tmpnewrow = deepClone(row)
                let newrow = tmpnewrow.notification
                newrow.id = tmpnewrow.id
                addModuleFlag.value.isUserOwnMsg = true
                addModuleFlag.value.addModuleFn(newrow, 'detail')
                if(!row.is_read){
                    addModuleFlag.value.readMsg()
                }
            })
        } else if (flag === 'delete') {
            ElMessageBox.confirm('您确定要删除选中的内容？',"提示", {
                type:"warning",
                closeOnClickModal: false
            }).then(() => {
                Api.delOwnMessage({id: row.id}).then(res => {
                    if (res.code == 2000) {
                        ElMessage.success(res.msg)
                        search()
                    } else {
                        ElMessage.warning(res.msg)
                    }
                })
            }).catch(() => {})
        } else if (flag === "reset") {
            formInline.value = {
                page: 1,
                limit: 10,
                search: ''
            }
            pageparm.value = {
                page: 1,
                limit: 10,
                total: 0
            }
            getData()
        }
    }

    // 分页回调
    const callFather = (parm) => {
        formInline.value.page = parm.page
        formInline.value.limit = parm.limit
        getData()
    }

    // 搜索
    const search = () => {
        formInline.value.page = 1
        formInline.value.limit = 10
        getData()
    }

    // 获取列表数据
    const getData = async () => {
        loadingPage.value = true
        Api.getOwnMessage(formInline.value).then(res => {
            loadingPage.value = false
            if (res.code == 2000) {
                tableData.value = res.data.data
                pageparm.value.page = res.data.page
                pageparm.value.limit = res.data.limit
                pageparm.value.total = res.data.total
            }
        })
    }

    // 生命周期钩子
    onMounted(() => {
        getData()
    })

</script>

<style lang="scss" scoped>
    .ellipsis {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .message-manage-container{
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: 10px;
        box-sizing: border-box;
        transition: all 0.3s ease;
    }

    .table-container {
        flex: 1;
        background: #fff;
        border-radius: 4px;
        overflow: hidden;

        :deep(.el-table) {
            .el-table__cell {
                padding: 8px 0;
            }
            .el-table__body-wrapper{
                background:var(--el-bg-color);
            }
        }
    }
</style>