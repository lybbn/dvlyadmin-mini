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
import { useUserState } from "@/store/userState";

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
            console.log(router.hasRoute('home'))
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
                let userState = useUserState()
                await userState.getSystemWebRouter(router);
                if (to.path === '/home') {//避免没有home首页时，跳转到第一个可用路由
                    const hasHomePath = userState.permissions.menus.some(route => route.web_path === '/home');
                    if (!hasHomePath) {
                        // 跳转到第一个路由
                        const firstRoute = routesList.value[0]?.path
                        return next(firstRoute); // 重定向到第一个路由
                    }
                }
                next({...to, replace: true});
            } else {
                if (to.path === '/home') {//避免没有home首页时，跳转到第一个可用路由
                    const hasHomePath = router.getRoutes().some(route => route.path === '/home');
                    if (!hasHomePath) {
                        // 跳转到第一个路由
                        const firstRoute = routesList.value[0]?.path
                        return next(firstRoute); // 重定向到第一个路由
                    }
                }
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