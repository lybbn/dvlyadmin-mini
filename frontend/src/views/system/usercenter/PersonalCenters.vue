<template>
  <div class="personal-center">
      <el-row :gutter="10">
        <!-- 左侧个人信息 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
          <el-card shadow="hover" class="user-card">
            <div class="user-info">
              <div class="avatar-upload">
                <el-upload
                  class="avatar-uploader"
                  action="/api/upload"
                  :show-file-list="false"
                  :on-success="handleAvatarSuccess"
                >
                  <el-avatar :size="120" :src="userInfo.avatar" />
                  <div class="avatar-mask">
                    <el-icon><Edit /></el-icon>
                  </div>
                </el-upload>
              </div>
              <div class="info-item">
                <span class="label">昵称：</span>
                <el-input v-if="editing" v-model="userInfo.nickname" />
                <span v-else>{{ userInfo.nickname }}</span>
              </div>
              <div class="info-item">
                <span class="label">姓名：</span>
                <el-input v-if="editing" v-model="userInfo.realName" />
                <span v-else>{{ userInfo.realName }}</span>
              </div>
              <div class="info-item">
                <span class="label">性别：</span>
                <el-select v-if="editing" v-model="userInfo.gender">
                  <el-option label="男" value="男" />
                  <el-option label="女" value="女" />
                </el-select>
                <span v-else>{{ userInfo.gender }}</span>
              </div>
              <div class="info-item">
                <span class="label">手机号：</span>
                <el-input v-if="editing" v-model="userInfo.phone" />
                <span v-else>{{ userInfo.phone }}</span>
              </div>
              <div class="info-item">
                <span class="label">邮箱：</span>
                <el-input v-if="editing" v-model="userInfo.email" />
                <span v-else>{{ userInfo.email }}</span>
              </div>
              <div class="info-item">
                <span class="label">部门：</span>
                <span>{{ userInfo.department }}</span>
              </div>
              <div class="info-item">
                <span class="label">角色：</span>
                <span>{{ userInfo.role }}</span>
              </div>
              <div class="edit-buttons">
                <el-button v-if="!editing" type="primary" @click="startEditing" round>编辑信息</el-button>
                <el-button v-else type="success" @click="saveInfo" round>保存</el-button>
                <el-button v-if="editing" @click="cancelEditing" round>取消</el-button>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧功能区域 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
          <!-- 消息通知卡片 -->
          <el-card shadow="hover" class="mb-20">
            <template #header>
              <div class="card-header">
                <span>消息通知</span>
                <el-button link type="primary" @click="gotoMessageList">查看更多</el-button>
              </div>
            </template>
            <el-scrollbar height="250px">
              <el-table :data="messages" style="width: 100%">
                <el-table-column prop="title" label="标题" width="180" />
                <el-table-column prop="content" label="内容" />
                <el-table-column prop="time" label="时间" width="180" />
              </el-table>
            </el-scrollbar>
          </el-card>

          <!-- 操作日志 -->
          <el-card shadow="hover">
            <el-tabs v-model="activeTab">
              <el-tab-pane label="操作日志" name="logs">
                <el-scrollbar height="300px">
                  <el-table :data="operationLogs" style="width: 100%">
                    <el-table-column prop="module" label="模块" width="180" />
                    <el-table-column prop="action" label="操作" />
                    <el-table-column prop="time" label="时间" width="180" />
                  </el-table>
                </el-scrollbar>
                <div class="pagination">
                  <el-pagination
                    layout="prev, pager, next"
                    :total="totalLogs"
                    :page-size="pageSize"
                    @current-change="handlePageChange"
                  />
                </div>
              </el-tab-pane>
              <el-tab-pane label="修改密码" name="password">
                <el-form :model="passwordForm" :rules="passwordRules" ref="passwordForm" label-width="120px">
                  <el-form-item label="原密码" prop="oldPassword">
                    <el-input type="password" v-model="passwordForm.oldPassword" show-password />
                  </el-form-item>
                  <el-form-item label="新密码" prop="newPassword">
                    <el-input type="password" v-model="passwordForm.newPassword" show-password />
                    <div class="password-strength">
                      <span :class="strengthClass">{{ strengthText }}</span>
                    </div>
                  </el-form-item>
                  <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input type="password" v-model="passwordForm.confirmPassword" show-password />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitPassword">提交</el-button>
                  </el-form-item>
                </el-form>
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
      </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Edit } from '@element-plus/icons-vue'

const router = useRouter()

// 用户信息
const userInfo = ref({
  avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
  nickname: '管理员',
  realName: '张三',
  gender: '男',
  phone: '13800138000',
  email: 'admin@example.com',
  department: '技术部',
  role: '超级管理员'
})

const editing = ref(false)
const originalInfo = ref({})

