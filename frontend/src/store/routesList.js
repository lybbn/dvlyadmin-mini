import { defineStore } from 'pinia';

export const useRoutesList = defineStore('routesList', {
	state:() => {
        return {
			//不存储到浏览器是刷新浏览器后可触发再次从后台加载路由
            routesList:[]
        }
    },
	getters:{

    },
	actions: {
		setRoutesList(data) {
			this.routesList = data;
		},
	}
});
