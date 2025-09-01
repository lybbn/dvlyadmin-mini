<template>
    <div class="menu-container">
        <el-row :gutter="10" class="main-row">
            <!-- 左侧菜单树 -->
            <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8" class="left-panel">
                <el-card shadow="hover" class="glass-card menu-card" v-loading="loadingMenuPage">
                    <template #header>
                        <div class="card-header">
                            <h4>菜单管理 <el-tooltip
                                class="item"
                                effect="dark"
                                raw-content
                                content="<div>1、支持拖拽菜单排序。</div><div>2、只有类型为【菜单】才能做【权限配置】。</div><div>3、配置sort时尽量间隔数值大一些。</div><div>4、类型为【菜单】的【组件名称】用于按钮权限值的匹配。</div>"
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
                            :expand-on-click-node="false"
                            draggable
                            :allow-drop="allowDrop"
                            :props="defaultProps"
                            @node-click="handleNodeClick"
                            @node-drop="onDrop"
                        >
                            <template #default="{ node, data }">
                                <span class="tree-node" :class="'level-' + getLevel(data)">
                                    <span class="tree-node-content">
                                        <SvgIcon :icon-class="data?.icon || 'Menu'" style="font-size:16px !important;"></SvgIcon>
                                        <span class="node-label">{{ node.label }}</span>
                                        <div class="actions">
                                            <el-button link type="info" size="small" @click.stop="">排序({{ data.sort }})</el-button>
                                            <el-button link type="primary" size="small" @click.stop="editMenu(data)" v-auth="'Update'">编辑</el-button>
                                            <el-button link type="danger" size="small" @click.stop="deleteMenu(data)" v-auth="'Delete'">删除</el-button>
                                            <el-button link type="primary" size="small" @click.stop="moveUp(data)" v-auth="'Move'">上移</el-button>
                                            <el-button link type="primary" size="small" @click.stop="moveDown(data)" v-auth="'Move'">下移</el-button>
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
                    <el-card shadow="hover" class="glass-card permission-card" v-if="selectedMenu && selectedMenu.type === 1">
                        <template #header>
                            <h4>权限配置 - {{ selectedMenu.name }}</h4>
                        </template>

                        <el-tabs v-model="activeTab" :stretch="isMobile" @tab-change="handlePMChage">
                            <!-- 按钮权限 -->
                            <el-tab-pane label="按钮权限配置" name="button">
                                <el-button type="primary" icon="Plus" @click="openButtonDialog" v-auth="'MenuButtonCreate'">添加按钮权限</el-button>
                                <el-button type="primary" @click="buttonBatchCreate">批量生成</el-button>
                                <el-button @click="getMenuButtonList" circle icon="refresh"></el-button>
                                <el-table :data="menuButtonList" row-key="id" border stripe style="margin-top: 10px;" v-loading="isMenuButtonListLoading">
                                    <el-table-column type="index" width="60" label="序号">
                                        <template #default="scope">
                                            <span v-text="scope.$index+1"></span>
                                        </template>
                                    </el-table-column>
                                    <el-table-column prop="name" label="按钮名称" width="120" />
                                    <el-table-column prop="value" label="权限值" min-width="140" />
                                    <el-table-column prop="api" label="接口地址" min-width="170"/>
                                    <el-table-column prop="method" label="请求方法" width="90">
                                        <template #default="{ row }">
                                            <el-tag :type="getMethodTagType(row.method)">{{ getMethodName(row.method) }}</el-tag>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="操作" width="120">
                                        <template #default="scope">
                                            <el-button link type="primary" @click="editButton(scope.row)" v-auth="'MenuButtonUpdate'">编辑</el-button>
                                            <el-button link type="danger" @click="deleteButton(scope.row)" v-auth="'MenuButtonDelete'">删除</el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-tab-pane>

                            <!-- 列权限 -->
                            <el-tab-pane label="列权限配置" name="column">
                                <el-button type="primary" icon="Plus" @click="openColumnDialog" v-auth="'MenuFieldCreate'">添加列权限</el-button>
                                <el-button type="primary" @click="FeildBatchCreate">自动生成</el-button>
                                <el-button @click="getMenuFieldList" circle icon="refresh"></el-button>
                                <el-table :data="menuFieldList" row-key="id" border stripe style="margin-top: 10px;" v-loading="loadingMenuField">
                                    <el-table-column type="index" width="60" label="序号">
                                        <template #default="scope">
                                            <span v-text="scope.$index+1"></span>
                                        </template>
                                    </el-table-column>
                                    <el-table-column prop="model" label="所属模型" width="150" />
                                    <el-table-column prop="field_name" label="字段名" min-width="150" />
                                    <el-table-column prop="title" label="字段显示名" min-width="150" />
                                    <el-table-column label="操作" width="150">
                                        <template #default="scope">
                                            <el-button link type="primary" @click="editColumn(scope.row)" v-auth="'MenuFieldDelete'">编辑</el-button>
                                            <el-button link type="danger" @click="deleteColumn(scope.row)" v-auth="'MenuFieldDelete'">删除</el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-tab-pane>
                        </el-tabs>
                    </el-card>
                    <el-card shadow="hover" class="glass-card permission-card" v-else>
                        <el-empty description="请选择左侧菜单、类型为【菜单】才允许配置权限"/>
                    </el-card>
                </transition>
            </el-col>
        </el-row>

        <!-- 弹窗表单 -->
        <el-dialog v-model="dialogVisible" :title="dialogTitle" width="560px" :fullscreen="isMobile" :close-on-click-modal="false">
            <el-form ref="formRefm" :rules="menuRules" :model="formData" label-width="100px" v-if="currentForm === 'menu'">
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
                            <el-tree-select v-model="formData.parent" node-key="id" :data="menus"
                                            check-strictly filterable clearable :render-after-expand="false"
                                            :props="{label:'name',value: 'id'}"
                                            style="width: 100%" placeholder="请选择/为空则为顶级" >
                                <template #default="{ data: { name,sort } }">
                                    {{ name }}<span style="float: right;color: gray;font-size: 12px;">排序({{ sort }})</span>
                                </template>
                            </el-tree-select>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="菜单名称" prop="name">
                            <el-input v-model="formData.name" placeholder="输入菜单的名称，如：用户管理"/>
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
                        <el-form-item label="路由地址" prop="web_path" :rules="menuWebPathRule">
                            <el-input v-model="formData.web_path" placeholder="输入路由地址：/home，相当于前端route的path属性" @input="handleWebPathInput"/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" v-if="formData?.type ===1">
                        <el-form-item label="组件名称" prop="component_name">
                            <el-input v-model="formData.component_name" placeholder="输入组件名，相当于前端route的name属性"/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" v-if="formData?.type ===1">
                        <el-form-item label="组件路径">
                            <el-input v-model="formData.component" placeholder="前端页面组件的位置路径：system/dept/deptManage"/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" v-if="formData?.type ===2 || formData?.type ===3">
                        <el-form-item label="链接地址" :rules="formData?.type ===2|| formData?.type ===3?menuLinkurlRule:[]">
                            <el-input v-model="formData.link_url" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="侧边可见" prop="visible">
                            <el-switch v-model="formData.visible" inline-prompt active-text="是" inactive-text="否"/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" v-if="formData?.type ===1">
                        <el-form-item label="是否缓存" prop="cache">
                            <el-switch v-model="formData.cache" inline-prompt active-text="是" inactive-text="否" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-form-item label="菜单状态" prop="status">
                            <el-switch v-model="formData.status" inline-prompt active-text="启用" inactive-text="禁用"/>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>

            <el-form ref="formRefb" :model="formData" :rules="buttonRules" label-width="100px" v-if="currentForm === 'button'">
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="按钮名称" prop="name">
                            <el-select v-model="formData.name" allow-create filterable placeholder="请选择" style="width: 80%" @change="getApiButtonCode">
                                <el-option
                                    v-for="item in buttonList"
                                    :key="item.value"
                                    :label="item.name"
                                    :value="item.name">
                                </el-option>
                            </el-select>
                            <el-button type="primary" v-auth="'ButtonCreate'" circle style="margin-left: 20px"  @click="addMenuButtonTemplateTable"><el-icon><circle-plus /></el-icon></el-button>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="权限值" prop="value">
                            <el-input v-model="formData.value" placeholder="组件名:按钮权限值  需唯一"/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="请求方法" prop="method">
                            <el-select v-model="formData.method" placeholder="请选择" style="width: 100%">
                                <el-option label="GET" :value="0" />
                                <el-option label="POST" :value="1" />
                                <el-option label="PUT" :value="2" />
                                <el-option label="DELETE" :value="3" />
                                <el-option label="OPTIONS" :value="4" />
                                <el-option label="WS" :value="5" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="接口地址" prop="api">
                            <el-select  v-model.trim="formData.api" filterable clearable  allow-create style="margin-bottom: 5px;width: 100%;" placeholder="请选择或手动输入">
                                <el-option
                                    v-for="item in apiList"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                            <el-alert title="请正确填写(或选择)，以免请求时被拦截。匹配编辑/详情/删除使用正则,如:/api/xxx/{id}/" type="info" show-icon/>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>

            <el-form ref="formRefc" :model="formData" :rules="feildRules" label-width="100px" v-if="currentForm === 'column'">
                <el-row :gutter="10">
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="所属模型" prop="model">
                            <el-select v-model="formData.model" allow-create filterable placeholder="请选择" style="width: 100%">
                                <el-option
                                    v-for="item in allCustomModels"
                                    :key="item.model"
                                    :label="item.title"
                                    :value="item.model">
                                    <span style="float: left">{{ item.title }}</span>
                                    <span
                                        style="
                                        float: right;
                                        color: var(--el-text-color-secondary);
                                        font-size: 13px;
                                        "
                                    >
                                        {{ item.model }}
                                    </span>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="显示名" prop="title">
                            <el-input v-model="formData.title" placeholder="如：用户名"/>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <el-form-item label="字段名" prop="field_name">
                            <el-input v-model="formData.field_name" placeholder="如：username"/>
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
        <el-dialog v-model="dialogAutoCreateFieldVisible" title="所属模型" width="500px" :fullscreen="isMobile" :close-on-click-modal="false">
            <el-select v-model="customMenuFeildModel" allow-create filterable placeholder="请选择所属模型" style="width: 100%">
                <el-option
                    v-for="item in allCustomModels"
                    :key="item.model"
                    :label="item.title"
                    :value="item.model">
                    <span style="float: left">{{ item.title }}</span>
                    <span
                        style="
                        float: right;
                        color: var(--el-text-color-secondary);
                        font-size: 13px;
                        "
                    >
                        {{ item.model }}
                    </span>
                </el-option>
            </el-select>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogAutoCreateFieldVisible = false">取消</el-button>
                    <el-button type="primary" @click="saveFeildBatchCreate">提交</el-button>
                </span>
            </template>
        </el-dialog>
        <moduleMenuButton ref="moduleMenuButtonFlag" @refreshData="handleRefreshMenuButtonTData" v-if="isDialogMenuButtonVisible" @closed="isDialogMenuButtonVisible = false"></moduleMenuButton>
        <DialogTableList ref="moduleMenuButtonTableFlag" :apiObj="Api.apiSystemButtonTemplate" width="680px" :tableIndex="true" v-if="isDialogMenuButtonTableVisible" @closed="isDialogMenuButtonTableVisible = false;getButtonTemplateData()">
            <template v-slot:search>
                <el-form>
                    <el-form-item label="">
                        <el-button type="primary" @click="handleMenuButtonTemplateAdd">新增</el-button>
                    </el-form-item>
                </el-form>
            </template>
            <el-table-column min-width="150" prop="name" label="按钮名称"></el-table-column>
            <el-table-column min-width="150" prop="value" label="权限值"></el-table-column>
            <el-table-column :fixed="isMobile?false:'right'" label="操作" width="120">
                <template #default="scope">
                    <el-button link type="primary" @click="handleMenuButtonTemplateOp(scope.row,'edit')">编辑</el-button>
                    <el-button link type="primary" @click ="handleMenuButtonTemplateOp(scope.row,'del')">删除</el-button>
                </template>
            </el-table-column>
        </DialogTableList>
    </div>
