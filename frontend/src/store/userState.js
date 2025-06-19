import { defineStore } from 'pinia';
import Api from '@/api/api'
import config from '@/config'
import XEUtils from "xe-utils";
import { generateLocalRoutes } from '@/utils/routeGenerator'

export const useUserState = defineStore('userState', {
	state:() => {
        return {
            userInfo:{
                username:""
            },
			msgInfo:{
				msgNumber:0,
			},
            sysConfig:{
                sysVersion:config.APP_VER,
                webServer:"",
                wwwrootPath:"",
                siteNums:0,
                dbNums:0,
                softNums:0,
                currentOs:"windows",
            },
            // 完整菜单树 (用于菜单渲染)
            menus: [],
            // 扁平化权限集合 (用于快速权限检查)
            permissions: {
                menus: [],    // 可访问的菜单路径
                buttons: [],  // {menuName: [buttonCode1, buttonCode2]}  menuName 菜单组件名 有唯一性
                columns: []   // {tableName: {columnName: permissionType}}
            }
        }
    },
	getters:{
        // 检查是否有菜单权限
        hasMenuPermission: (state) => (menuName) => {
            return state.permissions.menus.includes(menuName)
        },
        // 检查是否有按钮权限
        hasButtonPermission: (state) => (menuName, buttonCode) => {
            return state.permissions.buttons[menuName]?.includes(buttonCode) || false
        },
        // 获取列权限
        getColumnPermission: (state) => (tableName, columnName) => {
            return state.permissions.columns[tableName]?.[columnName] || 'write' // 默认可写
        }
    },
	actions: {
		/**
         * 获取用户信息
         * @methods getSystemUserInfo
         */
        async getSystemUserInfo(){
            Api.systemUserUserInfo().then(res => {
                if (res.code == 2000) {
					this.userInfo = res.data
                }
            })
        },
        /**
         * 动态导入Vue组件
         * @param {Object} dynamicViewsModules - import.meta.glob返回的对象 
         * @param {String} componentPath - 组件路径 (如 'system/user/index')
         * @returns {Promise<Component>}
         */
        async dynamicImport(dynamicViewsModules, componentPath) {
            // 标准化路径格式（统一为相对路径）
            const normalizedPath = componentPath.startsWith('/') 
                ? componentPath.slice(1) 
                : componentPath

            // 1. 精确匹配（优先尝试）
            const exactKey = `../views/${normalizedPath}.vue`
            if (dynamicViewsModules[exactKey]) {
                return dynamicViewsModules[exactKey]()
            }

            // 2. 模糊匹配（兼容不同路径格式）
            const keys = Object.keys(dynamicViewsModules)
            const matchKeys = keys.filter(key => {
                // 移除路径前缀和扩展名
                const cleanKey = key
                .replace(/^..\/views\//, '')
                .replace(/\.vue$/, '')
                .replace(/\/index$/, '')
                
                // 匹配组件路径
                return cleanKey === normalizedPath || 
                    cleanKey.endsWith(`/${normalizedPath}`)
            })

            // 匹配结果处理
            if (matchKeys.length === 1) {
                return dynamicViewsModules[matchKeys[0]]()
            }

            if (matchKeys.length > 1) {
                console.warn(`找到多个匹配组件: ${matchKeys.join(', ')}`)
                return dynamicViewsModules[matchKeys[0]]() // 返回第一个匹配项
            }

            // 匹配失败处理
            console.log(`未找到组件: ${componentPath}`)
        },
        /**
         * 转换后端菜单为路由配置
         * @param {Array} menus 后端菜单数据
         */
        transformMenuToRoutes(menus){
            const Component404 = () => import('@/views/system/error/404.vue')
            let localvuefiles = generateLocalRoutes()
            return menus.map(menu => {
                let route = {
                    path: menu.web_path,
                    name: menu.component_name,
                    meta: {
                        type:menu.type,
                        link:menu.link_url,
                        title: menu.name,
                        icon: menu.icon,
                        hidden : !menu.visible,
                        requiresAuth: true,
                        isKeepAlive:menu.cache,
                        affix:false,
                    }
                }

                // 动态加载组件(优先使用后台配置返回的菜单)
                if (menu.type == 1 && menu.component) {
                    try {
                        // 尝试加载目标组件
                        route.component = () => import(`@/views/${menu.component}.vue`)
                    } catch (error) {
                        route.component = Component404
                    }
                    
                }else if(menu.type == 1 && menu.name && !menu.component){
                    //后台没配置组件的位置的话，利用route的name和文件名来匹配本地vue文件
                    let fitem = localvuefiles.find(item => item.name === menu.component_name)
                    if(fitem){
                        route.component = fitem.component
                    }else{
                        route.component = Component404
                    }
                }

                // 处理子路由
                if (menu.children?.length) {
                    route.children = transformMenuToRoutes(menu.children)
                    // 自动重定向到第一个子路由
                    if (!menu.redirect && route.children.length > 0) {
                        route.redirect = `${route.path}/${route.children[0].path}`
                    }
                }

                return route
            })
        },

        /**
         * 获取菜单
         */
        async getSystemWebRouter(){
            Api.apiSystemWebRouter().then(res=>{
                if(res.code == 2000){
                    let tmpdata = this.transformMenuToRoutes(res.data)
                    this.permissions.menus = tmpdata
                    this.menus = XEUtils.toArrayTree(tmpdata, { parentKey: 'parent', strict: false })
                    console.log(this.menus)
                }
            })
        },
        /**
         * 取系统配置
         */
        async getSystemConfig(){
            Api.sysGetSettings().then(res=>{
                if(res.code == 2000){
                    this.sysConfig = res.data
                    this.serverInfo.serverIp = !!res.data.serverIp?res.data.serverIp:"127.0.0.1"
                    this.userInfo.username = res.data.username
                }
            })
        }
	},
    persist: [
        {
            pick: ['userInfo','msgInfo','sysConfig','menus','permissions'],
            storage: sessionStorage,
        }
    ],
});
