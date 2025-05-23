import { defineStore } from 'pinia'
import {autoStorage} from '@/utils/util'

export const useKeepAliveStore = defineStore('keepAlive', {
    state:() => {
        return {
            routeShow: true,
            keepAliveRoute:[],//希望缓存的页面name，如['server']
        }
    },
    getters:{

    },
    actions: {
        setKeepAliveRoute(val) {
            this.keepAliveRoute = val;
            autoStorage.set('keepAliveRoute',val);
        },
        setRouteShow(val){
			this.routeShow = val
            autoStorage.set('routeShow',val);
		}
    },
})