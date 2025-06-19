import {createRouter, createWebHashHistory} from 'vue-router';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
import {staticRoutes} from './routes';
import config from "@/config/index";
import {getToken,autoStorage} from '@/utils/util'
import {storeToRefs} from 'pinia';
import {useRoutesList} from '@/store/routesList';
import {ElNotification} from "element-plus"
import { cancelRequestState } from "@/store/cancelRequest";
import {initRoutes} from '@/utils/routeGenerator.js'

const router = createRouter({
    history: createWebHashHistory(),
    routes: staticRoutes,
});

//设置标题
document.title = config.APP_TITLE

router.beforeEach(async (to, from, next) => {
    NProgress.configure({showSpinner: false});
    if (to.meta.title) NProgress.start();
    const cancelReques = cancelRequestState();
    cancelReques.clearAllCancelToken()
    //动态标题
	//document.title = to.meta.title ? `${to.meta.title} - ${config.APP_TITLE}` : `${config.APP_TITLE}`
    const token = getToken()
    if (to.path === '/login' && !token) {
        next();
        NProgress.done();
    } else {
        if (!token && to.meta.requireAuth) {
            next(`/login`);
            autoStorage.clear();
            NProgress.done();
        } else if (token && to.path === '/login') {
            next('/home');
            NProgress.done();
        } else if(!token){
            next(`/login`);
            autoStorage.clear();
            NProgress.done();
        }else {
            const storesRoutesList = useRoutesList();
            const {routesList} = storeToRefs(storesRoutesList);
            if (routesList.value.length === 0) {
                await initRoutes(router);
                next({...to, replace: true});
            } else {
                next();
            }
        }
    }
})

router.afterEach(() => {
    NProgress.done();
});

router.onError((error) => {
	NProgress.done();
	ElNotification.error({
		title: '路由错误',
		message: error.message
	});
});

// 导出路由
export default router;