<template>
    <div class="personal-center-container">
        <el-card shadow="hover" class="profile-card" v-loading="loadingPage">
            <!-- 头部信息区 -->
            <div class="profile-header">
                <div class="avatar-section">
                    <el-avatar :size="120" :src="userInfo.avatar || defaultAvatar" class="profile-avatar">
                        <!-- <span v-if="!userInfo.avatar">{{ userInfo.name.charAt(0).toUpperCase() }}</span> -->
                    </el-avatar>
                    <el-button type="primary" size="small" @click="showAvatarDialog" class="avatar-edit-btn" v-auth="'UpdateAvatar'">
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
                            <span>{{ userInfo.mobile || "无" }}</span>
                        </div>
                        <div class="meta-item">
                            <el-icon><Message /></el-icon>
                            <span>{{ userInfo.email || "无" }}</span>
                        </div>
                    </div>
                    <div class="profile-org">
                        <el-tag type="info" size="large" class="org-tag">
                            <el-icon><OfficeBuilding /></el-icon>
                            {{ userInfo.department }}
                        </el-tag>
                        <el-tag type="info" size="large" class="org-tag">
                            <el-icon><Postcard /></el-icon>
                            {{ rolenames }}
                        </el-tag>
                    </div>
                </div>
                
                <div class="profile-actions">
                    <el-button type="primary" @click="showEditDialog" round v-auth="'Update'">
                        <el-icon><Edit /></el-icon> 编辑资料
                    </el-button>
                    <el-button @click="showPasswordDialog" round v-auth="'ResetPass'">
                        <el-icon><Lock /></el-icon> 修改密码
                    </el-button>
                </div>
            </div>

            <!-- 内容标签页 -->
            <el-tabs v-model="activeTab" class="profile-tabs" @tab-change="handleTabClick">
                <el-tab-pane label="基本信息" name="basic">
                    <div class="info-section">
                        <el-descriptions :column="isMobile ? 1 : 2" border>
                            <el-descriptions-item label="用户ID">{{ userInfo.id }}</el-descriptions-item>
                            <el-descriptions-item label="昵称">{{ userInfo.nickname }}</el-descriptions-item>
                            <el-descriptions-item label="姓名">{{ userInfo.name }}</el-descriptions-item>
                            <el-descriptions-item label="性别">
                            <el-tag :type="userInfo.gender === 2 ? 'primary' : 'danger'">
                                {{ genderName }}
                            </el-tag>
                            </el-descriptions-item>
                            <el-descriptions-item label="手机号">{{ userInfo.mobile }}</el-descriptions-item>
                            <el-descriptions-item label="邮箱">{{ userInfo.email }}</el-descriptions-item>
                            <el-descriptions-item label="部门">{{ userInfo.department }}</el-descriptions-item>
                            <el-descriptions-item label="角色">{{ rolenames }}</el-descriptions-item>
                            <el-descriptions-item label="创建时间">{{ userInfo.create_datetime }}</el-descriptions-item>
                            <el-descriptions-item label="最后登录">{{ userInfo.last_login }}</el-descriptions-item>
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
                
                <el-tab-pane label="操作日志" name="logs" v-auth="'GetOPLog'">
                    <div class="log-section">
                        <el-table :data="tableData" style="width: 100%" border v-loading="loadingBPage">
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
                                        :placement="isMobile ? 'bottom' : 'left-start'"
                                        trigger="click"
                                        :width="isMobile ? '80%' : '50%'"
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
                                        :placement="isMobile ? 'bottom' : 'left-start'"
                                        trigger="click"
                                        :width="isMobile ? '80%' : '50%'"
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
                            <!-- <el-table-column width="130" prop="creator_name" label="操作人" /> -->
                            <el-table-column width="160" prop="create_datetime" label="创建时间" show-overflow-tooltip/>
                        </el-table>
                        
                        <div class="lypagination">
                            <Pagination v-bind:child-msg="pageparm" @callFather="callFather" :border="false" small position="right"/>
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
                            <el-radio :value="2">男</el-radio>
                            <el-radio :value="1">女</el-radio>
                            <el-radio :value="0">未知</el-radio>
                            </el-radio-group>
                        </el-form-item>
                    </el-col>
                    <el-col :span="isMobile ? 24 : 12">
                        <el-form-item label="手机号" prop="mobile">
                            <el-input v-model="editForm.mobile" placeholder="请输入手机号">
                            <!-- <template #prepend>
                                <el-select v-model="phonePrefix" style="width: 70px">
                                <el-option label="+86" value="+86" />
                                <el-option label="+852" value="+852" />
                                <el-option label="+853" value="+853" />
                                </el-select>
                            </template> -->
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="isMobile ? 24 : 12">
                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="editForm.email" placeholder="请输入邮箱" />
                        </el-form-item>
                    </el-col>
                    <!-- <el-col :span="isMobile ? 24 : 12">
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
                    </el-col> -->
                </el-row>
            </el-form>
            <template #footer>
                <el-button @click="editDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="saveProfile" :loading="loadingSave">保存</el-button>
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
                    <lyPasswordStrength v-model="passwordForm.newPassword"></lyPasswordStrength>
				    <div class="el-form-item-msg">请输入6-20位包含英文、数字的密码</div>
                </el-form-item>
                <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="passwordDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="changePassword" :loading="loadingSave">确认修改</el-button>
            </template>
        </el-dialog>

        <!-- 更换头像对话框 -->
        <el-dialog v-model="avatarDialogVisible" title="更换头像" width="50%" :fullscreen="isMobile" :close-on-click-modal="false">
            <div class="avatar-edit-container">
                <div class="avatar-preview">
                    <div class="preview-wrapper2">
                        <pictureSingleUpload v-model="avatarPreviewUrl"
                               :disabled="false" :round="true" :cropper="true"
                               title="" :show-file-list="false"
                               :width="120" :height="120"></pictureSingleUpload>
                    </div>
                    <div class="preview-actions">
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
                <el-button type="primary" @click="saveAvatar" :loading="loadingSave">保存</el-button>
            </template>
        </el-dialog>
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
    import {useUserState} from "@/store/userState";
    import defaultAvatar from '@/assets/lybbn/imgs/avatar.jpg'
    import Api from '@/api/api.js'
    import lyPasswordStrength from "@/components/password/lyPasswordStrength.vue";
    import pictureSingleUpload from '@/components/upload/single-picture.vue'
    import Pagination from '@/components/Pagination.vue'

    const userState = useUserState()
    // 响应式窗口大小
    const { width } = useWindowSize()
    const isMobile = computed(() => width.value < 768)
    let loadingPage = ref(false)
    // 用户信息
    const userInfo = ref({
        id: '',
        nickname: '',
        name: '',
        gender: 0,
        mobile: '',
        email: '',
        department: '',
        role: '',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        create_datetime: '',
        last_login: '',
        role_info:[]
    })

    // 性别
    const genderList = [
        { value: 0, label: '未知' },
        { value: 1, label: '女' },
        { value: 2, label: '男' },
    ]

    const genderName = computed(() => {
        const item = genderList.find(item => item.value === userInfo.value.gender)
        return item?.label || '未知'
    })

    const rolenames = computed(() => {
        return userInfo.value.role_info.map(user => user.name).join(',')
    })

    // 部门选项
    const departments = ref([])

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

    // 编辑资料对话框
    const editDialogVisible = ref(false)
    const editFormRef = ref(null)
    const editForm = reactive({
        nickname: '',
        name: '',
        gender: '',
        mobile: '',
        email: '',
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
        mobile: [
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

    // 密码校验 长度不能小于6位且不能大于20位字符,必须包含大写字母、小写字母、数字和特殊符号
	var pwdRegex =/^(?=.*[0-9])(?=.*[a-zA-Z]).{6,20}$/;
    // 密码校验
    const validatePassword = (rule, value, callback) => {
        if (value === passwordForm.currentPassword) {
            callback(new Error('新密码不能与当前密码相同'))
        }else if(!pwdRegex.test(passwordForm.newPassword)){
            callback(new Error("用户密码必须包含字母、数字"));
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
            { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        newPassword: [
            { required: true, message: '请输入新密码', trigger: 'blur' },
            { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
            { validator: validatePassword, trigger: 'blur' }
        ],
        confirmPassword: [
            { required: true, message: '请确认密码', trigger: 'blur' },
            { validator: validateConfirmPassword, trigger: 'blur' }
        ]
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
            nickname: userInfo.value.nickname,
            name: userInfo.value.name,
            gender: userInfo.value.gender,
            mobile: userInfo.value.mobile,
            email: userInfo.value.email
        })
        editDialogVisible.value = true
    }
    let loadingSave = ref(false)
    const saveProfile = async () => {
        try {
            // 首先验证表单
            const valid = await editFormRef.value.validate()
            if (valid) {
                // 发送API请求
                loadingSave.value = true
                const res = await Api.systemUserUserInfoEdit(editForm)
                loadingSave.value = false
                if (res.code === 2000) {
                    editDialogVisible.value = false
                    ElMessage.success('修改成功')
                    loadingPage.value = true
                    await userState.getSystemUserInfo()
                    userInfo.value = {...userState.userInfo} // 创建新对象触发响应式更新
                    loadingPage.value = false
                } else {
                    ElMessage.warning(res.msg)
                }
            }
        } catch (error) {
            // 处理验证错误或API请求错误
            ElMessage.error('保存失败:', error)
        }
    }

    const showPasswordDialog = () => {
        passwordFormRef.value?.resetFields()
        passwordDialogVisible.value = true
    }

    const changePassword = () => {
        passwordFormRef.value.validate(valid => {
            if (valid) {
                loadingSave.value = true
                Api.systemUserChangePassword(passwordForm).then(res=>{
                    loadingSave.value = false
                    if(res.code === 2000){
                        passwordDialogVisible.value = false
                        ElMessage.success('修改成功')
                    }else{
                        ElMessage.warning(res.msg)
                    }
                })
            }
        })
    }

    const showAvatarDialog = () => {
        avatarPreviewUrl.value = userInfo.value.avatar
        avatarDialogVisible.value = true
    }

    const saveAvatar = () => {
        if (!avatarPreviewUrl.value) {
            ElMessage.warning('请选择或上传头像')
            return
        }
        loadingSave.value = true
        Api.systemUserChangeAvatar({avatar:avatarPreviewUrl.value}).then(res => {
            loadingSave.value = false
            if (res.code == 2000) {
                userInfo.value.avatar = avatarPreviewUrl.value
                userState.userInfo.avatar = avatarPreviewUrl.value
                avatarDialogVisible.value = false
                ElMessage.success('头像更新成功')
            }else{
                ElMessage.warning(res.msg)
            }
        })
    }

    const goToNotificationPage = () => {
        ElMessage.info('跳转到消息列表页面')
        // 实际项目中应该是路由跳转
    }

    function getSystemUserInfo(){
        loadingPage.value = true
        Api.systemUserUserInfo().then(res => {
            loadingPage.value = false
            if (res.code == 2000) {
                userInfo.value = res.data
            }
        })
    }

    let loadingData = ref(false)
    let formInline = ref({
        page:1,
        limit:10
    })
    let pageparm = ref({
        page: 1,
        limit: 10,
        total: 0
    })
    let tableData = ref([])
    let loadingBPage = ref(false)
    const getLogsData = async () => {
        try {
            loadingBPage.value = true
            const res = await Api.getOwnerOperationLogs(formInline.value)
            if (res.code == 2000) {
                tableData.value = res.data.data
                pageparm.value.page = res.data.page
                pageparm.value.limit = res.data.limit
                pageparm.value.total = res.data.total
            }
        } finally {
            loadingBPage.value = false
        }
    }

    const callFather = (parm) => {
        formInline.value.page = parm.page
        formInline.value.limit = parm.limit
        getData()
    }

    function handleTabClick(e){
        if(e == "logs"){
            formInline.value.page = 1
            formInline.value.limit = 10
            tableData.value = []
            getLogsData()
        }
    }

    // 初始化
    onMounted(async () => {
        loadingPage.value = true
        await userState.getSystemUserInfo()
        userInfo.value = {...userState.userInfo} // 创建新对象触发响应式更新
        loadingPage.value = false
    })
</script>

<style lang="scss" scoped>
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
        :deep(.el-tag__content){
            display: flex;
            align-items: center;
        }
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
        padding-bottom:0px;
    }

    .pagination {
        width:100%;
        padding-right:20px;
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

    .preview-wrapper2{
        width: 160px;
        height: 160px;
        display: flex;
        align-items: center;
        justify-content: center;
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