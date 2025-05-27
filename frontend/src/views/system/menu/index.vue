<template>
    <div class="menu-container">
        <el-row :gutter="10" class="main-row">
            <!-- 左侧菜单树 -->
            <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8" class="left-panel">
                <el-card shadow="hover" class="glass-card menu-card">
                    <template #header>
                        <div class="card-header">
                            <h4>菜单管理 <el-tooltip
                                class="item"
                                effect="dark"
                                content="支持拖拽菜单位置"
                                placement="right">
                                <el-icon><question-filled /></el-icon>
                                </el-tooltip>
                            </h4>
                            <el-button icon="Plus" circle @click="addMenu" type="primary" size="small" />
                        </div>
                    </template>

                    <el-input v-model="searchQuery" placeholder="搜索菜单..." prefix-icon="Search" clearable />

                    <div class="tree-wrapper">
                        <el-tree
                            ref="menuTree"
                            :data="filteredMenus"
                            node-key="id"
                            default-expand-all
                            draggable
                            :allow-drop="allowDrop"
                            :props="defaultProps"
                            @node-click="handleNodeClick"
                            @node-drop="onDrop"
                        >
                            <template #default="{ node, data }">
                                <span class="tree-node" :class="'level-' + getLevel(data)">
                                    <span class="tree-node-content">
                                    <el-icon><component :is="data.icon || 'Document'" /></el-icon>
                                    <span class="node-label">{{ node.label }}</span>
                                    <div class="actions">
                                        <el-button link type="primary" size="small" @click.stop="editMenu(data)">编辑</el-button>
                                        <el-button link type="danger" size="small" @click.stop="deleteMenu(data)">删除</el-button>
                                        <el-button link type="info" size="small" @click.stop="moveUp(data)">上移</el-button>
                                        <el-button link type="info" size="small" @click.stop="moveDown(data)">下移</el-button>
                                    </div>
                                    </span>
                                </span>
                            </template>
                        </el-tree>
                    </div>
                </el-card>
            </el-col>

            <!-- 右侧权限配置 -->
            <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16" class="right-panel">
                <transition name="fade" mode="out-in">
                    <el-card shadow="hover" class="glass-card permission-card" v-if="selectedMenu">
                        <template #header>
                            <h4>权限配置 - {{ selectedMenu.label }}</h4>
                        </template>

                        <el-tabs v-model="activeTab" :stretch="isMobile">
                            <!-- 按钮权限 -->
                            <el-tab-pane label="按钮权限配置" name="button">
                                <el-button type="primary" icon="Plus" @click="openButtonDialog">添加按钮权限</el-button>
                                <el-table :data="selectedMenu.buttons" row-key="id" border stripe style="margin-top: 10px;">
                                    <el-table-column prop="name" label="按钮名称" width="150" />
                                    <el-table-column prop="api" label="接口地址" />
                                    <el-table-column prop="method" label="请求方法" width="120">
                                        <template #default="{ row }">
                                            <el-tag :type="getMethodTagType(row.method)">{{ row.method }}</el-tag>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="操作" width="150">
                                        <template #default="{ $index }">
                                            <el-button link type="primary" @click="editButton($index)">编辑</el-button>
                                            <el-button link type="danger" @click="deleteButton($index)">删除</el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-tab-pane>

                            <!-- 列权限 -->
                            <el-tab-pane label="列权限配置" name="column">
                                <el-button type="success" icon="Plus" @click="openColumnDialog">添加列权限</el-button>
                                <el-table :data="selectedMenu.columns" row-key="id" border stripe style="margin-top: 10px;">
                                    <el-table-column prop="name" label="字段名称" width="150" />
                                    <el-table-column label="查询权限" width="120">
                                        <template #default="{ row }">
                                            <el-switch v-model="row.query" active-color="#13ce66" />
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="新增权限" width="120">
                                        <template #default="{ row }">
                                            <el-switch v-model="row.create" active-color="#13ce66" />
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="编辑权限" width="120">
                                        <template #default="{ row }">
                                            <el-switch v-model="row.edit" active-color="#13ce66" />
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="操作" width="150">
                                        <template #default="{ $index }">
                                            <el-button link type="primary" @click="editColumn($index)">编辑</el-button>
                                            <el-button link type="danger" @click="deleteColumn($index)">删除</el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-tab-pane>
                        </el-tabs>
                    </el-card>
                    <el-card shadow="hover" class="glass-card permission-card" v-else>
                        <el-empty description="请选择左侧菜单"/>
                    </el-card>
                </transition>
            </el-col>
        </el-row>

        <!-- 弹窗表单 -->
        <el-dialog v-model="dialogVisible" :title="dialogTitle" width="560px" :fullscreen="isMobile" :close-on-click-modal="false">
            <el-form ref="formRef" :rules="menuRules" :model="formData" label-width="100px" v-if="currentForm === 'menu'">
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="菜单类型" prop="type">
                            <el-radio-group v-model="formData.type">
                                <el-radio-button label="目录" :value="0" />
                                <el-radio-button label="菜单" :value="1" />
                                <el-radio-button label="Iframe" :value="2" />
                                <el-radio-button label="外链" :value="3" />
                            </el-radio-group>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="父级菜单" prop="parent">
                            <el-cascader
                                style="width: 100%"
                                :key="isResourceShow"
                                :show-all-levels="false"
                                :options="options"
                                v-model="formData.parent"
                                @change="handleChange"
                                :props="{ checkStrictly: true ,label:'name',value:'id'}"
                                clearable></el-cascader>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="菜单名称" prop="name">
                            <el-input v-model="formData.name" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="菜单图标" prop="icon">
                            <icon-selector v-model="formData.icon" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="菜单排序" prop="sort">
                            <el-input-number v-model="formData.sort" controls-position="right" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="路由地址" prop="web_path" :rules="formData?.type !=0?menuWebPathRule:[]">
                            <el-input v-model="formData.web_path" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="组件名称" prop="component_name">
                            <el-input v-model="formData.component_name" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="组件路径">
                            <el-input v-model="formData.component" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="侧边可见" prop="visible">
                            <el-switch v-model="formData.visible" inline-prompt active-text="是" inactive-text="否"/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="是否缓存" prop="cache">
                            <el-switch v-model="formData.cache" inline-prompt active-text="是" inactive-text="否"/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="菜单状态" prop="status">
                            <el-switch v-model="formData.status" inline-prompt active-text="启用" inactive-text="禁用"/>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>

            <el-form ref="formRef" :model="formData" label-width="100px" v-if="currentForm === 'button'">
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="按钮名称">
                            <el-input v-model="formData.name" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="接口地址">
                            <el-input v-model="formData.api" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="请求方法">
                            <el-select v-model="formData.method" placeholder="请选择" style="width: 100%">
                                <el-option label="GET" value="GET" />
                                <el-option label="POST" value="POST" />
                                <el-option label="PUT" value="PUT" />
                                <el-option label="DELETE" value="DELETE" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>

            <el-form ref="formRef" :model="formData" label-width="100px" v-if="currentForm === 'column'">
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="字段名称">
                            <el-input v-model="formData.name" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
                        <el-form-item label="查询权限">
                            <el-switch v-model="formData.query" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
                        <el-form-item label="新增权限">
                            <el-switch v-model="formData.create" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
                        <el-form-item label="编辑权限">
                            <el-switch v-model="formData.edit" />
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="saveData">保存</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
    import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
    import { ElMessage, ElMessageBox } from 'element-plus'
    import IconSelector from '@/components/icons/IconSelector.vue'

    // 数据源
    const menus = ref([
        {
            id: 1,
            parentId: 0,
            label: '仪表盘',
            icon: 'HomeFilled',
            path: '/dashboard',
            component: 'Dashboard',
            sort: 1,
            hidden: false,
            buttons: [],
            columns: []
        },
        {
            id: 2,
            parentId: 0,
            label: '系统管理',
            icon: 'Setting',
            path: '/system',
            component: 'Layout',
            sort: 2,
            hidden: false,
            children: [
            {
                id: 3,
                parentId: 2,
                label: '用户管理',
                icon: 'User',
                path: 'user',
                component: 'System/User',
                sort: 1,
                hidden: false,
                buttons: [
                { id: 1, name: '新增用户', api: '/api/user', method: 'POST' },
                { id: 2, name: '导出用户', api: '/api/user/export', method: 'GET' }
                ],
                columns: [
                { id: 1, name: '用户名', query: true, create: true, edit: true },
                { id: 2, name: '邮箱', query: true, create: true, edit: true },
                { id: 3, name: '角色', query: true, create: true, edit: true }
                ]
            },
            {
                id: 4,
                parentId: 2,
                label: '角色管理',
                icon: 'Avatar',
                path: 'role',
                component: 'System/Role',
                sort: 2,
                hidden: false,
                buttons: [
                { id: 3, name: '分配权限', api: '/api/role/assign', method: 'POST' }
                ],
                columns: [
                { id: 4, name: '角色名称', query: true, create: true, edit: true },
                { id: 5, name: '权限列表', query: true, create: true, edit: false }
                ]
            }
            ],
            buttons: [],
            columns: []
        }
        
        ]
    )

    let menuRules = {
        /* parent: [
            {required: true, message: '请选择父级菜单',trigger: 'blur'}
        ],*/
        name: [
            {required: true, message: '请输入菜单名称',trigger: 'blur'}
        ],
        sort: [
            {required: true, message: '请输入排序',trigger: 'blur'}
        ],
        // icon: [
        //     {required: true, message: '请填充图标',trigger: 'blur'}
        // ],
        // web_path: [
        //     {required: true, message: '请输入路由地址',trigger: 'blur'}
        // ],
    }

    let menuWebPathRule = [
        {
          required: true,
          message: '请输入路由地址',
          trigger: 'blur',
        },
    ]

    // 响应式变量
    const selectedMenu = ref(null)
    const searchQuery = ref('')
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增')
    const currentForm = ref('menu')
    const formData = ref({})
    const activeTab = ref('button')
    const menuTree = ref(null)
    const isMobile = ref(false)

    // 默认属性
    const defaultProps = {
        children: 'children',
        label: 'label'
    }

    // 计算属性
    const filteredMenus = computed(() => {
    if (!searchQuery.value) return menus.value
        const key = searchQuery.value.toLowerCase()
        return filterNodes(JSON.parse(JSON.stringify(menus.value)), key)
    })

    // 方法
    function filterNodes(nodes, key) {
        return nodes.filter(node => {
            const match = node.label.toLowerCase().includes(key)
            if (node.children) {
                node.children = filterNodes(node.children, key)
            }
            return match || (node.children && node.children.length > 0)
        })
    }

    function getLevel(node) {
        let level = 0
        let parent = findParent(menus.value, node.parentId)
        while (parent) {
            level++
            parent = findParent(menus.value, parent.parentId)
        }
        return level
    }

    function findParent(list, id) {
        for (const item of list) {
            if (item.id === id) return item
            if (item.children) {
                const found = findParent(item.children, id)
                if (found) return found
            }
        }
        return null
    }

    function addMenu() {
        currentForm.value = 'menu'
        dialogTitle.value = '新增菜单'
        formData.value = {
            id: "",
            parent: selectedMenu.value ? selectedMenu.value.id : 0,
            name: '',
            icon: '',
            web_path: '',
            component: '',
            component_name: '',
            link_url:'',
            type:0,
            sort: 0,
            cache: false,
            status: true,
            visible:true,
            buttons: [],
            columns: []
        }
        dialogVisible.value = true
    }

    function editMenu(data) {
        currentForm.value = 'menu'
        dialogTitle.value = '编辑菜单'
        formData.value = JSON.parse(JSON.stringify(data))
        dialogVisible.value = true
    }

    function deleteMenu(data) {
        ElMessageBox.confirm('确定要删除该菜单吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            removeNode(menus.value, data.id)
            selectedMenu.value = null
            ElMessage.success('删除成功')
        })
    }

    function removeNode(list, id) {
        for (let i = 0; i < list.length; i++) {
            if (list[i].id === id) {
                list.splice(i, 1)
                return true
            }
            if (list[i].children) {
                if (removeNode(list[i].children, id)) {
                    return true
                }
            }
        }
        return false
    }

    function moveUp(data) {
        const parent = findParent(menus.value, data.parentId)
        const list = parent ? parent.children : menus.value
        const index = list.findIndex(i => i.id === data.id)
        if (index > 0) {
            [list[index], list[index - 1]] = [list[index - 1], list[index]]
            refreshTree()
        }
    }

    function moveDown(data) {
        const parent = findParent(menus.value, data.parentId)
        const list = parent ? parent.children : menus.value
        const index = list.findIndex(i => i.id === data.id)
        if (index < list.length - 1) {
            [list[index], list[index + 1]] = [list[index + 1], list[index]]
            refreshTree()
        }
    }

    function refreshTree() {
        // 强制刷新树组件
        const data = JSON.parse(JSON.stringify(menus.value))
        menus.value = []
        nextTick(() => {
            menus.value = data
        })
    }

    function allowDrop(draggingNode, dropNode, type) {
        // 不允许将节点拖拽到其自身或其子节点上
        if (type === 'inner' && draggingNode.data.id === dropNode.data.id) {
            return false
        }
        
        // 检查是否尝试将节点拖拽到其子节点上
        let parent = dropNode.parent
        while (parent) {
            if (parent.data.id === draggingNode.data.id) {
                return false
            }
            parent = parent.parent
        }
        
        return true
    }

    function onDrop(draggingNode, dropNode, type) {
        // 更新父节点ID和排序
        const node = draggingNode.data
        if (type === 'inner') {
            node.parentId = dropNode.data.id
        } else {
            node.parentId = dropNode.data.parentId
        }
        
        // 更新排序
        const parent = findParent(menus.value, node.parentId)
        const list = parent ? parent.children : menus.value
        list.forEach((item, index) => {
            item.sort = index + 1
        })
    }

    function handleNodeClick(data) {
        selectedMenu.value = data
    }

    function openButtonDialog() {
        currentForm.value = 'button'
        dialogTitle.value = '新增按钮权限'
        formData.value = {
            id: Date.now(),
            name: '',
            api: '',
            method: 'GET'
        }
        dialogVisible.value = true
    }

    function editButton(index) {
        currentForm.value = 'button'
        dialogTitle.value = '编辑按钮权限'
        formData.value = JSON.parse(JSON.stringify(selectedMenu.value.buttons[index]))
        dialogVisible.value = true
    }

    function deleteButton(index) {
        selectedMenu.value.buttons.splice(index, 1)
        ElMessage.success('删除成功')
    }

    function openColumnDialog() {
        currentForm.value = 'column'
        dialogTitle.value = '新增列权限'
        formData.value = {
            id: Date.now(),
            name: '',
            query: true,
            create: true,
            edit: true
        }
        dialogVisible.value = true
    }

    function editColumn(index) {
        currentForm.value = 'column'
        dialogTitle.value = '编辑列权限'
        formData.value = JSON.parse(JSON.stringify(selectedMenu.value.columns[index]))
        dialogVisible.value = true
    }

    function deleteColumn(index) {
        selectedMenu.value.columns.splice(index, 1)
        ElMessage.success('删除成功')
    }

    function saveData() {
        if (currentForm.value === 'menu') {
            const targetList = formData.value.parentId === 0 ? menus.value : findParent(menus.value, formData.value.parentId)?.children || []
            const idx = targetList.findIndex(i => i.id === formData.value.id)
            if (idx !== -1) {
                targetList.splice(idx, 1, { ...formData.value })
            } else {
                targetList.push({ ...formData.value })
            }
        } else if (currentForm.value === 'button') {
            const idx = selectedMenu.value.buttons.findIndex(i => i.id === formData.value.id)
            if (idx !== -1) {
                selectedMenu.value.buttons.splice(idx, 1, { ...formData.value })
            } else {
                selectedMenu.value.buttons.push({ ...formData.value })
            }
        } else if (currentForm.value === 'column') {
            const idx = selectedMenu.value.columns.findIndex(i => i.id === formData.value.id)
            if (idx !== -1) {
                selectedMenu.value.columns.splice(idx, 1, { ...formData.value })
            } else {
                selectedMenu.value.columns.push({ ...formData.value })
            }
        }

        dialogVisible.value = false
        ElMessage.success('保存成功')
    }

    function getMethodTagType(method) {
        switch (method) {
            case 'GET': return 'success'
            case 'POST': return 'primary'
            case 'PUT': return 'warning'
            case 'DELETE': return 'danger'
            default: return ''
        }
    }

    function checkMobile() {
        isMobile.value = window.innerWidth < 768
    }

    // 生命周期钩子
    onMounted(() => {
        checkMobile()
        window.addEventListener('resize', checkMobile)
    })

    onBeforeUnmount(() => {
        window.removeEventListener('resize', checkMobile)
    })
