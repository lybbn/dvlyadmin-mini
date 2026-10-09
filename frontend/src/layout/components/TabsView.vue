<template>
    <div class="tabs-view-container" :class="{ 'mobile-tabs': ismobile }">
        <!-- 桌面端标签栏 -->
        <div v-if="!ismobile" class="tabs-view">
            <el-scrollbar class="tabscrollbar">
                <div class="tabs-list">
                    <div v-for="tab in tabsList" :key="tab.path" class="tabs-item" :class="{ 'is-active': tab.path === activeTab }"
                    @click="tabClick(tab)"
                    @contextmenu.prevent="openContextMenu($event, tab)"
                    >
                        <span>{{ tab.title }}</span>
                        <el-icon v-if="!tab.meta?.affix" class="tabs-close" @click.stop="removeTab(tab)">
                            <Close />
                        </el-icon>
                    </div>
                </div>
            </el-scrollbar>
            <div class="tabs-extra">
                <el-dropdown trigger="click" popper-class="ly-tabmenu-popper" @command="handleTabCommand">
                    <el-icon class="tabs-dropdown-icon">
                        <ArrowDown />
                    </el-icon>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="closeOther">关闭其他</el-dropdown-item>
                            <el-dropdown-item command="closeAll">关闭所有</el-dropdown-item>
                            <el-dropdown-item command="refresh">刷新当前</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>

        <!-- 移动端标签栏 -->
        <div v-else class="mobile-tabs-view">
            <el-dropdown trigger="click" popper-class="ly-tabmenu-popper" @command="handleMobileTabCommand">
                <div class="mobile-tabs-current">
                    <span>{{ currentTabTitle }}</span>
                    <el-icon class="mobile-tabs-icon">
                        <ArrowDown />
                    </el-icon>
                </div>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item
                            v-for="tab in tabsList"
                            :key="tab.path"
                            :command="tab.path"
                            :class="{ 'is-active': tab.path === activeTab }"
                        >
                            <div class="mobile-tab-item">
                            <span>{{ tab.title }}</span>
                            <el-icon
                                v-if="!tab.meta?.affix"
                                class="mobile-tab-close"
                                @click.stop="removeTab(tab)"
                            >
                                <Close />
                            </el-icon>
                            </div>
                        </el-dropdown-item>
                        <el-dropdown-item divided command="closeOther">
                            关闭其他
                        </el-dropdown-item>
                        <el-dropdown-item command="closeAll">关闭所有</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>

        <!-- 右键菜单 -->
        <ul v-show="contextMenuVisible" class="tabs-contextmenu" :style="{ left: contextMenuLeft + 'px', top: contextMenuTop + 'px' }">
            <li @click="refreshTab">刷新</li>
            <li @click="closeOtherTabs">关闭其他</li>
            <li @click="closeAllTabs">关闭所有</li>
            <li @click="closeContextMenu">取消</li>
        </ul>
    </div>
</template>

<script setup>
    import { ref, computed, watch, onMounted } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    import { useSiteThemeStore } from '@/store/siteTheme'
    import { useTabsStore } from '@/store/tabs'

    const router = useRouter()
    const route = useRoute()
    const siteThemeStore = useSiteThemeStore()
    const tabsStore = useTabsStore()

    const ismobile = computed(() => siteThemeStore.ismobile)
    const tabsList = computed(() => tabsStore.tabsList)
    const activeTab = computed(() => tabsStore.activeTab)

    // 当前标签标题（移动端用）
    const currentTabTitle = computed(() => {
        const tab = tabsList.value.find(tab => tab.path === activeTab.value)
        return tab?.title || ''
    })

    // 右键菜单相关
    const contextMenuVisible = ref(false)
    const contextMenuLeft = ref(0)
    const contextMenuTop = ref(0)
    const contextMenuTab = ref(null)

    // 点击标签
    const tabClick = tab => {
        router.push(tab.path)
    }

    // 移除标签
    const removeTab = tab => {
        tabsStore.removeTab(tab.path)
    }

    // 打开右键菜单
    const openContextMenu = (e, tab) => {
        contextMenuVisible.value = true
        contextMenuLeft.value = e.clientX
        contextMenuTop.value = e.clientY
        contextMenuTab.value = tab
    }

    // 关闭右键菜单
    const closeContextMenu = () => {
        contextMenuVisible.value = false
    }

    // 刷新当前标签
    const refreshTab = () => {
        if (contextMenuTab.value) {
            tabsStore.refreshTab(contextMenuTab.value.path)
        }
        closeContextMenu()
    }

    // 关闭其他标签
    const closeOtherTabs = () => {
        if (contextMenuTab.value) {
            tabsStore.closeOtherTabs(contextMenuTab.value.path)
        }
        closeContextMenu()
    }

    // 关闭所有标签
    const closeAllTabs = () => {
        tabsStore.closeAllTabs()
        closeContextMenu()
    }

    // 处理标签下拉菜单命令
    const handleTabCommand = command => {
        switch (command) {
            case 'refresh':
                tabsStore.refreshTab(activeTab.value)
            break
            case 'closeOther':
                tabsStore.closeOtherTabs(activeTab.value)
            break
            case 'closeAll':
                tabsStore.closeAllTabs()
            break
        }
    }

    // 处理移动端标签下拉菜单命令
    const handleMobileTabCommand = path => {
        if (path === 'closeOther') {
            tabsStore.closeOtherTabs(activeTab.value)
        } else if (path === 'closeAll') {
            tabsStore.closeAllTabs()
        } else {
            router.push(path)
        }
    }

    // 点击其他地方关闭右键菜单
    const handleClickOutside = e => {
        if (!e.target.closest('.tabs-contextmenu')) {
            closeContextMenu()
        }
    }

    onMounted(() => {
        document.addEventListener('click', handleClickOutside)
    })

    // 监听路由变化
    watch(
        () => route.path,
        newPath => {
            const tab = {
                path: newPath,
                title: route.meta?.title || '未命名',
                meta: route.meta,
                name:route.name
            }
            tabsStore.addTab(tab)
        },
        { immediate: true }
    )
