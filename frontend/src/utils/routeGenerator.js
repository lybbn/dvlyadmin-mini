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
        '!/src/views/**/components/**'
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