</script>

<style scoped lang="scss">
    .menu-container {
        padding: 10px;
    }

    .main-row {
        display: flex;
        flex-wrap: wrap;
        margin: 0 !important;
        height: auto;
    }

    .left-panel, .right-panel {
        padding: 0 !important;
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #333;
        font-weight: bold;
        padding: 0 4px;
    }

    .tree-wrapper {
        margin-top: 12px;
        overflow-y: auto;
        
        &::-webkit-scrollbar {
            width: 6px;
        }
        
        &::-webkit-scrollbar-thumb {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 3px;
        }
    }

    .tree-node {
        position: relative;
        width: 100%;
        padding-left: 5px;
        
        &::before {
            content: '';
            position: absolute;
            left: -9px;
            top: -15px;
            bottom: 50%;
            width: 16px;
            border-left: 1px dashed #c0c4cc;
            border-bottom: 1px dashed #c0c4cc;
        }
        
        &.level-0::before {
            display: none;
        }
    
        .tree-node-content {
            display: flex;
            align-items: center;
            padding: 8px 0;
            width: 100%;
            
            .el-icon {
                margin-right: 8px;
                color: var(--el-color-primary);
            }
            
            .node-label {
                flex: 1;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
        }
    
        .actions {
            display: flex;
            margin-left: 8px;
            opacity: 0;
            transition: opacity 0.3s;
            
            .el-button {
                padding: 0 4px;
            }
        }
    
        &:hover .actions {
            opacity: 1;
        }
    }

    .glass-card {
        border-radius: 6px;
        height: 100%;
    
        &.menu-card {
            margin-right: 8px;
        }
        
        &.permission-card {
            margin-left: 8px;
        }
    }

    .fade-enter-active, .fade-leave-active {
        transition: opacity 0.3s ease;
    }

    .fade-enter-from, .fade-leave-to {
        opacity: 0;
    }

    /* 移动端样式 */
    @media (max-width: 768px) {
        .main-row {
            flex-direction: column;
        }
        
        .left-panel, .right-panel {
            width: 100%;
        }
        
        .glass-card {
            &.menu-card, &.permission-card {
            margin: 0 0 16px 0;
            }
        }
    
        .tree-node {
            .actions {
                opacity: 1;
                flex-wrap: wrap;
                justify-content: flex-end;
            
                .el-button {
                    margin: 2px 0;
                }
            }
        }
    }

    /* 树节点连接线样式 */
    :deep(.el-tree) {
        .el-tree-node {
            position: relative;
            
            &:last-child::before {
                height: 50%;
            }
        }
        
        .el-tree-node__content {
            padding-left: 8px !important;
            height: auto;
        }
        
        .el-tree-node__children {
            padding-left: 16px;
        }
    }
</style>