</script>

<style scoped>
    /* 标签栏：透明容器 + 芯片式标签（融入玻璃顶栏与极光背景） */
    .tabs-view-container {
        height: 42px;
        padding: 8px 0 4px;
        background: transparent;
        box-shadow: none;
    }

    /* 桌面端标签样式 */
    .tabs-view {
        display: flex;
        height: 100%;
        border-bottom: none;
    }

    .tabs-view .el-scrollbar {
        flex: 1;
        height: 100%;
    }

    .tabscrollbar:deep(.el-scrollbar__view){
        height: 100%;
        width: 100%;
    }

    .tabs-list {
        display: flex;
        align-items: center;
        height: 100%;
        padding: 0 10px;
    }

    .tabs-item {
        position: relative;
        display: flex;
        align-items: center;
        height: 26px;
        padding: 0 12px;
        margin: 0 3px;
        font-size: 12.5px;
        cursor: pointer;
        color: var(--ly-text-2);
        border: none;
        border-radius: 13px;
        transition: color .15s ease, background .15s ease, box-shadow .15s ease;
        flex-shrink: 0;
        white-space: nowrap;
    }

    .tabs-item:hover {
        color: var(--ly-color-primary);
        background: var(--ly-header-item-hover);
    }

    .tabs-item.is-active {
        color: #fff;
        background: var(--ly-gradient-primary);
        box-shadow: var(--ly-sidebar-active-shadow);
    }

    .tabs-item.is-active::after {
        display: none;
    }

    .tabs-item.is-active::before {
        content: "";
        background: #fff;
        display: inline-block;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        position: relative;
        margin-right: 5px;
        opacity: .9;
    }

    .tabs-close {
        margin-left: 8px;
        font-size: 12px;
        color: var(--el-text-color-secondary);
        border-radius: 50%;
        transition: all .15s ease;
    }

    .tabs-close:hover {
        color: var(--el-color-white);
        background-color: var(--el-color-primary-light-3);
        transform: scale(1.1);
    }

    .tabs-item.is-active .tabs-close {
        color: rgba(255, 255, 255, 0.85);
    }

    .tabs-item.is-active .tabs-close:hover {
        color: #fff;
        background-color: rgba(255, 255, 255, 0.25);
    }

    .tabs-extra {
        display: flex;
        align-items: center;
        padding: 0 10px;
        border-left: none;
    }

    .tabs-dropdown-icon {
        cursor: pointer;
        color: var(--ly-text-3);
    }

    .tabs-dropdown-icon:hover {
        color: var(--el-color-primary);
    }

    /* 移动端标签样式 */
    .mobile-tabs-view {
        height: 100%;
        padding: 0 15px;
        border-bottom: 1px solid var(--el-border-color-light);
        display: flex;
        align-items: center;
    }

    .mobile-tabs-current {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 100%;
        color: var(--el-text-color-regular);
    }

    .mobile-tabs-icon {
        margin-left: 8px;
        color: var(--el-text-color-secondary);
    }

    .mobile-tab-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }

    .mobile-tab-close {
        margin-left: 8px;
        color: var(--el-text-color-secondary);
    }

    .mobile-tab-close:hover {
        color: var(--el-color-danger);
    }

    .el-dropdown-menu .is-active {
        color: var(--el-color-primary);
        background-color: var(--el-color-primary-light-9);
    }

    /* 标签栏下拉菜单：玻璃化圆角（append-to-body 场景用全局类名覆盖） */
    .tabs-contextmenu {
        position: fixed;
        z-index: 3000;
        margin: 0;
        padding: 6px;
        list-style-type: none;
        background-color: var(--ly-glass-bg-strong);
        backdrop-filter: var(--ly-glass-blur);
        -webkit-backdrop-filter: var(--ly-glass-blur);
        border: 1px solid var(--ly-glass-border);
        border-radius: var(--ly-radius-md);
        box-shadow: var(--ly-shadow-card);
        overflow: hidden;
    }

    .tabs-contextmenu li {
        padding: 8px 14px;
        font-size: 13px;
        color: var(--ly-text-2);
        cursor: pointer;
        border-radius: 8px;
        margin: 2px 2px;
        transition: all .13s ease;
    }

    .tabs-contextmenu li:hover {
        background: var(--ly-gradient-primary);
        color: #fff;
    }

    /* 响应式调整 */
    @media screen and (max-width: 768px) {
        .tabs-view-container {
            height: 28px;
        }
        
        .mobile-tabs-current {
            font-size: 14px;
        }
    }
</style>