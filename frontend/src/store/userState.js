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
			taskInfo:{
				taskNumber:0,
				taskList:[],
			},
			msgInfo:{
				msgNumber:0,
			},
			serverInfo:{
				serverIp:'127.0.0.1',
			},
			fileInfo:{
				currentDir:"",//文件管理当前所在文件夹path路径
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
            licenseInfo:{
                did:"",
                username:"",
                role:"public",
                expire:"",
                create_at:"",
                active_state:"",//'1' 已激活、'0' 未激活、'2' 已离线
            },
            loadingInfo:{
				isLoading:false,//全局加载
				content:"",//提示内容
                restartMode:false,//是否重启模式
                delay:6,//延迟时间
			},
        }
    },
	getters:{

    },
	actions: {
		/**
         * 获取系统任务列表
         * @methods getSystemTaskIngInfo 获取系统任务列表(正在运行的)
         */
        async getSystemTaskIngInfo(){
            Api.sysTaskcenter({page:1,limit:999,action:'ing'}).then(res => {
                if (res.code == 2000) {
					this.taskInfo.taskNumber = res.data.total
                    this.taskInfo.taskList = res.data.data
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
        },
        /**
         * 取系统license
         */
        async getLicenseInfo(){
            Api.sysGetLicenses().then(res=>{
                if(res.code ==2000) {
                    let tempdata = res.data
                    if(isEmpty(tempdata.expire)){
                        tempdata.expire = "长期"
                    }
                    this.licenseInfo = tempdata
                }else{
                    ElMessage.warning(res.msg)
                }
            })
        },
        isProUserCheck(){
            if(this.licenseInfo.role != "pro"){
                ElMessage.warning("请升级为专业版")
                return false
            }
            return true
        }
	},
    persist: [
        {
            pick: ['userInfo','taskInfo','msgInfo','serverInfo','fileInfo','sysConfig','licenseInfo'],
            storage: sessionStorage,
        }
    ],
});
