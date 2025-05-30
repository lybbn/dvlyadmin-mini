<template>
  <div :class="{'ly-is-full':isFull}">
        <div class="tableSelect" ref="tableSelect">
            <el-form :inline="true" :model="formInline" label-position="left">
                <el-form-item label="用户昵称：">
                    <el-input v-model.trim="formInline.nickname" maxlength="60"  clearable placeholder="用户昵称" @change="search" style="width:160px"></el-input>
                </el-form-item>
                <el-form-item label="手机号：">
                    <el-input v-model.trim="formInline.mobile" maxlength="60"  clearable placeholder="手机号" @change="search" style="width:160px"></el-input>
                </el-form-item>
                <el-form-item label="创建时间：">
                    <el-date-picker
                            style="width:350px"
                            v-model="timers"
                            type="datetimerange"
                            @change="timeChange"
                            range-separator="至"
                            start-placeholder="开始日期"
                            end-placeholder="结束日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label=""><el-button  @click="search" type="primary" icon="Search" v-show="hasPermission(this.$route.name,'Search')">查询</el-button></el-form-item>
                <el-form-item label=""><el-button  @click="handleEdit('','reset')" icon="Refresh">重置</el-button></el-form-item>
                <el-form-item label=""><el-button  @click="handleAddClick" type="primary" icon="Plus" v-show="hasPermission(this.$route.name,'Create')">新增</el-button></el-form-item>
                <el-form-item label=""><el-button  @click="exportDataBackend" type="primary">导出</el-button></el-form-item>
            </el-form>
        </div>

        <div class="table">
            <ly-table tableName="userManageTable" :height="tableHeight" :pageSize="10" :apiObj="Api.apiSystemMenu" :params="formInline" ref="tableref" :column="column" showSequence>
                <template #avatar="scope">
                    <el-image  :src="scope.row.avatar ? scope.row.avatar : defaultImg" :preview-src-list="[scope.row.avatar]" style="width: 30px;height: 30px" preview-teleported></el-image>
                </template>
                <!-- <template #is_active="scope">
                    <el-tag v-if="scope.row.is_active">正常</el-tag>
                    <el-tag v-else type="danger">禁用</el-tag>
                </template> -->
                <template #is_active="scope">
                    <el-switch v-model="scope.row.is_active" active-color="#13ce66" inactive-color="#ff4949" @change="changeStatus(scope.row)"></el-switch>
                </template>
                <el-table-column label="操作" fixed="right" width="180">
                    <template #header>
                        <div style="display: flex;justify-content: space-between;align-items: center;">
                            <div>操作</div>
                            <div @click="setFull">
                                <el-tooltip content="全屏" placement="bottom">
                                    <el-icon ><full-screen /></el-icon>
                                </el-tooltip>
                            </div>
                        </div>
                    </template>
                    <template #default="scope">
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'edit')" v-show="hasPermission(this.$route.name,'Update')">编辑</span>
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'detail')" v-show="hasPermission(this.$route.name,'Retrieve')">详情</span>
                        <span class="table-operate-btn" @click="handleEdit(scope.row,'delete')" v-show="hasPermission(this.$route.name,'Delete')">删除</span>
                        <!-- <span class="table-operate-btn" @click="handleEdit(scope.row,'disable')" v-show="hasPermission(this.$route.name,'Update')">
                            <span v-if="scope.row.is_active">禁用</span>
                            <span v-else>启用</span>
                        </span> -->
                    </template>
                </el-table-column>
            </ly-table>
        </div>
        <addUser ref="addUserFlag" @refreshData="getData" v-if="isDialogVisible" @closed="isDialogVisible = false"></addUser>
        <userDetail ref="userDetailFlag" v-if="isDetailDialogVisible" @closed="isDetailDialogVisible = false"></userDetail>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { FullScreen } from '@element-plus/icons-vue'
import { dateFormat, getTableHeight } from "@/utils/util"
import Api from '@/api/api'
import addUser from "./components/moduleCreateUpdate.vue"
import userDetail from "./components/moduleCreateUpdate.vue"

const route = useRoute()

