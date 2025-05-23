import { defineStore } from 'pinia';

export const useRoutesList = defineStore('routesList', {
	state:() => {
        return {
            routesList:[]
        }
    },
	getters:{

    },
	actions: {
		setRoutesList(data) {
			this.routesList = data;
		},
	},
});
