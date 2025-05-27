<template>
    <div class="personal-center-container">
        <el-card shadow="hover" class="profile-card">
            <!-- 头部信息区 -->
            <div class="profile-header">
                <div class="avatar-section">
                    <el-avatar :size="120" :src="userInfo.avatar" class="profile-avatar">
                        <span v-if="!userInfo.avatar">{{ userInfo.name.charAt(0).toUpperCase() }}</span>
                    </el-avatar>
                    <el-button type="primary" size="small" @click="showAvatarDialog" class="avatar-edit-btn">
                        <el-icon><Camera /></el-icon> 更换头像
                    </el-button>
                </div>
                
                <div class="profile-basic">
                    <h1 class="profile-name">{{ userInfo.nickname }}</h1>
                    <div class="profile-meta">
                        <div class="meta-item">
                            <el-icon><User /></el-icon>
                            <span>{{ userInfo.name }}</span>
                        </div>
                        <div class="meta-item">
                            <el-icon><Iphone /></el-icon>
                            <span>{{ userInfo.phone }}</span>
                        </div>
                        <div class="meta-item">
                            <el-icon><Message /></el-icon>
                            <span>{{ userInfo.email }}</span>
                        </div>
                    </div>
                    <div class="profile-org">
                        <el-tag type="info" size="large" class="org-tag">
                            <el-icon><OfficeBuilding /></el-icon>
                            {{ userInfo.department }}
                        </el-tag>
                        <el-tag type="info" size="large" class="org-tag">
                            <el-icon><Postcard /></el-icon>
                            {{ userInfo.role }}
                        </el-tag>
                    </div>
                </div>
                
                <div class="profile-actions">
                    <el-button type="primary" @click="showEditDialog" round>
                        <el-icon><Edit /></el-icon> 编辑资料
                    </el-button>
                    <el-button @click="showPasswordDialog" round>
                        <el-icon><Lock /></el-icon> 修改密码
                    </el-button>
                </div>
            </div>

            <!-- 内容标签页 -->
            <el-tabs v-model="activeTab" class="profile-tabs">
                <el-tab-pane label="基本信息" name="basic">
                    <div class="info-section">
                        <el-descriptions :column="isMobile ? 1 : 2" border>
                            <el-descriptions-item label="用户ID">{{ userInfo.id }}</el-descriptions-item>
                            <el-descriptions-item label="昵称">{{ userInfo.nickname }}</el-descriptions-item>
                            <el-descriptions-item label="姓名">{{ userInfo.name }}</el-descriptions-item>
                            <el-descriptions-item label="性别">
                            <el-tag :type="userInfo.gender === '男' ? 'primary' : 'danger'">
                                {{ userInfo.gender }}
                            </el-tag>
                            </el-descriptions-item>
                            <el-descriptions-item label="手机号">{{ userInfo.phone }}</el-descriptions-item>
                            <el-descriptions-item label="邮箱">{{ userInfo.email }}</el-descriptions-item>
                            <el-descriptions-item label="部门">{{ userInfo.department }}</el-descriptions-item>
                            <el-descriptions-item label="角色">{{ userInfo.role }}</el-descriptions-item>
                            <el-descriptions-item label="注册时间">{{ userInfo.registerTime }}</el-descriptions-item>
                            <el-descriptions-item label="最后登录">{{ userInfo.lastLogin }}</el-descriptions-item>
                        </el-descriptions>
                    </div>
                </el-tab-pane>
                
                <el-tab-pane label="消息通知" name="notifications">
                    <div class="notification-section">
                        <el-card shadow="never" v-for="(item, index) in notifications" :key="index" 
                                    class="notification-card" :class="{'unread': !item.read}">
                            <div class="notification-content">
                                <div class="notification-icon">
                                    <el-icon :size="24" :color="notificationTypes[item.type].color">
                                        <component :is="notificationTypes[item.type].icon" />
                                    </el-icon>
                                </div>
                                <div class="notification-main">
                                    <h4>{{ item.title }}</h4>
                                    <p>{{ item.content }}</p>
                                    <div class="notification-meta">
                                        <span>{{ item.time }}</span>
                                        <el-tag size="small" :type="notificationTypes[item.type].tagType">
                                            {{ notificationTypes[item.type].name }}
                                        </el-tag>
                                    </div>
                                </div>
                            </div>
                        </el-card>
                        
                        <div class="view-more">
                            <el-button type="primary" text @click="goToNotificationPage">查看更多消息</el-button>
                        </div>
                    </div>
                </el-tab-pane>
                
                <el-tab-pane label="操作日志" name="logs">
                    <div class="log-section">
                        <el-table :data="operationLogs" style="width: 100%" border>
                            <el-table-column prop="time" label="时间" width="180" />
                            <el-table-column prop="module" label="模块" width="120" />
                            <el-table-column prop="action" label="操作" />
                            <el-table-column prop="ip" label="IP地址" width="150" />
                            <el-table-column prop="status" label="状态" width="100">
                                <template #default="{row}">
                                    <el-tag :type="row.status === '成功' ? 'success' : 'danger'">
                                    {{ row.status }}
                                    </el-tag>
                                </template>
                            </el-table-column>
                        </el-table>
                        
                        <div class="pagination">
                            <el-pagination
                            v-model:current-page="logPage.current"
                            v-model:page-size="logPage.size"
                            :total="logPage.total"
                            layout="total, prev, pager, next, jumper"
                            @current-change="fetchOperationLogs"
                            />
                        </div>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </el-card>

        <!-- 编辑资料对话框 -->
        <el-dialog v-model="editDialogVisible" title="编辑资料" width="50%" :fullscreen="isMobile" :close-on-click-modal="false">
            <el-form :model="editForm" label-width="100px" :rules="editRules" ref="editFormRef">
                <el-row :gutter="20">
                    <el-col :span="isMobile ? 24 : 12">
                        <el-form-item label="昵称" prop="nickname">
                            <el-input v-model="editForm.nickname" placeholder="请输入昵称" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="isMobile ? 24 : 12">
                        <el-form-item label="姓名" prop="name">
                            <el-input v-model="editForm.name" placeholder="请输入真实姓名" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="isMobile ? 24 : 12">
                        <el-form-item label="性别" prop="gender">
                            <el-radio-group v-model="editForm.gender">
                            <el-radio label="男">男</el-radio>
                            <el-radio label="女">女</el-radio>
                            </el-radio-group>
                        </el-form-item>
                    </el-col>
                    <el-col :span="isMobile ? 24 : 12">
                        <el-form-item label="手机号" prop="phone">
                            <el-input v-model="editForm.phone" placeholder="请输入手机号">
                            <template #prepend>
                                <el-select v-model="phonePrefix" style="width: 70px">
                                <el-option label="+86" value="+86" />
                                <el-option label="+852" value="+852" />
                                <el-option label="+853" value="+853" />
                                </el-select>
                            </template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="isMobile ? 24 : 12">
                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="editForm.email" placeholder="请输入邮箱" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="isMobile ? 24 : 12">
                        <el-form-item label="部门" prop="department">
                            <el-select v-model="editForm.department" placeholder="请选择部门">
                            <el-option
                                v-for="item in departments"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <el-button @click="editDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="saveProfile">保存</el-button>
            </template>
        </el-dialog>

        <!-- 修改密码对话框 -->
        <el-dialog v-model="passwordDialogVisible" title="修改密码" width="50%" :fullscreen="isMobile" :close-on-click-modal="false">
            <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
                <el-form-item label="当前密码" prop="currentPassword">
                    <el-input v-model="passwordForm.currentPassword" type="password" show-password />
                </el-form-item>
                <el-form-item label="新密码" prop="newPassword">
                    <el-input v-model="passwordForm.newPassword" type="password" show-password />
                    <div class="password-strength">
                        <div class="strength-bar" :class="passwordStrengthClass"></div>
                        <span class="strength-text">密码强度：{{ passwordStrengthText }}</span>
                    </div>
                </el-form-item>
                <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="passwordDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="changePassword">确认修改</el-button>
            </template>
        </el-dialog>

        <!-- 更换头像对话框 -->
        <el-dialog v-model="avatarDialogVisible" title="更换头像" width="50%" :fullscreen="isMobile" :close-on-click-modal="false">
            <div class="avatar-edit-container">
                <div class="avatar-preview">
                    <div class="preview-wrapper">
                        <img :src="avatarPreviewUrl" v-if="avatarPreviewUrl" class="preview-image" />
                        <el-icon v-else class="preview-placeholder"><User /></el-icon>
                    </div>
                    <div class="preview-actions">
                        <el-button type="primary" size="small" @click="handleAvatarUpload">
                            <el-icon><Upload /></el-icon> 上传图片
                        </el-button>
                        <el-button size="small" @click="avatarPreviewUrl = ''">
                            <el-icon><Refresh /></el-icon> 重置
                        </el-button>
                    </div>
                </div>
                <div class="avatar-selector">
                    <h4>系统头像</h4>
                    <div class="default-avatars">
                        <div 
                            v-for="(avatar, index) in defaultAvatars" 
                            :key="index" 
                            class="default-avatar-item"
                            :class="{active: avatarPreviewUrl === avatar}"
                            @click="avatarPreviewUrl = avatar"
                        >
                            <img :src="avatar" />
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="avatarDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="saveAvatar">保存</el-button>
            </template>
        </el-dialog>

        <!-- 隐藏的文件上传input -->
        <input 
            type="file" 
            ref="avatarUploadInput" 
            accept="image/*" 
            style="display: none" 
            @change="handleAvatarChange"
        />
    </div>
