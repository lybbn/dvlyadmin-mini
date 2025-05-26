import {createRouter, createWebHashHistory} from 'vue-router';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
import {CustomStaticRoutes,staticRoutes,NotFound,RedirectRoute,dynamicRoutes} from './routes';
import { withAutoBreadcrumb } from './autoBreadcrumb.js'
import config from "@/config/index";
import {getToken,autoStorage} from '@/utils/util'
import {storeToRefs} from 'pinia';
import {useRoutesList} from '@/store/routesList';
import {ElNotification} from "element-plus"
import { cancelRequestState } from "@/store/cancelRequest";

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
        } else {
            const storesRoutesList = useRoutesList();
            const {routesList} = storeToRefs(storesRoutesList);
            if (routesList.value.length === 0) {
                await initRoutes();
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

async function initRoutes(){
    await setAddRoute();
}

async function setAddRoute() {
	let routeChildren = await setFilterRoute()
    routeChildren.forEach((route) => {
		router.addRoute(route);
	});
    router.addRoute(RedirectRoute);
    router.addRoute(NotFound[0]);//外部404（非嵌套，未登录时有用）
    const storesRoutesList = useRoutesList();
	storesRoutesList.setRoutesList(routeChildren[0].children);
}

//保留嵌套路由层级
async function setFilterRoute() {
    let filterRoute = dynamicRoutes
	filterRoute[0].children = [...filterRoute[0].children,...CustomStaticRoutes, ...NotFound];
    filterRoute = withAutoBreadcrumb(filterRoute)
	return filterRoute;
}

// 导出路由
export default router;