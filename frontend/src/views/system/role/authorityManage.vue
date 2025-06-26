<template>
    <div class="permission-container">
        <!-- 主内容区 -->
        <div class="permission-main">
            <!-- 左侧面板 -->
            <div class="left-panel">
                <!-- 角色选择卡片 -->
                <el-card class="panel-card" shadow="hover">
                <template #header>
                    <div class="card-header">
                        <div class="lyflexcenter">
                            <span style="margin-right:5px;">当前角色</span>
                            <el-tag size="small" type="primary" v-if="roleObj.name">
                                {{ roleObj.name }}
                            </el-tag>
                            <el-tag size="small" type="info" v-else>未选择</el-tag>
                        </div>
                        <el-button size="small" type="primary" @click="submitPermisson" :loading="saving" class="save-btn":disabled="!currentRole">保存</el-button>
                    </div>
                </template>
                <el-scrollbar>
                    <el-tree
                    class="role-tree"
                    :data="roleTreeData"
                    :props="{ label: 'name' }"
                    :highlight-current="true"
                    node-key="node_id"
                    default-expand-all
                    @node-click="nodeClick"
                    ref="roleTree"
                    />
                </el-scrollbar>
                </el-card>

                <!-- 数据范围授权卡片 -->
                <el-card class="panel-card" shadow="hover">
                    <template #header>
                        <div class="card-header">
                            <span>全局数据授权</span>
                            <el-tooltip content="全局授权用户可操作的数据范围" placement="top">
                                <el-icon><QuestionFilled /></el-icon>
                            </el-tooltip>
                        </div>
                    </template>
                    <el-select
                        v-model="roleObj.data_range"
                        @change="dataScopeSelectChange"
                        placeholder="选择数据范围"
                        :disabled="!roleObj.name"
                        class="data-scope-select"
                    >
                        <el-option
                        v-for="item in dataScopeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        />
                    </el-select>
                    
                    <div class="dept-tree-container" v-show="roleObj.data_range === 4">
                        <el-tree
                        class="dept-tree"
                        :data="deptOptions"
                        show-checkbox
                        default-expand-all
                        :default-checked-keys="deptCheckedKeys"
                        ref="deptTree"
                        node-key="id"
                        :props="{ label: 'name', children: 'children', disabled: 'disabled' }"
                        :disabled="!roleObj.name"
                        />
                    </div>
                </el-card>
            </div>

            <!-- 右侧面板 -->
            <div class="right-panel">
                <!-- 菜单权限卡片 -->
                <el-card class="panel-card" shadow="hover">
                    <template #header>
                        <div class="card-header">
                            <span>菜单/按钮授权</span>
                            <el-tooltip content="授权用户在菜单中可操作的范围,选择菜单、数据权限、按钮权限" placement="top">
                                <el-icon><QuestionFilled /></el-icon>
                            </el-tooltip>
                        </div>
                    </template>
                    <el-scrollbar v-loading="loadingPage" always>
                        <el-empty description="请先选择角色" v-if="!roleObj.name" />
                        <el-tree
                            v-else
                            class="menu-permission-tree"
                            ref="menuTree"
                            :data="menuOptions"
                            node-key="id"
                            default-expand-all
                            show-checkbox
                            :check-on-click-node="false"
                            :expand-on-click-node="false"
                            :default-checked-keys="menuCheckedKeys"
                            :check-strictly="true"
                            @check-change="handleCheckClick"
                        >
                            <template #default="{ node, data }">
                                <div class="menu-node-container">
                                    <div class="menu-node-header" :style="{width:((4-node.level)*18+220)+'px'}">
                                        <span class="menu-name">{{ data.name }}</span>
                                        <el-select
                                        v-if="data.type === 1"
                                        v-model="data.data_range"
                                        @change="dataScopeMenuSelectChange"
                                        size="small"
                                        class="menu-data-scope-select"
                                        >
                                        <el-option
                                            v-for="item in dataScopeOptionsMenu"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value"
                                        />
                                        </el-select>
                                    </div>
                                    
                                    <div class="button-permissions" v-if="data.menuPermission && data.menuPermission.length">
                                        <el-tag type="info" size="small">按钮权限:</el-tag>
                                        <el-checkbox-group v-model="data.menuPermissionChecked">
                                            <el-checkbox
                                                v-for="item in data.menuPermission"
                                                :key="item.id"
                                                :label="item.id"
                                                class="button-checkbox"
                                            >
                                                {{ item.name }}
                                            </el-checkbox>
                                        </el-checkbox-group>
                                    </div>
                                </div>
                            </template>
                        </el-tree>
                    </el-scrollbar>
                </el-card>

                <!-- 列权限卡片 -->
                <el-card class="panel-card" shadow="hover">
                    <template #header>
                        <div class="card-header">
                        <span>列权限</span>
                        <el-tooltip content="配置表格列可见性和可编辑性" placement="top">
                            <el-icon><QuestionFilled /></el-icon>
                        </el-tooltip>
                        </div>
                    </template>
                    <el-scrollbar v-loading="loadingPage">
                        <el-empty description="请先选择角色" v-if="!roleObj.name" />
                        <div v-else>
                        <el-table
                            :data="columnData"
                            style="width: 100%"
                            class="column-permission-table"
                            :row-class-name="tableRowClassName"
                        >
                            <el-table-column prop="name" label="列名" width="120" />
                            <el-table-column prop="code" label="编码" width="120" />
                            <el-table-column label="所属菜单" width="150">
                            <template #default="{ row }">
                                <el-tag size="small">{{ getMenuName(row.menuId) }}</el-tag>
                            </template>
                            </el-table-column>
                            <el-table-column label="可见" width="80">
                            <template #default="{ row }">
                                <el-switch
                                v-model="row.visible"
                                :disabled="!hasMenuPermission(row.menuId)"
                                active-color="#13ce66"
                                />
                            </template>
                            </el-table-column>
                            <el-table-column label="可编辑" width="90">
                            <template #default="{ row }">
                                <el-switch
                                v-model="row.editable"
                                :disabled="!row.visible || !hasMenuPermission(row.menuId)"
                                active-color="#13ce66"
                                />
                            </template>
                            </el-table-column>
                            <el-table-column label="操作" width="120">
                            <template #default="{ row }">
                                <el-button
                                size="small"
                                @click="editColumnConfig(row)"
                                :disabled="!hasMenuPermission(row.menuId)"
                                >
                                高级配置
                                </el-button>
                            </template>
                            </el-table-column>
                        </el-table>
                        </div>
                    </el-scrollbar>
                </el-card>
            </div>
        </div>

        <!-- 移动端底部操作栏 -->
        <div class="mobile-footer">
            <el-button
                type="primary"
                :icon="Check"
                @click="submitPermisson"
                :loading="saving"
                class="save-btn"
                round
                :disabled="!currentRole"
            >
                保存配置
            </el-button>
        </div>

        <!-- 列高级配置对话框 -->
        <el-dialog v-model="columnConfigDialogVisible" title="列高级配置" width="600px">
            <el-form :model="currentColumnConfig" label-width="120px">
                <el-form-item label="列名">
                <el-input v-model="currentColumnConfig.name" disabled />
                </el-form-item>
                <el-form-item label="编码">
                <el-input v-model="currentColumnConfig.code" disabled />
                </el-form-item>
                <el-form-item label="可见">
                <el-switch v-model="currentColumnConfig.visible" active-color="#13ce66" />
                </el-form-item>
                <el-form-item label="可编辑">
                <el-switch v-model="currentColumnConfig.editable" :disabled="!currentColumnConfig.visible" active-color="#13ce66" />
                </el-form-item>
                <el-form-item label="导出权限">
                <el-switch v-model="currentColumnConfig.exportable" active-color="#13ce66" />
                </el-form-item>
                <el-form-item label="导入权限">
                <el-switch v-model="currentColumnConfig.importable" active-color="#13ce66" />
                </el-form-item>
                <el-form-item label="验证规则">
                <el-select v-model="currentColumnConfig.validationRules" multiple placeholder="选择验证规则">
                    <el-option label="必填" value="required" />
                    <el-option label="数字" value="numeric" />
                    <el-option label="邮箱" value="email" />
                    <el-option label="手机号" value="phone" />
                </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="columnConfigDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="saveColumnConfig">保存</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted, watch } from 'vue'
    import { Check, Lock, QuestionFilled } from '@element-plus/icons-vue'
    import { ElMessage } from 'element-plus'
    import XEUtils from 'xe-utils'
    import Api from "@/api/api.js"

    // 响应式数据
    const currentRole = ref(null)
    const roleList = ref([])
    const roleTreeData = ref([])
    const roleObj = ref({ name: null, data_range: null })
    const menuOptions = ref([])
    const menuCheckedKeys = ref([])
    const deptOptions = ref([])
    const deptCheckedKeys = ref([])
    const loadingPage = ref(false)
    const saving = ref(false)
    const roleTree = ref(null)
    const menuTree = ref(null)
    const deptTree = ref(null)
    const columnData = ref([])
    const columnConfigDialogVisible = ref(false)
    const currentColumnConfig = ref({
        id: '',
        name: '',
        code: '',
        menuId: '',
        visible: false,
        editable: false,
        exportable: false,
        importable: false,
        validationRules: []
    })

    // 数据范围选项
    const dataScopeOptions = [
        { value: 0, label: '仅本人数据权限' },
        { value: 1, label: '本部门数据权限' },
        { value: 2, label: '本部门及以下数据权限' },
        { value: 3, label: '全部数据权限' },
        { value: 4, label: '自定义数据权限' }
    ]

    const dataScopeOptionsMenu = [
        { value: 0, label: '仅本人数据权限' },
        { value: 1, label: '本部门数据权限' },
        { value: 2, label: '本部门及以下数据权限' },
        { value: 3, label: '全部数据权限' },
        { value: 5, label: '同全局数据权限' }
    ]

    // 计算属性
    const hasChanges = computed(() => {
        // 实现变更检测逻辑
        return true
    })

    // 生命周期钩子
    onMounted(() => {
        fetchRoleList()
    })

    // 方法
    const fetchRoleList = async () => {
        try {
            loadingPage.value = true
            const res = await Api.apiSystemRole({ page: 1, limit: 999 })
            roleList.value = res.data.data
            roleTreeData.value = res.data.data.map((item, index) => {
                return { ...item, node_id: index }
            })
            
            // 如果有历史选中的角色，自动选中
            if (history.state.id) {
            const selectedRole = roleTreeData.value.find(role => role.id.toString() === history.state.id.toString())
            if (selectedRole) {
                currentRole.value = selectedRole.id
                handleRoleChange(selectedRole.id)
            }
            }
        } catch (error) {
            ElMessage.error('获取角色列表失败')
            console.error('获取角色列表失败:', error)
        } finally {
            loadingPage.value = false
        }
    }

    const handleRoleChange = (roleId) => {
        const selectedRole = roleList.value.find(role => role.id === roleId)
        if (selectedRole) {
            roleObj.value = { ...selectedRole }
            fetchMenuData(selectedRole)
            fetchDeptData()
            fetchColumnPermissions(roleId)
        }
    }

    const fetchMenuData = async (role) => {
        try {
            loadingPage.value = true
            const res = await Api.apiSystemRoleIdToMenuid(role.id)
            
            // 处理菜单数据
            const menuData = res.data.map(menu => {
            // 处理按钮权限选中状态
            const menuPermissionChecked = []
            menu.menuPermission.forEach(btn => {
                if (role.permission && role.permission.includes(parseInt(btn.id))) {
                    menuPermissionChecked.push(btn.id)
                }
            })
            
            // 处理数据范围
            let dataRange = 5 // 默认同全局
            if (role.menuDataRange) {
                const range = role.menuDataRange.find(item => item.menu_id.toString() === menu.id.toString())
                if (range) dataRange = range.data_range
            }
            
            return {
                ...menu,
                data_range: dataRange,
                menuPermissionChecked
            }
            })
            
            // 转换为树形结构
            menuOptions.value = XEUtils.toArrayTree(menuData, { parentKey: 'parent' })
            menuCheckedKeys.value = role.menu || []
        } catch (error) {
            ElMessage.error('获取菜单权限失败')
            console.error('获取菜单权限失败:', error)
        } finally {
            loadingPage.value = false
        }
    }

    const fetchDeptData = async () => {
        try {
            const res = await Api.apiSystemDept({ page: 1, limit: 9999 })
            // 处理部门数据为树形结构
            deptOptions.value = XEUtils.toArrayTree(
            res.data.data.map(item => ({ ...item, disabled: false })),
            { parentKey: 'parent', strict: false }
            )
            deptCheckedKeys.value = roleObj.value.dept || []
        } catch (error) {
            ElMessage.error('获取部门数据失败')
            console.error('获取部门数据失败:', error)
        }
    }

    const fetchColumnPermissions = async (roleId) => {
        try {
            loadingPage.value = true
            const res = await apiGetColumnPermissions(roleId)
            columnData.value = res.data.data || []
        } catch (error) {
            ElMessage.error('获取列权限失败')
            console.error('获取列权限失败:', error)
        } finally {
            loadingPage.value = false
        }
    }

    const nodeClick = (data) => {
        currentRole.value = data.id
        roleObj.value = data
        fetchMenuData(data)
        fetchDeptData()
        fetchColumnPermissions(data.id)
    }

    const dataScopeSelectChange = (value) => {
        if (value !== 4) {
            deptCheckedKeys.value = []
        }
    }

    const dataScopeMenuSelectChange = (value) => {
    // 处理菜单数据范围变更
    }

    const handleCheckClick = (data, checked) => {
        const { menuPermission, children } = data
        if (menuPermission) {
            data.menuPermissionChecked = checked ? menuPermission.map(btn => btn.id) : []
        }
        if (children) {
            children.forEach(item => {
            menuTree.value.setChecked(item.id, checked)
            })
        }
    }

    const getMenuAllCheckedKeys = () => {
        const checkedKeys = menuTree.value?.getCheckedKeys() || []
        const halfCheckedKeys = menuTree.value?.getHalfCheckedKeys() || []
        return [...checkedKeys, ...halfCheckedKeys]
    }

    const getDeptAllCheckedKeys = () => {
        const checkedKeys = deptTree.value?.getCheckedKeys() || []
        const halfCheckedKeys = deptTree.value?.getHalfCheckedKeys() || []
        return [...checkedKeys, ...halfCheckedKeys]
    }

    const getMenuDataRangeChecked = () => {
        const checkedMenuNodes = menuTree.value?.getCheckedNodes() || []
        return checkedMenuNodes.map(node => ({
            menu_id: node.id,
            menu_name: node.name,
            data_range: node.data_range
        }))
    }

    const hasMenuPermission = (menuId) => {
        return menuCheckedKeys.value.includes(menuId)
    }

    const getMenuName = (menuId) => {
        const menu = XEUtils.findTree(menuOptions.value, item => item.id === menuId)
        return menu ? menu.item.name : '未知菜单'
    }

    const tableRowClassName = ({ row }) => {
        return !hasMenuPermission(row.menuId) ? 'disabled-row' : ''
    }

    const editColumnConfig = (row) => {
        currentColumnConfig.value = { ...row }
        columnConfigDialogVisible.value = true
    }

    const saveColumnConfig = async () => {
        // 更新列数据
        const index = columnData.value.findIndex(col => col.id === currentColumnConfig.value.id)
        if (index !== -1) {
            columnData.value[index] = { ...currentColumnConfig.value }
        }
        columnConfigDialogVisible.value = false
    }

    const submitPermisson = async () => {
        if (!currentRole.value) {
            ElMessage.warning('请先选择角色')
            return
        }

        saving.value = true
        try {
            // 准备菜单权限数据
            const menuData = XEUtils.toTreeArray(menuOptions.value)
            const permissionData = []
            menuData.forEach(menu => {
            if (menu.menuPermissionChecked && menu.menuPermissionChecked.length > 0) {
                permissionData.push(...menu.menuPermissionChecked)
            }
            })

            // 准备角色数据
            const roleData = {
            ...roleObj.value,
            menu: getMenuAllCheckedKeys(),
            dept: getDeptAllCheckedKeys(),
            permission: permissionData,
            menuDataRange: getMenuDataRangeChecked()
            }

            // 保存角色权限
            const res = await apiPermissionSave(roleData)
            if (res.code === 2000) {
            // 保存列权限
            await apiSaveColumnPermissions({
                roleId: currentRole.value,
                columns: columnData.value
            })
            
            ElMessage.success('权限保存成功')
            history.state.id = roleObj.value.id
            fetchRoleList()
            } else {
            ElMessage.warning(res.msg)
            }
        } catch (error) {
            ElMessage.error('保存权限失败')
            console.error('保存权限失败:', error)
        } finally {
            saving.value = false
        }
    }
