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
		children: [],
	},
]

//自定义layout的children的静态路由，优先级高于后台api的动态路由
export const CustomStaticRoutes = [
	{
		path: "/home",
		name: 'home',
		component: () => import('@/views/system/home/index.vue'),
		meta: {
			title: "首页",
			requireAuth: true,
			hidden:false,
			icon:'House',
			affix: true//固定
		}
	},
	{
		path: "/PersonalCenter",
		name: 'PersonalCenter',
		component: () => import('@/views/system/usercenter/pcenter.vue'),
		meta: {
			title: "个人中心",
			requireAuth: true,
			hidden:false,
			icon:'User',
		}
	},
	{
		path: "/menuManage",
		name: 'menuManage',
		component: () => import('@/views/system/menu/index.vue'),
		meta: {
			title: "菜单管理",
			requireAuth: true,
			hidden:false,
			icon:'Collection',
		}
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

//重定向路由
export const RedirectRoute = {
	path: '/redirect',
	component: () => import('@/layout/index.vue'),
	name: 'RedirectTo',
	meta: {
		title: "Redirect",
		requireAuth: true,
		hidden: false,
	},
	children: [
		{
			path: '/redirect/:path(.*)',
			name: "Redirect",
			component: () => import('@/views/system/redirect/index.vue'),
			meta: {
				title: "Redirect",
				requireAuth: true,
				hidden: false,
			},
		},
	],
};