// 状态管理
const isFull = ref(false)
const tableHeight = ref(500)
const isDetailDialogVisible = ref(false)
const isDialogVisible = ref(false)
const formInline = ref({})
const timers = ref([])
const tableSelect = ref(null)
const tableref = ref(null)
const addUserFlag = ref(null)
const userDetailFlag = ref(null)

const defaultImg = ''
const statusList = [
  { id: 1, name: '正常' },
  { id: 0, name: '禁用' }
]
const identityList = [
  { id: 0, name: '普通用户' },
  { id: 1, name: '会员' }
]

const column = [
  {
    label: "用户头像",
    prop: "avatar",
    width: "100"
  },
  {
    label: "用户名",
    prop: "username",
    minWidth: "110"
  },
  {
    label: "用户昵称",
    prop: "nickname",
    minWidth: "110"
  },
  {
    label: "手机号",
    prop: "mobile",
    minWidth: "100",
  },
  {
    label: "状态",
    prop: "is_active",
    width: "100"
  },
  {
    label: "创建时间",
    prop: "create_datetime",
    minWidth: "180"
  }
]

// 方法
const setFull = () => {
  isFull.value = !isFull.value
  window.dispatchEvent(new Event('resize'))
}

const handleAddClick = () => {
  isDialogVisible.value = true
  nextTick(() => {
    addUserFlag.value.handleOpen(null, "新增")
  })
}

const handleEdit = (row, flag) => {
  switch (flag) {
    case 'edit':
      isDialogVisible.value = true
      nextTick(() => {
        addUserFlag.value.handleOpen(row, "编辑")
      })
      break
    case 'detail':
      isDetailDialogVisible.value = true
      nextTick(() => {
        userDetailFlag.value.handleOpen(row, '详情')
      })
      break
    case 'delete':
      ElMessageBox.confirm('您确定要删除选中的数据吗？', "警告", {
        closeOnClickModal: false,
        type: "warning"
      }).then(() => {
        UsersUsersDelete({ id: row.id }).then(res => {
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
  const originalStatus = row.is_active
  row.is_active = !row.is_active
  
  ElMessageBox.confirm('确定修改状态吗？', '提醒', {
    closeOnClickModal: false,
    type: "warning"
  }).then(() => {
    UsersUsersdisableEdit({ id: row.id }).then(res => {
      if (res.code == 2000) {
        ElMessage.success(res.msg)
        getData()
      } else {
        row.is_active = originalStatus
        ElMessage.warning(res.msg)
      }
    })
  }).catch(() => {
    row.is_active = originalStatus
  })
}

const downloadFileURL = (url) => {
  const iframe = document.createElement("iframe")
  iframe.style.display = "none"
  iframe.src = url
  document.body.appendChild(iframe)
}

const exportDataBackend = () => {
  const params = {
    page: 1,
    limit: 9999,
  }
  UsersUsersExportexecl(params).then(res => {
    if (res.code == 2000) {
      downloadFileURL(res.data.data)
    }
  })
}

const search = () => {
  tableref.value.reload(formInline.value)
}

const getData = () => {
  tableref.value.getData()
}

const timeChange = (val) => {
  if (val) {
    formInline.value.beginAt = dateFormat(val[0], 'yyyy-MM-dd hh:mm:ss')
    formInline.value.endAt = dateFormat(val[1], 'yyyy-MM-dd hh:mm:ss')
  } else {
    formInline.value.beginAt = null
    formInline.value.endAt = null
  }
  search()
}

const getTheTableHeight = () => {
  let tabSelectHeight = tableSelect.value ? tableSelect.value.offsetHeight : 0
  tabSelectHeight = isFull.value ? tabSelectHeight - 110 : tabSelectHeight
  tableHeight.value = getTableHeight(tabSelectHeight, false) - 125
}

const listenResize = () => {
  nextTick(() => {
    getTheTableHeight()
  })
}

// 生命周期
onMounted(() => {
  window.addEventListener('resize', listenResize)
  nextTick(() => {
    getTheTableHeight()
  })
})

onUnmounted(() => {
  window.removeEventListener("resize", listenResize)
})

// 权限检查函数
const hasPermission = (routeName, action) => {
  // 实现你的权限检查逻辑
  return true
}
</script>

<style scoped>
/* 样式保持不变 */
</style>