</script>

<style lang="scss" scoped>
    .permission-container {
        display: flex;
        flex-direction: column;
        height:calc(100vh - 78px);
        padding: 10px;
    }

    .permission-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        flex-wrap: wrap;
        gap: 10px;
    }

    .permission-header h2 {
        margin: 0;
        font-size: 1.5rem;
        color: var(--el-text-color-primary);
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .header-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .role-select {
        width: 240px;
    }

    .save-btn {
        --el-button-hover-bg-color: var(--el-color-primary-light-3);
        --el-button-active-bg-color: var(--el-color-primary-dark-2);
    }

    .permission-main {
        display: flex;
        flex: 1;
        gap: 10px;
        overflow: hidden;
    }

    .left-panel {
        width: 300px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .right-panel {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .panel-card {
        height: 100%;
        display: flex;
        flex-direction: column;
        border-radius: 6px;
        overflow: hidden;
        min-width: 240px;
    }

    .panel-card :deep(.el-card__header) {
        border-bottom: 1px solid var(--el-border-color-light);
        padding: 14px 20px;
    }

    .panel-card :deep(.el-card__body) {
        flex: 1;
        padding: 0;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .card-header span {
        font-weight: 500;
        color: var(--el-text-color-primary);
    }

    .role-tree {
        padding: 8px;
    }

    .data-scope-select {
        width: 100%;
        padding:10px;
    }

    .dept-tree-container {
        flex: 1;
        overflow: hidden;
    }

    .dept-tree {
        padding: 8px;
    }

    .menu-permission-tree {
        padding: 8px;
        flex: 1;
    }

    .menu-node-container {
        width: 100%;
        padding: 8px 0;
        display:flex;
        align-items:center;
    }

    .menu-node-header {
        display: flex;
        align-items: center;
        min-height: 32px;
        margin-bottom: 4px;
    }

    .menu-name {
        font-weight: 500;
        color: var(--el-text-color-primary);
        flex: 1;
        min-width: 0;
        white-space: nowrap;
        line-height: 32px; /* 设置固定行高 */
    }

    .menu-data-scope-select {
        width: 150px;
        /* 确保选择框高度与其他元素一致 */
        :deep(.el-input__wrapper) {
            height: 32px;
            padding-top: 1px;
            padding-bottom: 1px;
        }
        :deep(.el-input__inner) {
            height: 30px;
            line-height: 30px;
        }
    }

    .button-permissions {
        display: flex;
        align-items: center;
        gap: 8px;
        padding-left: 24px;
    }

    .button-checkbox {
        margin-right: 8px;
    }

    .column-permission-table {
        :deep(.disabled-row) {
            opacity: 0.6;
            pointer-events: none;
            
            .el-switch {
                opacity: 0.6;
            }
        }
    }

    .mobile-footer {
        display: none;
        padding: 12px 16px;
        background: var(--el-bg-color);
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }

    /* 响应式设计 */
    @media (max-width: 992px) {
        .permission-main {
            flex-direction: column;
        }
        
        .left-panel {
            width: 100%;
            flex-direction: row;
        }
        
        .left-panel > .panel-card {
            width: 50%;
        }
    }

    @media (max-width: 768px) {
        .permission-header {
            flex-direction: column;
            align-items: stretch;
        }
        
        .header-actions {
            flex-direction: column;
            align-items: stretch;
        }
        
        .role-select {
            width: 100%;
        }
        
        .left-panel {
            flex-direction: column;
        }
        
        .left-panel > .panel-card {
            width: 100%;
        }
        
        .save-btn {
            display: none;
        }
        
        .mobile-footer {
            display: block;
        }
    }

    /* 暗黑模式适配 */
    @media (prefers-color-scheme: dark) {
        .permission-container {
            background-color: var(--el-bg-color-page);
        }
        
        .panel-card :deep(.el-card__header) {
            background-color: var(--el-fill-color-dark);
        }
        
        .mobile-footer {
            background: var(--el-bg-color-overlay);
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
        }
    }
</style>