</template>

<script setup>
    import { ref, reactive, computed, onMounted } from 'vue'
    import { 
    Edit, Lock, Camera, User, Iphone, Message, OfficeBuilding, 
    Postcard, Upload, Refresh, VideoPlay, Setting
    } from '@element-plus/icons-vue'
    import { useWindowSize } from '@vueuse/core'
    import { ElMessage } from 'element-plus'

    // 响应式窗口大小
    const { width } = useWindowSize()
    const isMobile = computed(() => width.value < 768)

    // 用户信息
    const userInfo = reactive({
        id: 'U20230001',
        nickname: '星辰大海',
        name: '张伟',
        gender: '男',
        phone: '13800138000',
        email: 'zhangwei@example.com',
        department: '技术研发中心',
        role: '高级前端工程师',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        registerTime: '2023-01-15 10:30:45',
        lastLogin: '2023-06-20 14:25:36'
    })

    // 部门选项
    const departments = [
        { value: '技术研发中心', label: '技术研发中心' },
        { value: '产品设计部', label: '产品设计部' },
        { value: '市场运营部', label: '市场运营部' },
        { value: '人力资源部', label: '人力资源部' },
        { value: '财务部', label: '财务部' },
        { value: '客户服务部', label: '客户服务部' }
    ]

    // 标签页控制
    const activeTab = ref('basic')

    // 消息通知数据
    const notifications = ref([
        { id: 1, title: '系统升级通知', content: '系统将于2023-06-25 00:00至06:00进行升级维护', type: 'system', time: '2023-06-20 09:15', read: false },
        { id: 2, title: '新的任务分配', content: '您有一个新的任务需要处理：首页改版设计', type: 'task', time: '2023-06-19 14:30', read: false },
        { id: 3, title: '审批通过', content: '您的请假申请已通过审批', type: 'approval', time: '2023-06-18 16:45', read: true },
        { id: 4, title: '安全提醒', content: '检测到您的账号在异地登录，如非本人操作请及时修改密码', type: 'security', time: '2023-06-17 22:10', read: true },
        { id: 5, title: '版本更新', content: '新版本v2.5.0已发布，包含多项功能优化和问题修复', type: 'system', time: '2023-06-16 10:20', read: true },
        { id: 6, title: '会议提醒', content: '您有一个会议安排在明天上午10:00，主题：项目进度汇报', type: 'reminder', time: '2023-06-15 17:30', read: true },
    ])

    // 消息类型配置
    const notificationTypes = {
        system: { name: '系统', icon: 'Setting', color: '#409EFF', tagType: '' },
        task: { name: '任务', icon: 'List', color: '#67C23A', tagType: 'success' },
        approval: { name: '审批', icon: 'DocumentChecked', color: '#E6A23C', tagType: 'warning' },
        security: { name: '安全', icon: 'Lock', color: '#F56C6C', tagType: 'danger' },
        reminder: { name: '提醒', icon: 'Bell', color: '#909399', tagType: 'info' },
        hr: { name: '人事', icon: 'UserFilled', color: '#8E44AD', tagType: '' },
        message: { name: '消息', icon: 'ChatDotRound', color: '#3498DB', tagType: '' }
    }

    // 操作日志数据
    const operationLogs = ref([
        { id: 1, time: '2023-06-20 14:25:36', module: '个人中心', action: '查看个人信息', ip: '192.168.1.100', status: '成功' },
        { id: 2, time: '2023-06-20 13:45:22', module: '项目管理', action: '创建新项目「后台管理系统」', ip: '192.168.1.100', status: '成功' },
        { id: 3, time: '2023-06-20 11:30:15', module: '任务管理', action: '完成任务「首页改版」', ip: '192.168.1.100', status: '成功' },
        { id: 4, time: '2023-06-19 16:20:45', module: '系统设置', action: '修改个人密码', ip: '192.168.1.100', status: '成功' },
        { id: 5, time: '2023-06-19 10:15:33', module: '文档中心', action: '上传文档「需求规格说明书」', ip: '192.168.1.100', status: '成功' },
        { id: 6, time: '2023-06-18 17:05:12', module: '审批流程', action: '提交请假申请', ip: '192.168.1.100', status: '成功' },
        { id: 7, time: '2023-06-18 09:40:56', module: '个人中心', action: '更新个人信息', ip: '192.168.1.100', status: '成功' },
        { id: 8, time: '2023-06-17 14:30:28', module: '项目管理', action: '删除项目「测试项目」', ip: '192.168.1.100', status: '成功' },
        { id: 9, time: '2023-06-16 16:15:19', module: '任务管理', action: '分配任务给团队成员', ip: '192.168.1.100', status: '成功' },
        { id: 10, time: '2023-06-16 11:20:42', module: '系统设置', action: '修改通知偏好设置', ip: '192.168.1.100', status: '成功' }
    ])

    // 分页控制
    const logPage = reactive({
        current: 1,
        size: 10,
        total: 35
    })

    // 编辑资料对话框
    const editDialogVisible = ref(false)
    const editFormRef = ref(null)
    const editForm = reactive({
        nickname: '',
        name: '',
        gender: '',
        phone: '',
        email: '',
        department: ''
    })

    const phonePrefix = ref('+86')

    const editRules = {
        nickname: [
            { required: true, message: '请输入昵称', trigger: 'blur' },
            { min: 2, max: 12, message: '长度在 2 到 12 个字符', trigger: 'blur' }
        ],
        name: [
            { required: true, message: '请输入姓名', trigger: 'blur' },
            { min: 2, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur' }
        ],
        gender: [
            { required: true, message: '请选择性别', trigger: 'change' }
        ],
        phone: [
            { required: true, message: '请输入手机号', trigger: 'blur' },
            { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        email: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        department: [
            { required: true, message: '请选择部门', trigger: 'change' }
        ]
        }

        // 修改密码对话框
        const passwordDialogVisible = ref(false)
        const passwordFormRef = ref(null)
        const passwordForm = reactive({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
    })

    const validatePassword = (rule, value, callback) => {
        if (value === passwordForm.currentPassword) {
            callback(new Error('新密码不能与当前密码相同'))
        } else {
            callback()
        }
    }

    const validateConfirmPassword = (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
            callback(new Error('两次输入的密码不一致'))
        } else {
            callback()
        }
    }

    const passwordRules = {
        currentPassword: [
            { required: true, message: '请输入当前密码', trigger: 'blur' },
            { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        newPassword: [
            { required: true, message: '请输入新密码', trigger: 'blur' },
            { min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' },
            { validator: validatePassword, trigger: 'blur' }
        ],
        confirmPassword: [
            { required: true, message: '请确认密码', trigger: 'blur' },
            { validator: validateConfirmPassword, trigger: 'blur' }
        ]
    }

    // 密码强度计算
    const passwordStrength = computed(() => {
        if (!passwordForm.newPassword) return 0
        
        let strength = 0
        const password = passwordForm.newPassword
        
        // 长度评估
        if (password.length >= 8) strength += 1
        if (password.length >= 12) strength += 1
        
        // 包含数字
        if (/\d/.test(password)) strength += 1
        
        // 包含小写字母
        if (/[a-z]/.test(password)) strength += 1
        
        // 包含大写字母
        if (/[A-Z]/.test(password)) strength += 1
        
        // 包含特殊字符
        if (/[^a-zA-Z0-9]/.test(password)) strength += 1
        
        return Math.min(strength, 5)
    })

    const passwordStrengthClass = computed(() => {
        const strength = passwordStrength.value
        if (strength <= 2) return 'weak'
        if (strength <= 4) return 'medium'
        return 'strong'
    })

    const passwordStrengthText = computed(() => {
        const strength = passwordStrength.value
        if (strength <= 2) return '弱'
        if (strength <= 4) return '中'
        return '强'
    })

    // 更换头像对话框
    const avatarDialogVisible = ref(false)
    const avatarUploadInput = ref(null)
    const avatarPreviewUrl = ref('')
    const defaultAvatars = ref([
        'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
        'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
        'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
        'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
    ])

    // 方法
    const showEditDialog = () => {
        Object.assign(editForm, {
            nickname: userInfo.nickname,
            name: userInfo.name,
            gender: userInfo.gender,
            phone: userInfo.phone,
            email: userInfo.email,
            department: userInfo.department
        })
        editDialogVisible.value = true
    }

    const saveProfile = () => {
        editFormRef.value.validate(valid => {
            if (valid) {
            Object.assign(userInfo, editForm)
            editDialogVisible.value = false
            ElMessage.success('个人信息更新成功')
            }
        })
    }

    const showPasswordDialog = () => {
        passwordFormRef.value?.resetFields()
        passwordDialogVisible.value = true
    }

    const changePassword = () => {
        passwordFormRef.value.validate(valid => {
            if (valid) {
            passwordDialogVisible.value = false
            ElMessage.success('密码修改成功，请重新登录')
            // 这里应该调用API修改密码，然后跳转到登录页
            }
        })
    }

    const showAvatarDialog = () => {
        avatarPreviewUrl.value = userInfo.avatar
        avatarDialogVisible.value = true
    }

    const handleAvatarUpload = () => {
        avatarUploadInput.value.click()
    }

    const handleAvatarChange = (e) => {
        const file = e.target.files[0]
        if (!file) return
        
        if (!file.type.startsWith('image/')) {
            ElMessage.error('请选择图片文件')
            return
        }
        
        if (file.size > 2 * 1024 * 1024) {
            ElMessage.error('图片大小不能超过2MB')
            return
        }
        
        const reader = new FileReader()
        reader.onload = (e) => {
            avatarPreviewUrl.value = e.target.result
        }
        reader.readAsDataURL(file)
        
        // 清空input，以便可以重复选择同一文件
        e.target.value = ''
        }

        const saveAvatar = () => {
        if (!avatarPreviewUrl.value) {
            ElMessage.warning('请选择或上传头像')
            return
        }
        
        userInfo.avatar = avatarPreviewUrl.value
        avatarDialogVisible.value = false
        ElMessage.success('头像更新成功')
    }

    const fetchOperationLogs = () => {
        // 这里应该是API调用获取分页日志
        ElMessage.info(`加载第${logPage.current}页操作日志`)
    }

    const goToNotificationPage = () => {
        ElMessage.info('跳转到消息列表页面')
        // 实际项目中应该是路由跳转
    }

    // 初始化
    onMounted(() => {
    })
</script>

<style scoped>
    .personal-center-container {
        /* max-width: 1200px; */
        margin: 0 auto;
        padding: 10px;
    }

    .profile-card {
        border-radius: 8px;
        overflow: hidden;
    }

    .profile-header {
        display: flex;
        padding: 30px;
        background: linear-gradient(135deg, #f6f9fc 0%, #b0c5d5 100%);
        position: relative;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }

    .avatar-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
    }

    .profile-avatar {
        border: 4px solid white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        flex-shrink: 0;
        transition: all 0.3s;
    }

    .profile-avatar:hover {
        transform: scale(1.05);
    }

    .avatar-edit-btn {
        width: 120px;
    }

    .profile-basic {
        flex: 1;
        max-width: 450px;
        /* min-width: 250px; */
    }

    .profile-name {
        font-size: 24px;
        margin: 0 0 10px;
        color: #303133;
        font-weight: 600;
    }

    .profile-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 15px;
    }

    .meta-item {
        display: flex;
        align-items: center;
        gap: 5px;
        color: #606266;
        font-size: 14px;
    }

    .profile-org {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }

    .org-tag {
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .profile-actions {
        flex-shrink: 0;
        display: flex;
        gap: 10px;
    }

    .profile-tabs {
        margin-top: 10px;
    }

    .info-section {
        padding: 20px;
    }

    .notification-section {
        padding: 10px;
    }

    .notification-card {
        margin-bottom: 10px;
        transition: all 0.3s;
        border-radius: 8px;
    }

    .notification-card.unread {
        background-color: #f5f9ff;
        border-left: 3px solid #409EFF;
    }

    .notification-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .notification-content {
        display: flex;
        gap: 15px;
    }

    .notification-icon {
        flex-shrink: 0;
        display: flex;
        align-items: center;
    }

    .notification-main {
        flex: 1;
    }

    .notification-main h4 {
        margin: 0 0 8px;
        font-size: 16px;
        color: #303133;
    }

    .notification-main p {
        margin: 0 0 8px;
        color: #606266;
        font-size: 14px;
        line-height: 1.5;
    }

    .notification-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 12px;
        color: #909399;
    }

    .view-more {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    .log-section {
        padding: 20px;
    }

    .pagination {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
    }

    /* 密码强度指示器 */
    .password-strength {
        margin-top: 8px;
        height: 6px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .strength-bar {
        height: 100%;
        flex: 1;
        border-radius: 3px;
        background-color: #ebeef5;
        overflow: hidden;
        position: relative;
    }

    .strength-bar::after {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: calc(v-bind(passwordStrength) * 20%);
        transition: all 0.3s;
    }

    .strength-bar.weak::after {
         background-color: #f56c6c;
    }

    .strength-bar.medium::after {
        background-color: #e6a23c;
    }

    .strength-bar.strong::after {
        background-color: #67c23a;
    }

    .strength-text {
        font-size: 12px;
        color: #909399;
    }

    /* 头像编辑 */
    .avatar-edit-container {
        display: flex;
        flex-direction: column;
        gap: 30px;
    }

    @media (min-width: 768px) {
        .avatar-edit-container {
            flex-direction: row;
        }
    }

    .avatar-preview {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
    }

    .preview-wrapper {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        background-color: #f5f7fa;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border: 1px dashed #dcdfe6;
    }

    .preview-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .preview-placeholder {
        font-size: 60px;
        color: #c0c4cc;
    }

    .preview-actions {
        display: flex;
        gap: 10px;
    }

    .avatar-selector {
        flex: 1;
    }

    .default-avatars {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }

    .default-avatar-item {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        overflow: hidden;
        cursor: pointer;
        border: 2px solid transparent;
        transition: all 0.3s;
    }

    .default-avatar-item:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .default-avatar-item.active {
        border-color: var(--el-color-primary);
    }

    .default-avatar-item img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .profile-header {
            flex-direction: column;
            text-align: center;
            padding: 20px;
        }
        
        .profile-basic {
            text-align: center;
        }
        
        .profile-meta {
            justify-content: center;
        }
        
        .profile-org {
            justify-content: center;
        }
        
        .profile-actions {
            width: 100%;
            justify-content: center;
        }
        
        .info-section {
            padding: 10px;
        }
        
        .notification-content {
            flex-direction: column;
        }
        
        .notification-icon {
            justify-content: center;
        }
    }
</style>