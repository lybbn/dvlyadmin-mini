<template>
    <div class="permission-container">
        <!-- 主内容区 -->
        <div class="permission-main">
            <!-- 右侧面板 -->
            <div class="right-panel">
                <!-- 菜单权限卡片 -->
                <el-card class="panel-card" shadow="hover">
                    <template #header>
                        <div class="card-header">
                            <div class="permission-header">
                                <span>当前角色</span>
                                <div class="header-actions">
                                    <el-select v-model="currentRole" placeholder="选择角色" class="role-select" @change="handleRoleChange" style="width:200px;">
                                        <el-option
                                            v-for="role in roleList"
                                            :key="role.id"
                                            :label="role.name"
                                            :value="role.id"
                                        />
                                    </el-select>
                                    <el-button type="primary" :icon="Check" @click="savePermissions" :loading="saving" class="save-btn">
                                    保存配置
                                    </el-button>
                                </div>
                            </div>
                            <el-tooltip content="授权用户在菜单中可操作的范围,选择菜单、数据权限、按钮权限、列权限（点击菜单配置）" placement="top">
                                <el-icon><QuestionFilled /></el-icon>
                            </el-tooltip>
                        </div>
                    </template>
                    <el-scrollbar v-loading="loadingPage" always class="tree-scroll-container">
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
                            :check-on-click-leaf="false"
                            @node-click="handleNodeClick"
                            @check-change="handleCheckClick"
                        >
                            <template #default="{ node, data }">
                                <div class="menu-node-container">
                                    <div class="menu-node-header" :style="{width:((4-node.level)*18+210)+'px'}">
                                        <span class="menu-name">{{ data.name }}</span>
                                        <el-select
                                        @click.stop=""
                                        v-if="data.type === 1"
                                        v-model="data.data_scope"
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
                                    
                                    <div class="button-permissions" v-if="data.type === 1&&data.menu_buttons && data.menu_buttons.length">
                                        <el-tag type="info" size="small">按钮权限:</el-tag>
                                        <el-checkbox-group v-model="data.menuPermissionChecked">
                                            <el-checkbox
                                                @click.stop=""
                                                v-for="item in data.menu_buttons"
                                                :key="item.id"
                                                :label="item.name"
                                                :value="item.id"
                                                class="button-checkbox"
                                            >
                                            </el-checkbox>
                                        </el-checkbox-group>
                                    </div>
                                </div>
                            </template>
                        </el-tree>
                    </el-scrollbar>
                </el-card>

                <!-- 列权限卡片 -->
                <el-drawer v-model="feildDrawer" direction="rtl" size="50%" class="lydrawer">
                    <template #header>
                        <div class="lyflexcenter">
                            <h4>列权限-</h4>
                            <el-tooltip content="配置表格列可见性和可编辑性" placement="bottom">
                                <el-icon><QuestionFilled /></el-icon>
                            </el-tooltip>
                        </div>
                    </template>
                    <template #default>
                        <el-scrollbar v-loading="loadingPage">
                            <el-empty description="请先选择角色" v-if="!roleObj.name" />
                            <div style="padding:10px;" v-else>
                                <el-table
                                :data="columnData"
                                style="width: 100%"
                                :row-class-name="tableRowClassName"
                                @select-all="handleSelectAll"
                                >
                                    <el-table-column prop="title" label="列名" min-width="120" />
                                    <el-table-column prop="field_name" label="字段" min-width="120" />
                                    
                                    <!-- 可见列 - 带表头复选框 -->
                                    <el-table-column label="列可见" min-width="80">
                                        <template #header>
                                        <el-checkbox
                                            v-model="allVisibleSelected"
                                            :indeterminate="isIndeterminateVisible"
                                            @change="toggleAllVisible"
                                        >可见</el-checkbox>
                                        </template>
                                        <template #default="{ row }">
                                        <el-checkbox
                                            v-model="row.visible"
                                            @change="updateVisibleSelection"
                                        />
                                        </template>
                                    </el-table-column>
                                    
                                    <!-- 可编辑列 - 带表头复选框 -->
                                    <el-table-column label="可编辑" min-width="90">
                                        <template #header>
                                        <el-checkbox
                                            v-model="allEditableSelected"
                                            :indeterminate="isIndeterminateEditable"
                                            @change="toggleAllEditable"
                                        >可编辑</el-checkbox>
                                        </template>
                                        <template #default="{ row }">
                                        <el-checkbox
                                            v-model="row.editable"
                                            @change="updateEditableSelection"
                                        />
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                        </el-scrollbar>
                    </template>
                    <template #footer>
                        <el-button @click="feildDrawer=false">取消</el-button>
                        <el-button type="primary" @click="confirmClick">确认</el-button>
                    </template>
                </el-drawer>
            </div>
        </div>
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
    let currentMenu = ref(null)
    const roleList = ref([])
    const roleTreeData = ref([])
    const roleObj = ref({ name: null, data_scope: null })
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
    let feildDrawer = ref(false)
    // 数据范围选项
    const dataScopeOptions = [
        { value: 0, label: '仅本人数据权限' },
        { value: 1, label: '本部门数据权限' },
        { value: 2, label: '本部门及以下数据权限' },
        { value: 3, label: '自定义部门数据权限' },
        { value: 4, label: '全部数据权限' }
    ]

    const dataScopeOptionsMenu = [
        { value: 0, label: '仅本人数据权限' },
        { value: 1, label: '本部门数据权限' },
        { value: 2, label: '本部门及以下数据权限' },
        { value: 4, label: '全部数据权限' },
        { value: 5, label: '同全局数据权限' }
    ]

    const allVisibleSelected = ref(false);
    const isIndeterminateVisible = ref(false);
    const allEditableSelected = ref(false);
    const isIndeterminateEditable = ref(false);

    // 切换所有可见状态
    const toggleAllVisible = (val) => {
        columnData.value.forEach(row => {
            row.visible = val;
        });
        updateVisibleSelection();
    };

    // 切换所有可编辑状态
    const toggleAllEditable = (val) => {
        columnData.value.forEach(row => {
            if(row.visible) {
                row.editable = val;
            }
        });
        updateEditableSelection();
    };

    // 更新可见选择状态
    const updateVisibleSelection = () => {
        const visibleRows = columnData.value.filter(row => row.visible);
        allVisibleSelected.value = visibleRows.length === columnData.value.length;
        isIndeterminateVisible.value = visibleRows.length > 0 && visibleRows.length < columnData.value.length;
        
        // 如果取消可见，同时取消可编辑
        if(!allVisibleSelected.value) {
            toggleAllEditable(false);
        }
    };

    // 更新可编辑选择状态
    const updateEditableSelection = () => {
        const editableRows = columnData.value.filter(row => row.editable);
        allEditableSelected.value = editableRows.length === columnData.value.filter(row => row.visible).length;
        isIndeterminateEditable.value = editableRows.length > 0 && editableRows.length < columnData.value.filter(row => row.visible).length;
    };

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
            menu.menu_buttons.forEach(btn => {
                if (role.permission && role.permission.includes(parseInt(btn.id))) {
                    menuPermissionChecked.push(btn.id)
                }
            })
            
            // 处理数据范围
            let dataRange = 5 // 默认同全局
            if (role.menuDataRange) {
                const range = role.menuDataRange.find(item => item.menu_id.toString() === menu.id.toString())
                if (range) dataRange = range.data_scope
            }
            
            return {
                ...menu,
                data_scope: dataRange,
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
        // fetchColumnPermissions(data.id)
    }

    const dataScopeSelectChange = (value) => {
        if (value !== 4) {
            deptCheckedKeys.value = []
        }
    }

    const dataScopeMenuSelectChange = (value) => {
    // 处理菜单数据范围变更
    }

    function handleNodeClick(data, node, component){
        if(data.type == 1){
            currentMenu.value = data
            columnData.value = data?.menu_fields || []
            feildDrawer.value = true
        }
    }

    const handleCheckClick = (data, checked) => {
        const { menu_buttons, children } = data
        if (menu_buttons) {
            data.menuPermissionChecked = checked ? menu_buttons.map(btn => btn.id) : []
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
            data_scope: node.data_scope
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

    .tree-scroll-container {
        width: 100%;
        height: 100%;
        
        /* 关键样式 - 使滚动容器可以水平滚动 */
        :deep(.el-scrollbar__wrap) {
            overflow-x: auto;
            overflow-y: hidden;
        }
        
        :deep(.el-scrollbar__view) {
            min-width: 100%;
            display: inline-block;
        }
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
        flex-shrink: 0;
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
            align-items: center;
            display:flex;
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

    }
</style>