</template>

<script setup>
    import { ref, computed, watch, onMounted, onBeforeUnmount,nextTick } from 'vue'
    import { ElMessage, ElMessageBox } from 'element-plus'
    import IconSelector from '@/components/icons/IconSelector.vue'
    import Api from "@/api/api.js"
    import {deepClone} from "@/utils/util.js"
    import XEUtils from "xe-utils";
    import moduleMenuButton from "./components/moduleMenuButton.vue";
    import DialogTableList from "@/components/dialog/dialogTableList.vue"
    import { useUserState } from "@/store/userState";
    import SvgIcon from '@/components/icons/svgIcon.vue'

    let userState = useUserState()

    let formRefm = ref(null)
    let formRefb = ref(null)
    let formRefc = ref(null)

    let apiList = ref([])
    let isMenuButtonListLoading = ref(false)
    let dialogAutoCreateFieldVisible = ref(false)
    let customMenuFeildModel = ref("")

    // 数据源
    const menus = ref([
        {
            id: "1",
            parent: null,
            name: '仪表盘',
            icon: 'HomeFilled',
            path: '/dashboard',
            component: 'Dashboard',
            sort: 1,
            hidden: false,
            columns: []
        },
        {
            id: "2",
            parent: null,
            name: '系统管理',
            icon: 'Setting',
            path: '/system',
            component: 'Layout',
            sort: 2,
            hidden: false,
            children: [
            {
                id: "3",
                parent: "2",
                name: '用户管理',
                icon: 'User',
                path: 'user',
                component: 'System/User',
                sort: 1,
                hidden: false,
                columns: [
                { id: 1, name: '用户名', query: true, create: true, edit: true },
                { id: 2, name: '邮箱', query: true, create: true, edit: true },
                { id: 3, name: '角色', query: true, create: true, edit: true }
                ]
            },
            {
                id: "4",
                parent: "2",
                name: '角色管理',
                icon: 'Avatar',
                path: 'role',
                component: 'System/Role',
                sort: 2,
                hidden: false,
                columns: [
                { id: 4, name: '角色名称', query: true, create: true, edit: true },
                { id: 5, name: '权限列表', query: true, create: true, edit: false }
                ]
            }
            ],
            columns: []
        }
        
        ]
    )
    let buttonList = ref([])
    let menuButtonList = ref([])
    let menuFieldList = ref([])
    let allCustomModels = ref([])
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

    let buttonRules = {
        name: [
            {required: true, message: '请输入/选择按钮名称',trigger: 'blur'}
        ],
        value: [
            {required: true, message: '请输入权限值',trigger: 'blur'}
        ],
        api: [
            {required: true, message: '请输入接口地址',trigger: 'blur'}
        ],
        method: [
            {required: true, message: '请选择接口方法',trigger: 'blur'}
        ],
    }

    let feildRules = {
        model: [
            {required: true, message: '请选择所属表',trigger: 'blur'}
        ],
        field_name: [
            {required: true, message: '请输入字段名',trigger: 'blur'}
        ],
        title: [
            {required: true, message: '请输入字段显示名',trigger: 'blur'}
        ]
    }

    let menuWebPathRule = [
        {
          required: true,
          message: '请输入路由地址',
          trigger: 'blur',
        },
    ]

    let menuLinkurlRule = [
        {
          required: true,
          message: '请输入链接地址',
          trigger: 'blur',
        },
    ]

    // 响应式变量
    const selectedMenu = ref(null)
    const searchQuery = ref('')
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增')
    const currentForm = ref('menu')
    let currentSaveMode = ref('add')
    const formData = ref({})
    const activeTab = ref('button')
    const menuTree = ref(null)
    const isMobile = ref(false)

    // 默认属性
    const defaultProps = {
        children: 'children',
        label: 'name'
    }

    // 计算属性
    const filteredMenus = computed(() => {
    if (!searchQuery.value) return menus.value
        const key = searchQuery.value.toLowerCase()
        return filterNodes(deepClone(menus.value), key)
    })

    // 方法
    function filterNodes(nodes, key) {
        return nodes.filter(node => {
            const match = node.name.toLowerCase().includes(key)
            if (node.children) {
                node.children = filterNodes(node.children, key)
            }
            return match || (node.children && node.children.length > 0)
        })
    }

    function getLevel(node) {
        let level = 0
        let parent = findParent(menus.value, node.parent)
        while (parent) {
            level++
            parent = findParent(menus.value, parent.parent)
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
        currentSaveMode.value = 'add'
        dialogTitle.value = '新增菜单'
        formData.value = {
            id: "",
            parent: selectedMenu.value ? selectedMenu.value.id : "",
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
        currentSaveMode.value = 'edit'
        dialogTitle.value = '编辑菜单'
        formData.value = deepClone(data)
        dialogVisible.value = true
    }

    function deleteMenu(data) {
        ElMessageBox.confirm('确定要删除该菜单吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            Api.apiSystemMenuDelete({id:data.id}).then(res=>{
                if(res.code === 2000){
                    removeNode(menus.value, data.id)
                    selectedMenu.value = null
                    ElMessage.success('删除成功')
                    getMenuData()
                }else{
                    ElMessage.warning(res.msg)
                }
            })
            
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

    function updateSortToServer(nodes){
        const payload = {
            menus: nodes.map(node => ({
                id: node.id,
                sort: node.sort,
                parent:node.parent
            }))
        }
        Api.apiSystemMenuUpdateSort(payload).then(res=>{
            if(res.code === 2000){
                getMenuData()
                ElMessage.success(res.msg)
            }else{
                getMenuData()
                ElMessage.warning(res.msg)
            }
        })
    }

    function moveUp(data) {
        const parent = findParent(menus.value, data.parent)
        const list = parent ? parent.children : menus.value
        const index = list.findIndex(i => i.id === data.id)
        if (index > 0) {
            // 先定义变量
            const currentNode = list[index]
            const prevNode = list[index - 1]

            // 交换位置
            list[index] = prevNode
            list[index - 1] = currentNode

            // 交换排序值
            const tempSort = currentNode.sort
            currentNode.sort = prevNode.sort
            prevNode.sort = tempSort

            // 提交排序到后端
            updateSortToServer([currentNode, prevNode])
        }
    }

    function moveDown(data) {
        const parent = findParent(menus.value, data.parent);
        const list = parent ? parent.children : menus.value;
        const index = list.findIndex(i => i.id === data.id);
        
        if (index < list.length - 1) {
            // 先定义变量（避免解构赋值的顺序问题）
            const currentNode = list[index];
            const nextNode = list[index + 1];

            // 交换位置（直接赋值，不使用解构）
            list[index] = nextNode;
            list[index + 1] = currentNode;

            // 交换排序值
            const tempSort = currentNode.sort;
            currentNode.sort = nextNode.sort;
            nextNode.sort = tempSort;

            updateSortToServer([currentNode, nextNode]);
        }
    }

    function refreshTree() {
        // 强制刷新树组件
        const data = deepClone(menus.value)
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
        console.log(menus.value,111)
        //draggingNode 拖拽的节点 、dropNode拖拽的目标节点、type 拖拽放置的类型（相对拖拽后的目标节点）
        let currentNode = draggingNode.data
        let tmpcsort = currentNode.sort
        let targetData = dropNode.data;
        let tmptsort = targetData.sort
        let yxIndex;//受影响的上一个或下一个节点索引

        // 获取新父级 & 新兄弟节点
        let newParent = findParent(menus.value, targetData.parent);
        let newSiblings = newParent ? newParent.children : menus.value;
        let targetIndex = newSiblings.findIndex(item => item.id === dropNode.data.id);

        let modifyDataArr = []
        let mustUpdateSameLevelSort = false //是否更新同级的所有sort
        // 使用固定步长重新分配 sort 值（基于当前 index）
        const baseSort = 10;
        if (type === 'before') {
            // 插入到 dropNode 前面
            currentNode.parent = dropNode.data.parent
            yxIndex = targetIndex - 2
            currentNode.sort = tmptsort-1
        } else if (type === 'after') {
            // 插入到 dropNode 后面
            currentNode.parent = dropNode.data.parent
            yxIndex = targetIndex + 2
            currentNode.sort = tmptsort+1
        } else if (type === 'inner') {
            // 成为 dropNode 的子节点
            currentNode.parent = dropNode.data.id
            yxIndex = newSiblings.length;
        }

        let yxdata = newSiblings[yxIndex] || null
        if(yxdata && yxdata.sort == currentNode.sort){
            mustUpdateSameLevelSort = true
            newSiblings.forEach((item, index)=>{
                item.sort = (index + 1) * baseSort
                modifyDataArr.push(item)
            })
        }else{
            modifyDataArr.push(currentNode)
        }
        
        updateSortToServer(modifyDataArr);
        // 更新排序
        // const parent = findParent(menus.value, currentNode.parent)
        // let list = parent ? parent.children : menus.value
        // list.forEach((item, index) => {
        //     item.sort = index + 1
        // })
        // refreshTree();
    }

    let loadingMenuPage = ref(false)
    function getMenuData(){
        loadingMenuPage.value = true
        let params = {
            page:1,
            limit:999
        }
        Api.apiSystemMenu(params).then(res=>{
            loadingMenuPage.value = false
            if(res.code === 2000){
                // 将列表数据转换为树形数据
                menus.value = XEUtils.toArrayTree(res.data.data, { parentKey: 'parent' })
            }
        })
    }

    function handleNodeClick(data) {
        menuButtonList.value = []
        menuFieldList.value = []
        selectedMenu.value = data
        activeTab.value = 'button'
        getMenuButtonList()
    }

    function openButtonDialog() {
        currentForm.value = 'button'
        currentSaveMode.value = 'add'
        dialogTitle.value = '新增按钮权限'
        formData.value = {
            name:'',
            value: '',
            api: '',
            method: 0
        }
        dialogVisible.value = true
        getSchemeJson()
        getButtonTemplateData()
    }

    function editButton(row) {
        currentForm.value = 'button'
        currentSaveMode.value = 'edit'
        dialogTitle.value = '编辑按钮权限'
        formData.value = deepClone(row)
        dialogVisible.value = true
        getSchemeJson()
        getButtonTemplateData()
    }

    function deleteButton(row) {
        ElMessageBox.confirm('确定要删除该条数据吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
                Api.apiSystemMenuButtonDelete({id:row.id}).then(res=>{
                if(res.code === 2000){
                    getMenuButtonList()
                }else{
                    ElMessage.warning(res.msg)
                }
            })
        })
        .catch(() => {
        })
    }

    function getMenuButtonList(){
        isMenuButtonListLoading.value = true
        Api.apiSystemMenuButton({page:1,limit:999,menu:selectedMenu.value.id}).then(res=>{
            isMenuButtonListLoading.value = false
            if(res.code === 2000){
                menuButtonList.value = res.data.data
            }
        })
    }

    function openColumnDialog() {
        currentForm.value = 'column'
        currentSaveMode.value = 'add'
        dialogTitle.value = '新增列权限'
        formData.value = {
            title: '',
            model: '',
            menu:null,
            field_name: ''
        }
        dialogVisible.value = true
        getAllCustomModels()
    }

    function editColumn(row) {
        currentForm.value = 'column'
        currentSaveMode.value = 'edit'
        dialogTitle.value = '编辑列权限'
        formData.value = deepClone(row)
        dialogVisible.value = true
        getAllCustomModels()
    }

    function deleteColumn(row) {
        ElMessageBox.confirm('确定要删除该条数据吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
                Api.apiSystemMenuFieldDelete({id:row.id}).then(res=>{
                if(res.code === 2000){
                    getMenuFieldList()
                }else{
                    ElMessage.warning(res.msg)
                }
            })
        })
        .catch(() => {
        })
    }

    async function saveData() {
        if (currentForm.value === 'menu') {
            try {
                await formRefm.value.validate()
                loadingMenuPage.value=true
                let param = {
                    ...formData.value
                }
                let apiObj = Api.apiSystemMenuAdd
                if(currentSaveMode.value == 'edit'){
                    apiObj = Api.apiSystemMenuEdit
                }
                apiObj(param).then(res=>{
                    loadingMenuPage.value=false
                    if(res.code ==2000) {
                        // getMenuData()
                        window.location.reload()
                    } else {
                        ElMessage.warning(res.msg)
                        return
                    }
                })
                
            } catch (error) {
                // console.log('表单验证失败！', error)
                return
            }
            
        } else if (currentForm.value === 'button') {
            try {
                await formRefb.value.validate()
                isMenuButtonListLoading.value=true
                let param = {
                    ...formData.value
                }
                let apiObj;
                if(currentSaveMode.value == 'edit'){
                    apiObj = Api.apiSystemMenuButtonEdit
                }else{
                    apiObj = Api.apiSystemMenuButtonAdd
                    param['menu'] = selectedMenu.value.id
                }
                apiObj(param).then(res=>{
                    isMenuButtonListLoading.value=false
                    if(res.code ==2000) {
                        getMenuButtonList()
                    } else {
                        ElMessage.warning(res.msg)
                        return
                    }
                })
                
            } catch (error) {
                // console.log('表单验证失败！', error)
                return
            }

        } else if (currentForm.value === 'column') {
            try {
                await formRefc.value.validate()
                loadingMenuField.value=true
                let param = {
                    ...formData.value
                }
                let apiObj;
                if(currentSaveMode.value == 'edit'){
                    apiObj = Api.apiSystemMenuFieldEdit
                }else{
                    apiObj = Api.apiSystemMenuFieldAdd
                    param['menu'] = selectedMenu.value.id
                }
                apiObj(param).then(res=>{
                    loadingMenuField.value=false
                    if(res.code ==2000) {
                        getMenuFieldList()
                    } else {
                        ElMessage.warning(res.msg)
                        return
                    }
                })
                
            } catch (error) {
                // console.log('表单验证失败！', error)
                return
            }
        }

        dialogVisible.value = false
        ElMessage.success('保存成功')
    }

    function getMethodTagType(method) {
        switch (method) {
            case 0: return 'success'
            case 1: return 'primary'
            case 2: return 'warning'
            case 3: return 'danger'
            default: return ''
        }
    }

    function getMethodName(method) {
        switch (method) {
            case 0: return 'GET'
            case 1: return 'POST'
            case 2: return 'PUT'
            case 3: return 'DELETE'
            case 4: return 'OPTIONS'
            case 5: return 'WS'
            default: return ''
        }
    }

    function checkMobile() {
        isMobile.value = window.innerWidth < 768
    }

    function handleWebPathInput(e){
        if(formData.value.type === 1){
            formData.value.component_name = e.replace(/[\/:：]/g, '')
        }
    }

    function getSchemeJson(){
        Api.apiSchemeJson().then(res=>{
            var result = Object.keys(res.paths)
            var data = []
            for (const item of result) {
                const obj = {}
                obj.label = item
                obj.value = item
                data.push(obj)
            }
            apiList.value = data
        })
    }

    let moduleMenuButtonTableFlag = ref(null)
    let isDialogMenuButtonTableVisible = ref(false)
    function addMenuButtonTemplateTable(){
        isDialogMenuButtonTableVisible.value = true
        nextTick(() => {
            moduleMenuButtonTableFlag.value.handleOpen(null, "按钮模板")
        })
    }

    let moduleMenuButtonFlag = ref(null)
    let isDialogMenuButtonVisible = ref(false)
    function handleMenuButtonTemplateAdd(){
        isDialogMenuButtonVisible.value = true
        nextTick(() => {
            moduleMenuButtonFlag.value.handleOpen(null, "新增按钮模板")
        })
    }

    function handleRefreshMenuButtonTData(){
        moduleMenuButtonTableFlag.value.refresh()
    }

    function handleMenuButtonTemplateOp(row,op){
        if(op === 'edit'){
            isDialogMenuButtonVisible.value = true
            nextTick(() => {
                moduleMenuButtonFlag.value.handleOpen(row, "编辑按钮模板")
            })
        }else if(op === 'del'){
            ElMessageBox.confirm('确定要删除该条数据吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				 Api.apiSystemButtonTemplateDelete({id:row.id}).then(res=>{
                    if(res.code === 2000){
                        handleRefreshMenuButtonTData()
                    }else{
                        ElMessage.warning(res.msg)
                    }
                })
			})
			.catch(() => {
			})
        }
    }

    function getButtonTemplateData(){
        Api.apiSystemButtonTemplate({page:1,limit:999}).then(res=>{
            if(res.code === 2000){
                buttonList.value = res.data.data
            }
        })
    }

    function getApiButtonCode(val){
        // 根据 val 找到对应的完整 item
        const selectedItem = buttonList.value.find(item => item.name === val);
        if(selectedItem){
            formData.value.value = selectedMenu.value.component_name+":"+selectedItem.value
        }
    }

    function buttonBatchCreate(){
        if(selectedMenu.value && selectedMenu.value.type === 1){
            ElMessageBox.prompt('', '请输入RESTful接口前缀', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                inputPlaceholder:'如：/api/system/menu/'
            })
            .then(({ value }) => {
                Api.apiSystemMenuButtonBatchGenerate({'menu':selectedMenu.value.id,'baseapi':value}).then(res=>{
                    if(res.code === 2000){
                        getMenuButtonList()
                    }else{
                        ElMessage.warning(res.msg)
                    }
                })
            })
            .catch(() => {
            })
        }
    }

    let loadingMenuField = ref(false)
    function getMenuFieldList(){
        loadingMenuField.value = true
        menuFieldList.value = []
        Api.apiSystemMenuField({page:1,limit:999,menu:selectedMenu.value.id}).then(res=>{
            loadingMenuField.value = false
            if(res.code === 2000){
                menuFieldList.value = res.data.data
            }
        })
    }

    function FeildBatchCreate(){
        customMenuFeildModel.value = ""
        dialogAutoCreateFieldVisible.value = true
        getAllCustomModels()
    }

    function saveFeildBatchCreate(){
        if(selectedMenu.value && selectedMenu.value.type === 1){
            if(!customMenuFeildModel.value){
                ElMessage.warning("请提供模型名")
                return
            }
            Api.apiSystemMenuFieldAutoCreate({'menu':selectedMenu.value.id,'model':customMenuFeildModel.value}).then(res=>{
                if(res.code === 2000){
                    ElMessage.success(res.msg)
                    getMenuFieldList()
                    dialogAutoCreateFieldVisible.value = false
                }else{
                    ElMessage.warning(res.msg)
                }
            })
        }
    }

    function getAllCustomModels(){
        Api.apiSystemMenuFieldGetModels().then(res=>{
            if(res.code === 2000){
                allCustomModels.value = res.data
            }
        })
    }

    function handlePMChage(e){
        if(e === 'column'){
            getMenuFieldList()
        }else{
            getMenuButtonList()
        }
    }   

    // 生命周期钩子
    onMounted(() => {
        checkMobile()
        window.addEventListener('resize', checkMobile)
        getMenuData()
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

        :deep(.el-tree-node__content>.el-tree-node__expand-icon) {
            padding: unset;
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
            opacity: 1;
            transition: opacity 0.3s;
            
            .el-button {
                padding: 0 4px;
            }
        }
    
        // &:hover .actions {
        //     opacity: 1;
        // }
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