<template>
    <div :class="['journal-manage-container', { 'ly-is-full': isFull }]">
        <el-card class="tableSelect" ref="tableSelect" shadow="hover">
            <lySearchBar :model="formInline" @search="search" @reset="handleEdit('','reset')">
                <template #actions-right>
                    <el-button @click="deleteAlllogs" type="danger" v-auth="'DeleteAll'">
                        全部清空
                    </el-button>
                </template>
                <!-- 自定义默认搜索项 -->
                <template #default>
                    <el-form-item label="关键词">
                        <el-input
                            v-model.trim="formInline.search"
                            maxlength="60"
                            clearable
                            placeholder="关键词"
                            style="width:160px"
                        />
                    </el-form-item>
                    <!-- <el-form-item label="IP地址">
                        <el-input
                        v-model.trim="formInline.request_ip"
                        maxlength="60"
                        clearable
                        placeholder="IP地址"
                        style="width:160px"
                        />
                    </el-form-item> -->

                    <el-form-item label="创建时间">
                        <el-date-picker
                        v-model="timers"
                        type="datetimerange"
                        @change="timeChange"
                        range-separator="至"
                        start-placeholder="开始日期"
                        end-placeholder="结束日期"
                        />
                    </el-form-item>
                </template>
            </lySearchBar>
        </el-card>
        <div class="table-container">
            <el-table border :data="tableData" v-loading="loadingPage" style="width: 100%;height:100%;" :flexible="true">
                <!-- <el-table-column type="index" width="60" align="center" label="序号" :index="getIndex"/> -->

                <el-table-column min-width="100" prop="req_modular" label="请求模块" show-overflow-tooltip/>

                <el-table-column min-width="160" prop="req_path" label="请求地址" show-overflow-tooltip/>

                <el-table-column width="90" prop="req_method" label="请求方法" show-overflow-tooltip/>

                <el-table-column min-width="100" prop="req_ip" label="IP地址" show-overflow-tooltip/>

                <!-- <el-table-column min-width="130" prop="ip_area" label="IP归属地" show-overflow-tooltip/> -->

                <el-table-column min-width="130" prop="req_browser" label="请求浏览器" show-overflow-tooltip/>

                <el-table-column width="90" prop="req_body" label="请求数据">
                    <template #default="{ row }">
                        <div class="json-cell">
                        <el-popover
                            v-if="row.req_body"
                            :placement="ismobile ? 'bottom' : 'left-start'"
                            trigger="click"
                            :width="ismobile ? '80%' : '50%'"
                            :show-arrow="false"
                        >
                            <template #reference>
                            <el-tag class="json-tag" size="small" effect="dark">
                                <el-icon><Warning /></el-icon>
                            </el-tag>
                            </template>
                            <div class="json-popover-content">
                            <pre>{{ formatBody(row.req_body) }}</pre>
                            </div>
                        </el-popover>
                        <span v-else>无</span>
                        </div>
                    </template>
                </el-table-column>

                <el-table-column width="80" prop="resp_code" label="响应码">
                    <template #default="{ row }">
                        <el-tag v-if="row.resp_code" :type="row.resp_code === '2000' ? 'success' : 'warning'">
                        {{ row.resp_code }}
                        </el-tag>
                        <span v-else></span>
                    </template>
                </el-table-column>

                <el-table-column width="90" prop="json_result" label="返回信息">
                    <template #default="{ row }">
                        <div class="json-cell">
                        <el-popover
                            v-if="row.json_result"
                            :placement="ismobile ? 'bottom' : 'left-start'"
                            trigger="click"
                            :width="ismobile ? '80%' : '50%'"
                            :show-arrow="false"
                        >
                            <template #reference>
                                <el-tag class="json-tag" size="small" effect="dark">
                                    <el-icon><Warning /></el-icon>
                                </el-tag>
                            </template>
                            <div class="json-popover-content">
                                <pre>{{ formatBody(row.json_result) }}</pre>
                            </div>
                        </el-popover>
                        <span v-else>无</span>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column width="130" prop="creator_name" label="操作人" />
                <el-table-column width="160" prop="create_datetime" label="创建时间" show-overflow-tooltip/>
                <el-table-column label="操作" fixed="right" width="120">
                    <template #header>
                        <div class="table-header-actions">
                        <span>操作</span>
                        <el-tooltip content="全屏" placement="bottom">
                            <el-icon @click="setFull"><FullScreen /></el-icon>
                        </el-tooltip>
                        </div>
                    </template>
                    <template #default="{ row }">
                        <!-- <span class="table-operate-btn" @click="handleEdit(row,'detail')">详情</span> -->
                        <span class="table-operate-btn delete" @click="handleEdit(row,'delete')" v-auth="'Delete'">删除</span>
                </template>
                </el-table-column>
            </el-table>
        </div>

        <Pagination v-bind:child-msg="pageparm" @callFather="callFather"/>

        <journal-manage-detail ref="journalManageDetailFlag" />
    </div>
</template>

