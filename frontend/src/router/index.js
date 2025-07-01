import {createRouter, createWebHashHistory} from 'vue-router';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
import {staticRoutes,dynamicRoutes} from './routes';
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
    routes: [...staticRoutes,...dynamicRoutes],
});

//设置标题
document.title = config.APP_TITLE

router.beforeEach(async (to, from, next) => {
    NProgress.configure({ showSpinner: false });
    if (to.meta.title) NProgress.start();
    
    // 清除所有 pending 的请求
    cancelRequestState().clearAllCancelToken();
    //动态标题
    //document.title = to.meta.title ? `${to.meta.title} - ${config.APP_TITLE}` : `${config.APP_TITLE}`
    const token = getToken();

    // 1. 处理登录页面的特殊情况
    if (to.path === '/login') {
        if (token) {
            // 已登录却访问登录页，重定向到首页
            NProgress.done();
            return next('/home');
        }
        // 未登录访问登录页，直接放行
        NProgress.done();
        return next();
    }
    
    // 2. 处理未认证情况
    if (!token) {
        autoStorage.clear();
        NProgress.done();
        // 如果需要认证且没有token，重定向到登录页
        let mustAuth = (to.meta?.requireAuth || to.name == "notFound" || to.name == undefined) ? true :false
        if (mustAuth) {
            return next(`/login`);
        }
        return next();
    }
    const storesRoutesList = useRoutesList();
    const { routesList } = storeToRefs(storesRoutesList);
    const userState = useUserState();

    let isGetBackendRoute = false;

    // 3. 已认证用户处理动态路由
    try {
        // 加载动态路由（如果尚未加载）
        if (routesList.value.length === 0 && !isGetBackendRoute) {
            await userState.getSystemWebRouter(router);
            isGetBackendRoute = true
        }

        // 检查目标路由是否存在
        const hasRoute = router.getRoutes().some(r => 
        r.path === to.path || 
        (r.name && r.name === to.name && to.name != "notFound")
        );
        // 处理首页特殊情况
        if (to.path === '/home') {
            const hasHome = router.getRoutes().some(r => r.path === '/home' && to.name != "notFound");
            if (!hasHome) {
                const firstRoute = getFirstMenuRoutePath(routesList.value);
                NProgress.done();
                return firstRoute ? next(firstRoute) : next('/404');
            }
        }
        // 如果路由不存在
        if (!hasRoute) {
            NProgress.done();
            // 检查是否是动态路由加载后导致的404
            if (routesList.value.length > 0) {
                return next('/404');
            }
            // 可能是动态路由尚未加载，尝试重新加载
            if (!isGetBackendRoute) {
                await userState.getSystemWebRouter(router);
                isGetBackendRoute = true
            }
            const retryHasRoute = router.getRoutes().some(r => r.path === to.path);
            return retryHasRoute ? next() : next('/404');
        }

        next();
    } catch (error) {
        console.error('路由守卫错误:', error);
        NProgress.done();
        next('/500');
    }
});

// router.beforeEach(async (to, from, next) => {
//     NProgress.configure({showSpinner: false});
//     if (to.meta.title) NProgress.start();
//     const cancelReques = cancelRequestState();
//     cancelReques.clearAllCancelToken()
//     //动态标题
// 	//document.title = to.meta.title ? `${to.meta.title} - ${config.APP_TITLE}` : `${config.APP_TITLE}`
//     const token = getToken()
//     if (to.path === '/login' && !token) {
//         next();
//         NProgress.done();
//     } else {
//         if (!token && to.meta.requireAuth) {
//             next(`/login`);
//             autoStorage.clear();
//             NProgress.done();
//         } else if (token && to.path === '/login') {
//             next('/home');
//             NProgress.done();
//         } else if(!token){
//             next(`/login`);
//             autoStorage.clear();
//             NProgress.done();
//         }else {
//             const storesRoutesList = useRoutesList();
//             const {routesList} = storeToRefs(storesRoutesList);
//             if (routesList.value.length === 0) {
//                 let userState = useUserState()
//                 await userState.getSystemWebRouter(router);
//                 if (to.path === '/home') {//避免没有home首页时，跳转到第一个可用路由
//                     const hasHomePath = userState.permissions.menus.some(route => route.web_path === '/home');
//                     if (!hasHomePath) {
//                         // 跳转到第一个路由
//                         const firstRoute = getFirstMenuRoutePath(routesList.value)
//                         return next(firstRoute); // 重定向到第一个路由
//                     }
//                 }
//                 next({...to, replace: true});
//             } else {
//                 if (to.path === '/home') {//避免没有home首页时，跳转到第一个可用路由
//                     const hasHomePath = router.getRoutes().some(route => route.path === '/home');
//                     if (!hasHomePath) {
//                         // 跳转到第一个路由
//                         const firstRoute = getFirstMenuRoutePath(routesList.value)
//                         return next(firstRoute); // 重定向到第一个路由
//                     }
//                 }
//                 next();
//             }
//         }
//     }
// })

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
        //如果第一个页面就是404页面，证明没有获取到后台菜单列表，直接返回404
        if(menu.name == '404'){
            return menu
        }
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