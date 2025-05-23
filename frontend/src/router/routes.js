//动态路由
export const dynamicRoutes = [
	{
		path: '/',
		name: 'layout',
		component: () => import('@/layout/index.vue'),
        redirect: '/home',
        meta: {
			title: "",
			isKeepAlive: false,
            requireAuth: false,
		},
		children: [
			{
				path: "/home",
				name: 'home',
				component: () => import('@/views/system/home/index.vue'),
				meta: {
					title: "首页",
					requireAuth: true,
					hidden:false,
					icon:'House'
				}
			},
		],
	},
]

//404路由
export const NotFound = [
	{
		path: "/:pathMatch(.*)*",
        name: 'notFound',
		component: () => import('@/views/system/error/404.vue'),
		meta: {
			title: "404 notFound",
            requireAuth: false,
            hidden:true,
		},
	},
]

//静态路由
export const staticRoutes = [
	{
		path: "/login",
        name: 'login',
		component: () => import('@/views/system/login/index.vue'),
		meta: {
			title: "登录",
            requireAuth: false,
            hidden:false,
		}
	},
	{
		path: "/register",
        name: 'register',
		component: () => import('@/views/system/login/register.vue'),
		meta: {
			title: "注册",
            requireAuth: false,
            hidden:false,
		}
	},
]