<script setup>
    import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
    import { useRoute } from 'vue-router'
    import { ElMessage, ElMessageBox } from 'element-plus'
    import {
        FullScreen,
        Warning,
        ArrowUp,
        Document
    } from '@element-plus/icons-vue'
    import Pagination from '@/components/Pagination.vue'
    import JournalManageDetail from './components/journalManageDetail.vue'
    import { dateFormats, getTableHeight } from '@/utils/util'
    import lySearchBar from '@/components/lySearchBar.vue'
    import Api from '@/api/api'
    import { useSiteThemeStore } from "@/store/siteTheme";

    const siteThemeStore = useSiteThemeStore()

    const route = useRoute()

    const isFull = ref(false)
    const tableHeight = ref(500)
    const loadingPage = ref(false)
    const tableSelect = ref(null)
    const journalManageDetailFlag = ref(null)
    const tableref = ref(null)

    const formInline = ref({
        page: 1,
        limit: 20,
    })

    const timers = ref([])
    const tableData = ref([])
    const pageparm = ref({
        page: 1,
        limit: 20,
        total: 0
    })

    let ismobile = computed(() => {
        return siteThemeStore.ismobile
    })

    const getIndex = (index) => {
        return (pageparm.value.page - 1) * pageparm.value.limit + index + 1
    }

    const formatBody = (value) => {
        if (!value) return value;
        
        // 如果是对象直接返回
        if (typeof value === 'object') return value;
        
        try {
            // 尝试直接解析
            return JSON.parse(value);
        } catch (err) {
            try {
                // 尝试替换单引号为双引号
                const fixedStr = value.replace(/'/g, '"');
                return JSON.parse(fixedStr);
            } catch (e) {
                return value
            }
        }
    }

    const deleteAlllogs = () => {
        ElMessageBox.confirm('是否确认清空全部日志数据', '警告', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            Api.systemOperationlogDeletealllogsDelete().then((res) => {
                if (res.code == 2000) {
                ElMessage.success(res.msg)
                search()
                } else {
                ElMessage.warning(res.msg)
                }
            })
        }).catch(() => {})
    }

    const handleEdit = (row, flag) => {
        if (flag === 'detail') {
            journalManageDetailFlag.value.journalManageDetailFn(row)
        } else if (flag === 'delete') {
            ElMessageBox.confirm('您确定要删除选中的数据吗？', {
            closeOnClickModal: false
            })
            .then(() => {
                Api.systemOperationlogDelete({ id: row.id }).then((res) => {
                if (res.code == 2000) {
                    ElMessage.success(res.msg)
                    getData()
                } else {
                    ElMessage.warning(res.msg)
                }
                })
            })
            .catch(() => {})
        } else if (flag === 'reset') {
            formInline.value = {
                page: 1,
                limit: 20,
            }
            pageparm.value = {
                page: 1,
                limit: 20,
                total: 0
            }
            timers.value = []
            getData()
        }
    }

    const callFather = (parm) => {
        formInline.value.page = parm.page
        formInline.value.limit = parm.limit
        getData()
    }

    const search = () => {
        formInline.value.page = 1
        formInline.value.limit = 20
        getData()
    }

    const timeChange = (val) => {
        if (val) {
            formInline.value.beginAt = dateFormats(val[0], 'yyyy-MM-dd hh:mm:ss')
            formInline.value.endAt = dateFormats(val[1], 'yyyy-MM-dd hh:mm:ss')
        } else {
            formInline.value.beginAt = null
            formInline.value.endAt = null
        }
    }

    const getData = async () => {
        try {
            loadingPage.value = true
            const res = await Api.systemOperationlog(formInline.value)
            if (res.code == 2000) {
            tableData.value = res.data.data
            pageparm.value.page = res.data.page
            pageparm.value.limit = res.data.limit
            pageparm.value.total = res.data.total
            }
        } finally {
            loadingPage.value = false
        }
    }

    const setFull = () => {
        isFull.value = !isFull.value
        nextTick(() => {
            getTheTableHeight()
        })
    }

    const getTheTableHeight = () => {
        const tabSelectHeight = tableSelect.value ? tableSelect.value.offsetHeight : 0
        const adjustedHeight = isFull.value ? tabSelectHeight - 110 : tabSelectHeight
        tableHeight.value = getTableHeight(adjustedHeight)
    }

    const listenResize = () => {
        nextTick(() => {
            getTheTableHeight()
        })
    }

    onMounted(() => {
        window.addEventListener('resize', listenResize)
        nextTick(() => {
            getTheTableHeight()
        })
        getData()
    })

    onUnmounted(() => {
        window.removeEventListener('resize', listenResize)
    })
</script>

<style scoped lang="scss">
    .journal-manage-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: 10px;
        box-sizing: border-box;
        transition: all 0.3s ease;

        &.ly-is-full {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 2000;
            background: #fff;
            padding: 16px;
            overflow: auto;
        }
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

            .json-cell {
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .json-tag {
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
            }

            .action-buttons {
                display: flex;
                gap: 8px;
            }
        }
    }

    .json-popover-content {
        background: #1e1e1e;
        color: rgb(194, 106, 62);
        max-height: 60vh;
        overflow: auto;
        padding: 12px;
        border-radius: 4px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 14px;
        line-height: 1.5;
        pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    }

    .table-header-actions {
        display: flex;
        align-items: center;
        justify-content: space-between;

        .el-icon {
            cursor: pointer;
            color: #909399;
            &:hover {
                color: #409eff;
            }
        }
    }

    @media (max-width: 768px) {

        .table-container {
            :deep(.el-table) {
                .el-table__cell {
                    padding: 4px 0;
                }
            }
        }
    }
</style>