// 消息通知
const messages = ref([
  { title: '系统更新', content: '系统将于今晚23:00进行维护更新', time: '2023-06-01 10:00' },
  { title: '任务提醒', content: '您有新的任务待处理', time: '2023-06-01 09:30' },
  { title: '审批通过', content: '您的请假申请已通过', time: '2023-05-31 16:45' },
  { title: '系统通知', content: '新版本v2.0已发布', time: '2023-05-30 09:15' },
  { title: '会议提醒', content: '今天下午3点有部门会议', time: '2023-05-29 10:30' },
  { title: '工资发放', content: '5月份工资已发放', time: '2023-05-28 12:00' },
  { title: '培训通知', content: '下周二有新技术培训', time: '2023-05-27 14:20' },
  { title: '考勤异常', content: '您有未打卡记录', time: '2023-05-26 08:45' },
  { title: '生日祝福', content: '今天是您的生日，祝您生日快乐！', time: '2023-05-25 00:00' },
  { title: '系统公告', content: '服务器维护通知', time: '2023-05-24 15:30' }
])

// 操作日志
const operationLogs = ref([
  { module: '用户管理', action: '新增用户', time: '2023-06-01 10:00' },
  { module: '角色管理', action: '修改角色权限', time: '2023-06-01 09:30' },
  { module: '系统设置', action: '更新系统参数', time: '2023-05-31 16:45' },
  { module: '审批流程', action: '处理请假申请', time: '2023-05-30 09:15' },
  { module: '数据统计', action: '导出报表', time: '2023-05-29 10:30' },
  { module: '系统监控', action: '查看服务器状态', time: '2023-05-28 12:00' },
  { module: '消息中心', action: '发送系统通知', time: '2023-05-27 14:20' },
  { module: '个人设置', action: '修改个人信息', time: '2023-05-26 08:45' },
  { module: '文件管理', action: '上传文件', time: '2023-05-25 00:00' },
  { module: '系统日志', action: '查看操作记录', time: '2023-05-24 15:30' }
])
const totalLogs = ref(50)
const pageSize = ref(10)
const activeTab = ref('logs')

// 密码修改表单
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 密码验证规则
const validatePassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入密码'))
  } else if (value.length < 8) {
    callback(new Error('密码长度不能少于8位'))
  } else {
    callback()
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.value.newPassword) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 密码强度检测
const passwordStrength = computed(() => {
  const password = passwordForm.value.newPassword
  if (!password) return 0
  
  let strength = 0
  if (password.length >= 8) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++
  
  return strength
})

const strengthText = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 1) return '弱'
  if (strength <= 3) return '中'
  return '强'
})

const strengthClass = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 1) return 'weak'
  if (strength <= 3) return 'medium'
  return 'strong'
})

// 方法
const gotoMessageList = () => {
  router.push('/message/list')
}

const handlePageChange = (page) => {
  // 获取对应页面的日志数据
  console.log('切换到第', page, '页')
}

const submitPassword = () => {
  // 提交密码修改
  console.log('提交密码修改')
}

const startEditing = () => {
  editing.value = true
  originalInfo.value = {...userInfo.value}
}

const cancelEditing = () => {
  editing.value = false
  userInfo.value = {...originalInfo.value}
}

const saveInfo = () => {
  // 保存用户信息
  editing.value = false
  console.log('保存用户信息', userInfo.value)
}

const handleAvatarSuccess = (response) => {
  userInfo.value.avatar = response.url
}

onMounted(() => {
  // 可以在这里获取用户信息和消息通知等数据
})
</script>

<style scoped>
.personal-center {
  padding: 10px;
}

.user-info {
  padding: 20px;
}

.info-item {
  margin: 15px 0;
  font-size: 14px;
  display: flex;
  align-items: center;
}

.info-item .label {
  font-weight: bold;
  color: #666;
  min-width: 60px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mb-20 {
  margin-bottom: 10px;
}

.password-strength {
  margin-top: 5px;
  font-size: 12px;
}

.password-strength .weak {
  color: #f56c6c;
}

.password-strength .medium {
  color: #e6a23c;
}

.password-strength .strong {
  color: #67c23a;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.avatar-uploader {
  position: relative;
  margin: 0 auto 20px;
  width: 120px;
}

.avatar-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
}

.avatar-uploader:hover .avatar-mask {
  opacity: 1;
}

.edit-buttons {
  margin-top: 20px;
  text-align: center;
}

.user-card {
  margin-bottom: 20px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .info-item {
    margin: 10px 0;
    flex-direction: row;
    align-items: flex-start;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .edit-buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .el-button {
    width: 100%;
  }
  
  .el-form-item {
    margin-bottom: 15px;
  }
  
  .el-form-item__label {
    width: 100% !important;
    text-align: left;
  }
  
  .el-form-item__content {
    margin-left: 0 !important;
  }
}
</style>