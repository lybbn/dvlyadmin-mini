import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {NotFound,RedirectRoute,staticRoutes} from '@/router/routes';

export const useTabsStore = defineStore('tabs', () => {
    const router = useRouter()
    const route = useRoute()

    const tabsList = ref([])
    const activeTab = ref('')

    // 添加标签
    const addTab = (tab) => {
        let noAddTabArr = [RedirectRoute.name,RedirectRoute.children[0].name, NotFound[0].name]
        staticRoutes.forEach(ele => {
            noAddTabArr.push(ele.name)
        });
        if (noAddTabArr.includes(tab.name) || !tab.name) {
            return;
        }
        // 检查是否已存在
        const index = tabsList.value.findIndex(item => item.path === tab.path)
        if (index === -1) {
            tabsList.value.push(tab)
        }
        activeTab.value = tab.path
    }

    // 移除标签
    const removeTab = (path) => {
        if (tabsList.value.length <= 1) return

        const index = tabsList.value.findIndex(item => item.path === path)
        if (index !== -1) {
            tabsList.value.splice(index, 1)
            
            // 如果删除的是当前活动标签，则跳转到前一个标签
            if (path === activeTab.value) {
                const prevTab = tabsList.value[index - 1] || tabsList.value[0]
                router.push(prevTab.path)
            }
        }
    }

    // 刷新标签
    const refreshTab = (path) => {
        if (path === route.path) {
            router.replace({ path: '/redirect' + path })
        }
    }

    // 关闭其他标签
    const closeOtherTabs = (path) => {
        tabsList.value = tabsList.value.filter(tab => 
            tab.path === path || tab.meta?.affix
        )
        if (path !== activeTab.value) {
            router.push(path)
        }
    }

    // 关闭所有标签
    const closeAllTabs = () => {
        // 保留固定的标签
        tabsList.value = tabsList.value.filter(tab => tab.meta?.affix)

        if (tabsList.value.length > 0) {
            const firstTab = tabsList.value[0]
            router.push(firstTab.path)
        } else {
            router.push('/')
        }
    }

    // 清除缓存
    const clearCache = () => {
        tabsList.value = []
        activeTab.value = ""
    }

    return {
        tabsList,
        activeTab,
        addTab,
        removeTab,
        refreshTab,
        closeOtherTabs,
        closeAllTabs
    }
},{
    persist: [
        {
            pick: ['tabsList','activeTab'],
            storage: localStorage,//sessionStorage
        }
    ],
})