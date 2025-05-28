import { defineStore } from 'pinia';
import Api from '@/api/api'
import config from '@/config'

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
                buttons: {},  // {menuPath: [buttonCode1, buttonCode2]}
                columns: {}   // {tableName: {columnName: permissionType}}
            }
        }
    },
	getters:{
        // 检查是否有菜单权限
        hasMenuPermission: (state) => (menuPath) => {
            return state.permissions.menus.includes(menuPath)
        },
        // 检查是否有按钮权限
        hasButtonPermission: (state) => (menuPath, buttonCode) => {
            return state.permissions.buttons[menuPath]?.includes(buttonCode) || false
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
         * 获取菜单
         */
        async getSystemWebRouter(){
            Api.apiSystemWebRouter().then(res=>{
                if(res.code == 2000){
                    this.menus = res.data.data
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
