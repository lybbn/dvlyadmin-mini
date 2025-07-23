import {useRoutesList} from '@/store/routesList';
import {CustomStaticRoutes,staticRoutes,NotFound,RedirectRoute,dynamicRoutes} from '@/router/routes.js';
import { withAutoBreadcrumb } from '@/router/autoBreadcrumb.js'

export function generateLocalRoutes() {
    // 定义需要排除的路径
    const excludes = [
        '/system/home',
        '/system/login',
        '/system/login/register',
        '/system/redirect',
        '/system/error/404'
    ];

    // 获取所有非components目录的vue文件
    const modules = import.meta.glob([
        '/src/views/**/*.vue',
        '!/src/views/**/components/**/*.vue'
    ]);

    return Object.entries(modules)
        .map(([path, component]) => {
            const filename = path
                .split('/').pop()         // 获取最后一部分
                .replace(/\.vue$/, '');   // 移除.vue扩展名

            const routePath = path
                .replace(/^\/src\/views/, '')
                .replace(/\.vue$/, '')
                .replace(/\/index$/, '')
                || '/';

            return {
                path: routePath,
                component,
                name: filename
            };
        })
        // 过滤掉排除路径
        .filter(route => !excludes.includes(route.path));
}


export async function initRoutes(router,dRoutes=dynamicRoutes){
    let newrouter = await setAddRoute(router,dRoutes);
    return newrouter
}

async function setAddRoute(router,dRoutes=dynamicRoutes) {
	let routeChildren = await setFilterRoute(router,dRoutes=dynamicRoutes)
    routeChildren.forEach((route) => {
		router.addRoute(route);
	});
    router.addRoute(RedirectRoute);
    router.addRoute(NotFound[0]);//外部404（非嵌套，未登录时有用）
    
    const storesRoutesList = useRoutesList();
	storesRoutesList.setRoutesList(routeChildren[0].children);
    return router
}

//保留嵌套路由层级
async function setFilterRoute(router,dRoutes=dynamicRoutes) {
    let filterRoute = dRoutes
	filterRoute[0].children = [...filterRoute[0].children,...CustomStaticRoutes, ...NotFound];
    filterRoute = withAutoBreadcrumb(filterRoute)
	return filterRoute;
}

// 重置动态路由
export async function resetDynamicRoutes(router) {
    const routes = router.getRoutes();
    
    routes.forEach(route => {
        // 确保满足所有条件再删除
        if (route.name && route.meta?.isDynamic) {
            try {
                router.removeRoute(route.name);
            } catch (err) {
                console.warn(`删除路由失败: ${route.name}`, err);
            }
        }
    });
}