import {nextTick} from "vue"
import {createRouter, createWebHashHistory} from 'vue-router';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
import {staticRoutes,dynamicRoutes,CustomStaticRoutes,NotFound,RedirectRoute} from './routes';
import config from "@/config/index";
import {getToken,autoStorage} from '@/utils/util'
import {storeToRefs} from 'pinia';
import {useRoutesList} from '@/store/routesList';
import {ElNotification} from "element-plus"
import { cancelRequestState } from "@/store/cancelRequest";
import { useUserState } from "@/store/userState";
import { useTabsStore } from '@/store/tabs'
import { withAutoBreadcrumb } from '@/router/autoBreadcrumb.js'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [...staticRoutes,...dynamicRoutes],
});

//设置标题
document.title = config.APP_TITLE

//加载注册缓存后台路由
await updateDynamicRoutes()

router.beforeEach(async (to, from, next) => {
    // 处理根路径重定向
    if (to.path === '/') {
        // 检查是否是从/home来的重定向
        if (from.path === '/home') {
            return next(false) // 取消导航，避免循环
        }
        return next('/home') // 正常重定向
    }
    NProgress.configure({ showSpinner: false });
    if (to.meta.title) NProgress.start();
    
    // 清除所有 pending 的请求
    cancelRequestState().clearAllCancelToken();
    //动态标题
    //document.title = to.meta.title ? `${to.meta.title} - ${config.APP_TITLE}` : `${config.APP_TITLE}`
    const token = getToken();

    // 1. 处理登录页面的特殊情况
    if (to.path === '/login') {
        NProgress.done();
        return token ? next('/home') : next();
    }

    if(["/500","/404"].includes(to.path)){
        NProgress.done();
        return next()
    }
    
    // 2. 处理未认证情况
    if (!token) {
        autoStorage.clear();
        NProgress.done();
        // 如果需要认证且没有token，重定向到登录页
        let mustAuth = (to.meta?.requireAuth || to.name == "notFound" || to.name == undefined) ? true :false
        return mustAuth ? next('/login') : next();
    }

    const storesRoutesList = useRoutesList();
    const { routesList } = storeToRefs(storesRoutesList);
    const userState = useUserState();

    let isGetBackendRoute = false;
    // 3. 已认证用户处理动态路由
    try {
        // 加载动态路由（如果尚未加载）
        if (routesList.value.length === 0 && !isGetBackendRoute) {
            await nextTick();
            await userState.getSystemWebRouter(router);
            isGetBackendRoute = true
            // 重新触发导航以确保新路由生效
            return next(to.fullPath); 
        }
        // 检查目标路由是否存在
        const hasRoute = checkRouteExists(router, to);
        // 处理首页特殊情况
        if (to.path === '/home') {
            const hasHome = router.getRoutes().some(r => {
                // 检查路径是否包含 '/home'（包括子路由）
                const pathMatches  =  r.path == '/home' ? true : false;
                // 检查名称条件
                const nameCondition = to.name !== "notFound";
                return pathMatches && nameCondition;
            });
            if (!hasHome) {
                const firstRoute = getFirstMenuRoutePath(routesList.value);
                NProgress.done();
                // 确保不会重定向回/home
                const target = firstRoute && firstRoute !== '/home' ? firstRoute : '/404';
                return next(target)
            }
        }
        // 如果路由不存在
        if (!hasRoute) {
            NProgress.done();
            // 检查是否是动态路由加载后导致的404
            if (isGetBackendRoute) {
                return next('/404')
            }else{
                await userState.getSystemWebRouter(router)
                isGetBackendRoute = true
            }
            const retryHasRoute = router.getRoutes().some(r => r.path === to.path);
            return retryHasRoute ? next() : next('/404');
        }
        
        next();
    } catch (error) {
        NProgress.done();
        next('/500');
    }
});


async function updateDynamicRoutes() {
    let userState = localStorage.getItem('userState') || null
    let jsonUserState = userState?JSON.parse(userState) : null
    let menus = jsonUserState?jsonUserState?.menus : null
    if(menus){
        
        dynamicRoutes[0].children = transformMenuComponents(menus)
        let newdynamicRoutes = dynamicRoutes
        await initRoutes(router,newdynamicRoutes)
    }
}

/**
 * 将菜单数据中的 componentPath 转换为动态导入的 component
 * @param {Array} menus - 本地存储的菜单数据（含 componentPath）
 * @returns {Array} - 转换后的菜单数据（含 component 动态导入）
 */
function transformMenuComponents(menus) {
    return menus.map((menu) => {
        // 深拷贝当前菜单项（避免污染原数据）
        const transformedMenu = { ...menu };

        // 如果有 componentPath，转换为动态导入
        if (menu.meta?.componentPath) {
        transformedMenu.component = () => import(/* @vite-ignore */ `${menu.meta.componentPath}`);
        }

        // 递归处理子菜单
        if (menu.children && menu.children.length > 0) {
        transformedMenu.children = transformMenuComponents(menu.children);
        }

        return transformedMenu;
    });
}

export async function initRoutes(dRoutes=dynamicRoutes){
    let newrouter = await setAddRoute(dRoutes);
    return newrouter
}

async function setAddRoute(dRoutes=dynamicRoutes) {
	let routeChildren = await setFilterRoute(dRoutes=dynamicRoutes)
    // 先移除所有动态路由（避免重复添加）
    routeChildren.forEach(route => {
        router.removeRoute(route.name); 
    });
    // 添加新路由
    routeChildren.forEach((route) => {
		router.addRoute(route);
	});
    router.addRoute(RedirectRoute);
    router.addRoute(NotFound[0]);//外部404（非嵌套，未登录时有用）
    
    // 返回一个 Promise 确保路由更新完成
    return new Promise(resolve => {
        nextTick(() => resolve(router));
    });
}

//保留嵌套路由层级
async function setFilterRoute(dRoutes=dynamicRoutes) {
    let filterRoute = dRoutes
	filterRoute[0].children = [...filterRoute[0].children,...CustomStaticRoutes, ...NotFound];
    filterRoute = withAutoBreadcrumb(filterRoute)
	return filterRoute;
}

//检查路由是否存在
function checkRouteExists(router, to) {
  // 精确匹配路径或名称（排除notFound）
  return router.getRoutes().some(r => 
    r.path === to.path || 
    (r.name && r.name === to.name && to.name !== "notFound")
  );
}

function getCacheActiveTab(){
    let tabsStore = useTabsStore()
    return tabsStore.activeTab
}

function getFirstMenuRoutePath(menuList) {
    let c_tab_path = getCacheActiveTab()
    if(c_tab_path && c_tab_path !="/404" && c_tab_path !="/500"){
        return c_tab_path
    }
    const firstMenu = findFirstAvailableMenu(menuList)
    if (firstMenu) {
        return firstMenu.path
    }
    return ''
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