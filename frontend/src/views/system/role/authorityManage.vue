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
                                    <el-button type="primary" :icon="Check" @click="submitPermisson" :loading="saving" class="save-btn" v-auth="'Save'">
                                    保存配置
                                    </el-button>
                                </div>
                            </div>
                            <el-tooltip raw-content content="<div>1、授权角色在菜单中可操作的范围、数据权限、按钮权限、列权限（点击配置）</div><div>2、数据权限支持具体按钮的配置，点击按钮后的settings配置即可</div><div>3、列权限如不可点击，则先需要在【菜单管理】中配置列权限</div>" placement="bottom">
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
                                    <div class="menu-node-header" :style="{width:((4-node.level)*18+280)+'px'}">
                                        <span class="menu-name">{{ data.name }}</span>
                                        <el-select
                                        @click.stop=""
                                        v-if="data.type === 1"
                                        v-model="data.data_scope"
                                        @change="dataScopeMenuSelectChange"
                                        size="small"
                                        class="menu-data-scope-select"
                                        :disabled="true"
                                        >
                                            <el-option
                                                v-for="item in dataScopeOptions"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.value"
                                            />
                                        </el-select>
                                        <el-button type="primary" size="small" :disabled="!isNodeChecked(data.id)" v-if="data.type === 1" @click.stop.prevent="handleMenuDataScopeClick(data)">数据权限</el-button>
                                    </div>
                                    <div class="button-permissions" v-if="data.type === 1">
                                        <el-button type="primary" :disabled="!data.menu_fields || data.menu_fields.length<1" size="small" @click.stop="handleFeildNodeClick(data)">列权限</el-button>
                                    </div>
                                    <div class="button-permissions" v-if="data.type === 1&&data.menu_buttons && data.menu_buttons.length" @click.stop.prevent="">
                                        <el-tag type="primary" size="small">按钮权限:</el-tag>
                                        <el-checkbox-group v-model="data.buttonPermissionChecked" @change="(val) => handleButtonPermissonChange(data, val)" @click.stop="">
                                            <el-checkbox
                                                v-for="item in data.menu_buttons"
                                                :key="item.id"
                                                :label="item.name"
                                                :value="item.id"
                                                class="button-checkbox"
                                            >
                                                <span @click.stop.prevent="">{{item.name}}</span>
                                                <el-icon @click.stop.prevent="handleJuDataScopeClick(item)" v-if="data.buttonPermissionChecked.includes(item.id)" style="margin-left:5px;"><Setting /></el-icon>
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
                            <h4>列权限{{"-"+currentMenu?.name}}</h4>
                            <el-tooltip content="配置表格列可见性和可编辑、可创建性" placement="bottom">
                                <el-icon><QuestionFilled /></el-icon>
                            </el-tooltip>
                        </div>
                    </template>
                    <template #default>
                        <el-scrollbar v-loading="loadingPage">
                            <el-empty description="请先选择角色" v-if="!roleObj.name" />
                            <div style="padding:10px;" v-else>
                                <el-table :data="columnData" style="width: 100%">
                                    <el-table-column prop="field_name" label="字段" min-width="120" />
                                    <el-table-column prop="title" label="列名" min-width="120" />
                                    <!-- 可见列 - 带表头复选框 -->
                                    <el-table-column label="列可见" min-width="80">
                                        <template #header>
                                        <el-checkbox
                                            v-model="allVisibleSelected"
                                            :indeterminate="isIndeterminateVisible"
                                            @change="toggleAllVisible"
                                        >列可见</el-checkbox>
                                        </template>
                                        <template #default="{ row }">
                                        <el-checkbox
                                            v-model="row.can_view"
                                            @change="updateVisibleSelection"
                                        />
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="可创建" min-width="90">
                                        <template #header>
                                            <el-checkbox
                                                v-model="allCreateableSelected"
                                                :indeterminate="isIndeterminateCreateable"
                                                @change="toggleAllCreateable"
                                            >可创建</el-checkbox>
                                        </template>
                                        <template #default="{ row }">
                                        <el-checkbox
                                            v-model="row.can_create"
                                            @change="updateCreateableSelection"
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
                                            v-model="row.can_update"
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
                        <el-button type="primary" @click="confirmFeildClick">确认</el-button>
                    </template>
                </el-drawer>
                <moduleDataScope ref="dataScopeDialogRef" @refreshData="handleConfirmDataScope" v-if="isDialogDataScopeVisible" @closed="isDialogDataScopeVisible = false"></moduleDataScope>
                <moduleMenuDataScope ref="menuDataScopeDialogRef" @refreshData="handleConfirmMenuDataScope" v-if="isDialogMenuDataScopeVisible" @closed="isDialogMenuDataScopeVisible = false"></moduleMenuDataScope>
            </div>
        </div>
    </div>
