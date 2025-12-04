import { defineStore } from 'pinia';
import Api from '@/api/api'
import config from '@/config'
import XEUtils from "xe-utils";
import {dynamicRoutes} from '@/router/routes.js';
import { generateLocalRoutes,initRoutes,resetDynamicRoutes } from '@/utils/routeGenerator'
import { useKeepAliveStore } from "@/store/keepAlive";
import defaultLogo from '@/assets/lybbn/imgs/logo.png'

export const useUserState = defineStore('userState', {
	state:() => {
        return {
            userInfo:{
                username:""
            },
            sysConfig:{
                sysVersion:config.APP_VER,
                loginCaptcha:false,
                logo:defaultLogo,
                systitle:config.APP_NAME
            },
            // 完整菜单树 (用于菜单渲染),是获取后台菜单转换后的路由配置
            menus: [],
            // 扁平化权限集合 (用于快速权限检查)
            permissions: {
                menus: [],    // 原始菜单路径
                buttons: [],  // {menuName:buttonCode}  menuName 菜单组件名 有唯一性
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
            let pcode = `${menuName}:${buttonCode}`
            return state.permissions.buttons.includes(pcode)
        },
    },
	actions: {
		/**
         * 获取用户信息
         * @methods getSystemUserInfo
         */
        async getSystemUserInfo(){
            const res = await Api.systemUserUserInfo()
            if (res.code == 2000) {
                this.userInfo = res.data
            }
        },
        /**
         * 获取菜单按钮权限
         * @methods getSystemUserInfo
         */
        async getMenuButtonPermission(){
            Api.apiSystemMenuButtonPermission().then(res => {
                if (res.code == 2000) {
					this.permissions.buttons = res.data
                }
            })
        },
        getComponentPath(component) {
            if (typeof component !== 'function') return null;

            // 匹配动态导入的路径
            const match = component.toString().match(/import\(["'](.*)["']\)/);
            return match ? match[1] : null;
        },
        /**
         * 转换后端菜单为路由配置
         * @param {Array} menus 后端菜单数据
         */
        transformMenuToRoutes(menus){
            const Component404 = () => import('@/views/system/error/404.vue')
            let localvuefiles = generateLocalRoutes()
            const KeepAliveStore = useKeepAliveStore()

            return menus.map(menu => {
                let route = {
                    id:menu.id,
                    parent:menu.parent,
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
                        isDynamic:true,
                        affix:false,//默认全部为非固定，如果要固定则可扩展或反馈dvlyadmin-mini的作者lybbn
                    }
                }
                KeepAliveStore.updateKeepAlive(route)
                // 动态加载组件(优先使用后台配置返回的菜单)
                if (menu.type == 1 && menu.component) {
                    try {
                        // 尝试加载目标组件
                        let componentPath = menu.component;
                        // 如果路径不包含扩展名，添加.vue
                        if (!componentPath.startsWith('/')) {
                            componentPath = `/${componentPath}`;
                        }
                        let fitem = localvuefiles.find(item => {
                            if(item.path === componentPath){
                                return true
                            }
                            if (item.name === menu.component_name) return true;
                            return false
                        })
                        if(fitem){
                            route.component = fitem.component
                        }else{
                            console.error("未找到本地vue文件，重启vite再试:",menu.component_name,fitem)
                            route.component = Component404
                        }
                    } catch (error) {
                        console.error('动态导入组件失败:', menu.component, error);
                        route.component = Component404
                    }
                    
                }else if(menu.type == 1 && menu.name && !menu.component){
                    //后台没配置组件的位置的话，利用route的name和文件名来匹配本地vue文件
                    let fitem = localvuefiles.find(item => item.name === menu.component_name)
                    if(fitem){
                        route.component = fitem.component
                    }else{
                        console.error("未找到本地vue文件，重启vite再试:",menu.component_name,fitem)
                        route.component = Component404
                    }
                }

                if(menu.type == 2){
                    route.component = () => import('@/layout/components/iframeView.vue')
                    route.name = menu.web_path
                }

                if(menu.type == 3){
                    route.component = () => import('@/layout/components/linkView.vue')
                }

                if(menu.type == 0){
                    route.name = route.name || `${route.id}-directory`; // 确保目录类型有 name,消除警告
                    route.path = route.path || `/${route.id}-directory`
                }

                // 处理子路由
                if (menu.children?.length) {
                    route.children = transformMenuToRoutes(menu.children)
                    // 自动重定向到第一个子路由
                    if (!menu.redirect && route.children.length > 0) {
                        route.redirect = `${route.path}/${route.children[0].path}`
                    }
                }
                route.meta.componentPath = this.getComponentPath(route.component)
                return route
            })
        },
        /**
         * 更新动态路由
         * @returns {Promise<boolean>} 是否更新成功
         */
        async updateDynamicRoutes(router) {
            try {
                // 清理旧路由
                resetDynamicRoutes(router)
                dynamicRoutes[0].children = this.menus
                let newdynamicRoutes = dynamicRoutes
                await initRoutes(router,newdynamicRoutes)
                return true
            } catch (error) {
                console.error('路由更新失败:', error)
                return false
            }
        },

        /**
         * 获取菜单
         */
        async getSystemWebRouter(router){
            const res = await Api.apiSystemWebRouter();
            if(res.code == 2000){
                let tmpdata = this.transformMenuToRoutes(res.data)
                this.permissions.menus = res.data
                this.menus = XEUtils.toArrayTree(tmpdata, { parentKey: 'parent', strict: true })
                await this.updateDynamicRoutes(router)
            }else{
                this.permissions.menus = []
                this.menus = []
                await this.updateDynamicRoutes(router)
            }
        },
        /**
         * 取系统配置
         */
        async getSystemConfig(){
            Api.getSysConfig().then(res=>{
                if(res.code == 2000){
                    this.sysConfig = res.data
                    this.sysConfig.sysVersion = config.APP_VER
                    if(!this.sysConfig?.logo){
                        this.sysConfig.logo = defaultLogo
                    }
                    if(!this.sysConfig?.systitle){
                        this.sysConfig.systitle = config.APP_NAME
                    }
                }
            })
        }
	},
    persist: [
        {
            pick: ['userInfo','sysConfig','menus','permissions'],
            storage: localStorage,//sessionStorage
        }
    ],
});
