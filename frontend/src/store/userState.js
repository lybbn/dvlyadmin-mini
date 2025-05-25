import { defineStore } from 'pinia';
import Api from '@/api/api'
import config from '@/config'
import { isEmpty } from '@/utils/util';
import { ElMessage } from 'element-plus'

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
            }
        }
    },
	getters:{

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
            pick: ['userInfo','msgInfo','sysConfig'],
            storage: sessionStorage,
        }
    ],
});