</template>

<script setup name="authorityManage">
    import { ref, computed, onMounted, nextTick } from 'vue'
    import { Check, Lock, QuestionFilled } from '@element-plus/icons-vue'
    import { ElMessage } from 'element-plus'
    import {deepClone,isEmpty} from "@/utils/util.js"
    import moduleDataScope from './components/moduleDataScope.vue'
    import moduleMenuDataScope from './components/moduleMenuDataScope.vue'
    import XEUtils from 'xe-utils'
    import Api from "@/api/api.js"

    // 响应式数据
    const currentRole = ref(null)
    let currentMenu = ref(null)
    let currentButton = ref(null)
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
        { value: 2, label: '本部门及以下' },
        { value: 3, label: '自定义部门数据权限' },
        { value: 4, label: '全部数据权限' }
    ]

    let allVisibleSelected = ref(false);
    let isIndeterminateVisible = ref(false);
    let allEditableSelected = ref(false);
    let allCreateableSelected = ref(false)
    let isIndeterminateEditable = ref(false);
    let isIndeterminateCreateable = ref(false)

    let dataScopeDialogRef = ref(null)
    let isDialogDataScopeVisible = ref(false)
    let menuDataScopeDialogRef = ref(null)
    let isDialogMenuDataScopeVisible = ref(false)

    function resetECU(){
        allVisibleSelected.value = false
        isIndeterminateVisible.value = false
        allEditableSelected.value = false
        allCreateableSelected.value = false
        isIndeterminateEditable.value = false
        isIndeterminateCreateable.value = false
    }

    // 切换所有可见状态
    const toggleAllVisible = (val) => {
        columnData.value.forEach(row => {
            row.can_view = val;
        });
        updateVisibleSelection();
    };

    // 切换所有可编辑状态
    const toggleAllEditable = (val) => {
        columnData.value.forEach(row => {
            row.can_update = val;
        });
        updateEditableSelection();
    };
    // 切换所有可编辑状态
    const toggleAllCreateable = (val) => {
        columnData.value.forEach(row => {
            row.can_create = val;
        });
        updateCreateableSelection();
    };

    // 更新可见选择状态
    const updateVisibleSelection = () => {
        const visibleRows = columnData.value.filter(row => row.can_view);
        allVisibleSelected.value = visibleRows.length === columnData.value.length;
        isIndeterminateVisible.value = visibleRows.length > 0 && visibleRows.length < columnData.value.length;
    };

    // 更新可编辑选择状态
    const updateEditableSelection = () => {
        const editableRows = columnData.value.filter(row => row.can_update);
        allEditableSelected.value = editableRows.length === columnData.value.length;
        isIndeterminateEditable.value = editableRows.length > 0 && editableRows.length < columnData.value.length;
    };

    function updateCreateableSelection(){
        const editableRows = columnData.value.filter(row => row.can_create);
        allCreateableSelected.value = editableRows.length === columnData.value.length;
        isIndeterminateCreateable.value = editableRows.length > 0 && editableRows.length < columnData.value.length;

    }

    // 生命周期钩子
    onMounted(() => {
        fetchRoleList()
    })

    // 方法
    const fetchRoleList = async () => {
        try {
            loadingPage.value = true
            const res = await Api.apiSystemRolePermission({ page: 1, limit: 999 })
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
        } finally {
            loadingPage.value = false
        }
    }

    const handleRoleChange = (roleId) => {
        const selectedRole = roleList.value.find(role => role.id === roleId)
        if (selectedRole) {
            roleObj.value = { ...selectedRole }
            fetchMenuData(selectedRole)
            // fetchDeptData()
        }
    }

    const fetchMenuData = async (role) => {
        try {
            loadingPage.value = true
            const res = await Api.apiSystemRoleIdToMenuid(role.id)
            if(res.code !=2000){
                ElMessage.warning(res.msg)
                loadingPage.value = false
                return
            }
            menuCheckedKeys.value = []
            // 处理菜单数据
            const menuData = res.data.map(menu => {
                menu.checked = false
                // 处理按钮权限选中状态
                const buttonPermissionChecked = []
                menu.menu_buttons.forEach(btn => {
                    btn.data_scope = 5
                    btn.dept = []
                    btn.checked = false
                    for (var i=0;i<role.role_button_permission.length;i++){
                        let temp_role_button_permission = role.role_button_permission[i]
                        if(btn.id === temp_role_button_permission.menu_button){
                            btn.data_scope = temp_role_button_permission.data_scope
                            btn.dept = temp_role_button_permission.dept
                            btn.checked = true
                            buttonPermissionChecked.push(btn.id)
                            break
                        }
                    }
                })
                menu.menu_fields.forEach(fds => {
                    fds.can_view = false
                    fds.can_create = false
                    fds.can_update = false
                    for (var i=0;i<role.role_field_permission.length;i++){
                        let temp_role_field_permission = role.role_field_permission[i]
                        if(fds.field_name === temp_role_field_permission.field_name){
                            fds.can_view = temp_role_field_permission.can_view
                            fds.can_create = temp_role_field_permission.can_create
                            fds.can_update = temp_role_field_permission.can_update
                            break
                        }
                    }
                })
                
                // 处理数据范围
                menu.data_scope = 4 // 默认全部数据权限
                menu.dept = []

                for (var i=0;i<role.role_menu_permission.length;i++){
                    let temp_role_menu_permission = role.role_menu_permission[i]
                    if(menu.id === temp_role_menu_permission.menu){
                        menu.data_scope = temp_role_menu_permission.data_scope
                        menu.dept = temp_role_menu_permission.dept
                        menu.checked = true
                        menuCheckedKeys.value.push(menu.id)
                        break
                    }
                }
                
                return {
                    ...menu,
                    buttonPermissionChecked
                }
            })
            
            // 转换为树形结构
            menuOptions.value = XEUtils.toArrayTree(menuData, { parentKey: 'parent' })

        } catch (error) {
            ElMessage.error('获取菜单权限失败')
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
        }
    }

    const nodeClick = (data) => {
        currentRole.value = data.id
        roleObj.value = data
        fetchMenuData(data)
        // fetchDeptData()
    }

    const dataScopeMenuSelectChange = (value) => {
        // 处理菜单数据范围变更
    }

    function handleNodeClick(data, node, component){
        currentMenu.value = data
    }

    function handleFeildNodeClick(data){
        if(data.type == 1){
            currentMenu.value = data
            columnData.value = deepClone(data?.menu_fields) || []
            resetECU()
            feildDrawer.value = true
        }
    }

    function confirmFeildClick(){
        if (!currentMenu.value) return;
        if(columnData.value && columnData.value.length>0){
             currentMenu.value = {
                ...currentMenu.value,
                menu_fields: [...columnData.value]
            };
            const updateTreeData = (nodes) => {
                nodes.forEach(node => {
                // 找到目标菜单节点
                if (node.id === currentMenu.value.id) {
                    node.menu_fields = columnData.value;
                }
                // 递归处理子节点
                if (node.children?.length) {
                    updateTreeData(node.children);
                }
                });
            };
             //执行更新
            updateTreeData(menuOptions.value);
        }
        feildDrawer.value = false;
    }

    const handleCheckClick = (data, checked) => {
        data.checked = checked
        const { menu_buttons, children } = data
        if (menu_buttons) {
            data.buttonPermissionChecked = checked ? menu_buttons.map(btn => btn.id) : []
            menu_buttons.forEach(item=>{
                item.checked = checked
            })
        }
        // 递归处理所有子节点
        const setChildrenChecked = (node, checkStatus) => {
            if (node.children && node.children.length) {
                node.children.forEach(child => {
                    menuTree.value.setChecked(child.id, checkStatus);
                    setChildrenChecked(child, checkStatus); // 递归调用
                });
            }
        };
        // 处理子节点
        if (children) {
            setChildrenChecked(data, checked);
        }
    }

    const getMenuAllCheckedKeys = () => {
        const checkedKeys = menuTree.value?.getCheckedKeys() || []
        const halfCheckedKeys = menuTree.value?.getHalfCheckedKeys() || []
        return [...checkedKeys, ...halfCheckedKeys]
    }

    function isNodeChecked(nodeId) {
        // 获取所有选中的节点key
        const checkedKeys = getMenuAllCheckedKeys()
        // 检查当前节点是否在选中列表中
        return checkedKeys.includes(nodeId);
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
    
    function handleJuDataScopeClick (item){
        isDialogDataScopeVisible.value = true
        currentButton.value = item
        nextTick(() => {
            dataScopeDialogRef.value.handleOpen(item)
        })
    }

    function handleMenuDataScopeClick(item){
        currentMenu.value = item
        isDialogMenuDataScopeVisible.value = true
        nextTick(() => {
            menuDataScopeDialogRef.value.handleOpen(item)
        })
    }

    function handleConfirmDataScope(item){
        if (currentButton.value) {
            // 直接修改原对象属性
            currentButton.value.data_scope = item.data_scope;
            currentButton.value.dept = item.dept;
        }
    }

    function handleConfirmMenuDataScope(item){
        if (currentMenu.value) {
            // 直接修改原对象属性
            currentMenu.value.data_scope = item.data_scope;
            currentMenu.value.dept = item.dept;
        }
    }

    function handleButtonPermissonChange(menuData, checkedIds){
        if (!menuData.menu_buttons) return;
  
        // 同步更新每个按钮的 checked 状态
        menuData.menu_buttons.forEach(button => {
            button.checked = checkedIds.includes(button.id);
        });
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
            let RoleMenuPermission = []
            let RoleMenuButtonPermission = []
            let FieldPermission = []
            menuData.forEach(item=>{
                if(item.checked){
                    RoleMenuPermission.push({
                        role:roleObj.value.id,
                        menu:item.id,
                        data_scope:item.data_scope,
                        dept:item.dept
                    })
                }
                item.menu_buttons.forEach(nitem=>{
                    if(nitem.checked){
                        RoleMenuButtonPermission.push({
                            role:roleObj.value.id,
                            menu_button:nitem.id,
                            data_scope:nitem.data_scope,
                            dept:nitem.dept
                        })
                    }
                })
                if(item.menu_fields && item.menu_fields.length>0){
                    const allDisabled = item.menu_fields.every(item => 
                        item.can_create === false && 
                        item.can_update === false && 
                        item.can_view === false
                    );
                    if(!allDisabled){//如果都为false默认表示没配置列权限
                        item.menu_fields.forEach(fitem=>{
                            FieldPermission.push({
                                role:roleObj.value.id,
                                field:fitem.id,
                                can_create:fitem.can_create,
                                can_update:fitem.can_update,
                                can_view:fitem.can_view
                            })
                        })
                    }
                }
            })
            // 准备角色数据
            const roleData = {
                role_id:roleObj.value.id,
                RoleMenuPermission: RoleMenuPermission,
                RoleMenuButtonPermission:RoleMenuButtonPermission,
                FieldPermission:FieldPermission,
            }
            // 保存角色权限
            const res = await Api.apiSystemRolePermissionSave(roleData)
            if (res.code === 2000) {
                ElMessage.success('保存成功')
                history.state.id = roleObj.value.id
                fetchRoleList()
            } else {
                ElMessage.warning(res.msg)
            }
        } catch (error) {
            ElMessage.error('保存权限失败')
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
        min-height: 30px;
        flex-shrink: 0;
    }

    .menu-name {
        font-weight: 500;
        color: var(--el-text-color-primary);
        flex: 1;
        min-width: 0;
        white-space: nowrap;
        line-height: 30px; /* 设置固定行高 */
    }

    .menu-data-scope-select {
        width: 150px;
        /* 确保选择框高度与其他元素一致 */
        :deep(.el-input__wrapper) {
            height: 30px;
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
        width:80px;
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