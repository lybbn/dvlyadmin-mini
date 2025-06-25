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
import { useTabsStore } from '@/store/tabs'

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
                let userState = useUserState()
                await userState.getSystemWebRouter(router);
                if (to.path === '/home') {//避免没有home首页时，跳转到第一个可用路由
                    const hasHomePath = userState.permissions.menus.some(route => route.web_path === '/home');
                    if (!hasHomePath) {
                        // 跳转到第一个路由
                        const firstRoute = getFirstMenuRoutePath(routesList.value)
                        return next(firstRoute); // 重定向到第一个路由
                    }
                }
                next({...to, replace: true});
            } else {
                if (to.path === '/home') {//避免没有home首页时，跳转到第一个可用路由
                    const hasHomePath = router.getRoutes().some(route => route.path === '/home');
                    if (!hasHomePath) {
                        // 跳转到第一个路由
                        const firstRoute = getFirstMenuRoutePath(routesList.value)
                        return next(firstRoute); // 重定向到第一个路由
                    }
                }
                next();
            }
        }
    }
})

function getCacheActiveTab(){
    let tabsStore = useTabsStore()
    return tabsStore.activeTab
}

function getFirstMenuRoutePath(menuList) {
    let c_tab_path = getCacheActiveTab()
    if(c_tab_path){
        return c_tab_path
    }
    const firstMenu = findFirstAvailableMenu(menuList)
    if (firstMenu) {
        return firstMenu.path
    }
    return '/'
}

// 递归查找第一个可用菜单
function findFirstAvailableMenu(menus) {
    for (const menu of menus) {
        // 跳过隐藏菜单、外链和404页面、重定向页面
        if (menu.meta?.hidden || menu.meta?.type === 3 || menu.name === 'notFound' || menu.name === 'RedirectTo') {
            continue
        }

        // 情况1：如果是菜单类型(type=1、2)，直接返回
        if (menu.meta?.type === 1 || menu.meta?.type === 2) {
            return menu
        }

        // 情况2：如果是目录(type=0)且有子菜单，递归查找
        if ((menu.meta?.type === 0 || menu.meta?.type === 2) && menu.children?.length) {
            const childMenu = findFirstAvailableMenu(menu.children)
            if (childMenu) {
                return childMenu
            }
        }
    }
    return null
}

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