/**
 * 自动生成面包屑配置
 * @param {RouteRecordRaw} route 路由记录
 * @param {RouteRecordRaw[]} allRoutes 所有路由
 * @param {string} parentPath 父路径
 * @returns {Array} 面包屑数组
 */
function generateBreadcrumb(route, allRoutes, parentPath = '') {
    // 如果已有自定义面包屑配置，则直接返回
    // if (route.meta?.breadcrumb) {
    //     return route.meta.breadcrumb
    // }

    const pathSegments = route.path.split('/').filter(Boolean)
    const breadcrumb = []

    // 查找父路由
    const parentRoute = allRoutes.find(r => {
        const parentSegments = r.path.split('/').filter(Boolean)
        return parentSegments.length === pathSegments.length - 1 && route.path.startsWith(r.path + '/')
    })

    // 如果有父路由，继承父路由的面包屑
    if (parentRoute) {
        const parentBreadcrumb = generateBreadcrumb(parentRoute, allRoutes, parentPath)
        breadcrumb.push(...parentBreadcrumb.slice(0, -1)) // 不包含父路由的最后一项
    } else if (pathSegments.length > 1) {
        // 添加首页
        breadcrumb.push({ title: '首页', path: '/' })
    }

    // 添加当前路由项
    const isDynamic = route.path.includes(':')
    let title = "未命名"
    try {
        title = route.meta?.title || 
                (pathSegments[pathSegments.length - 1]
                ?.replace(/-/g, ' ')
                ?.replace(/\b\w/g, l => l.toUpperCase())
                ?.replace(/:/g, ''));
        } catch (error) {
        title = "未命名"
    }

    breadcrumb.push({
        title,
        path: isDynamic ? null : route.path
    })

    return breadcrumb
}

/**
 * 包装路由配置，自动添加breadcrumb
 * @param {RouteRecordRaw[]} routes 原始路由配置
 * @returns {RouteRecordRaw[]} 处理后的路由配置
 */
export function withAutoBreadcrumb(routes) {
    return routes.map(route => {
        const processedRoute = { ...route }

        // 处理子路由
        if (Array.isArray(route.children)) {
            processedRoute.children = withAutoBreadcrumb(route.children)
        }

        // 自动生成breadcrumb
        if (!processedRoute.meta) {
            processedRoute.meta = {}
        }

        if (processedRoute.path && typeof processedRoute.path === 'string' && processedRoute.path != '/') {
            processedRoute.meta.breadcrumb = generateBreadcrumb(processedRoute, routes)
        }

        return processedRoute
    })
}