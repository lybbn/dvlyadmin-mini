import { defineStore } from 'pinia'

export const useKeepAliveStore = defineStore('keepAlive', {
    state:() => {
        return {
            routeShow: true,
            keepAliveRoute:[],//希望缓存的页面name，如['server'],后台菜单的cache会覆盖此变量
        }
    },
    getters:{

    },
    actions: {
        // 根据路由更新缓存列表（自动去重）
        updateKeepAlive(route) {
            if (route.meta?.isKeepAlive && route.name) {
                if (!this.keepAliveRoute.includes(route.name)) {
                    this.keepAliveRoute = [...this.keepAliveRoute, route.name];
                }
            }else if(!route.meta?.isKeepAlive && route.name){
                if (this.keepAliveRoute.includes(route.name)) {
                    this.keepAliveRoute = this.keepAliveRoute.filter(name => name !== route.name);
                }
            }
        },
        // 清空所有缓存
        clearKeepAlive() {
            this.keepAliveRoute = [];
        },
    },
    persist: [
        {
            pick: ['keepAliveRoute'],
            storage: sessionStorage,
        }
    ],
})