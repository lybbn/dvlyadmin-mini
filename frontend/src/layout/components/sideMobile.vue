<template>
	<div ref="mobileDraggableButton" class="mobile-nav-button" @click="showMobileNav($event)" v-drag><el-icon><Menu /></el-icon></div>

	<el-drawer ref="mobileNavMenuBox" title="移动端菜单" :size="200" v-model="nav" direction="ltr" :with-header="false" destroy-on-close>
		<el-container class="mobile-nav">
			<el-header class="mobileheader">
				<div class="logo-bar"><ly-img class="logo" :src="userState.sysConfig.logo" /></div>
				<span class="headertitle">{{ userState.sysConfig.systitle }}</span>
			</el-header>
			<el-main>
				<el-scrollbar class="lylybbnmobilenavside">
					<el-menu :default-active="route.meta.active || route.fullPath" @select="select" router :background-color="siteThemeStore.siteTheme == 'dark'?'#141414':'#272E39'" text-color="#fff" active-text-color="var(--el-color-primary)">
						<NavMenu :navMenus="menu"></NavMenu>
					</el-menu>
				</el-scrollbar>
			</el-main>
		</el-container>
	</el-drawer>

</template>

<script setup>

	import {ref, onMounted,nextTick} from 'vue'
	import NavMenu from './NavMenu.vue';
	import {useRoutesList} from "@/store/routesList";
	import { useRouter,useRoute } from 'vue-router'
	import {useSiteThemeStore} from "@/store/siteTheme";
	import config from '@/config'
	import {useUserState} from "@/store/userState";

    const userState = useUserState()

	const siteThemeStore = useSiteThemeStore()

	const route = useRoute()

	const storesRoutesList = useRoutesList()

	let nav = ref(false)
	let menu = ref([])
	let mobileDraggableButton = ref(null)

	//转换外部链接的路由
	function filterUrl(map){
		var newMap = []
		map && map.forEach(item => {
			item.meta = item.meta?item.meta:{};
			if(item.meta.hidden || item.meta.type=="button"){
				return false
			}
			if(item.meta.type=='iframe'){
				item.path = `/i/${item.name}`;
			}
			if(item.children&&item.children.length > 0){
				item.children = filterUrl(item.children);
			}
			newMap.push(item)
		})
		return newMap;
	}

	function showMobileNav(e){
		var isdrag = e.currentTarget.getAttribute('drag-flag')
		if (isdrag == 'true') {
			return false;
		}else{
			nav.value = true;
		}

	}
	let mobileNavMenuBox = ref(null)
	function select(){
		mobileNavMenuBox.value.handleClose()
	}

	onMounted(()=>{
		menu.value = filterUrl(storesRoutesList.routesList)
	})

</script>

<style scoped>
	.mobile-nav-button {position: fixed;bottom:10px;left:10px;z-index: 10;width: 50px;height: 50px;background: var(--el-color-primary);box-shadow: 0 2px 12px 0 rgb(37, 4, 223);border-radius: 50%;display: flex;align-items: center;justify-content: center;}
	.mobile-nav-button i {color: #fff;font-size: 20px;}

	.mobile-nav {background: #272E39;}
	.mobile-nav .el-header {background: transparent;border: 0;}
	.mobile-nav .el-main {padding:0;}
	.mobile-nav .logo-bar {display: flex;align-items: center;font-weight: bold;font-size: 20px;color: #fff;}
	.mobile-nav .logo-bar img {width: 30px;height: 30px;margin-right: 10px;}
	.mobile-nav .el-submenu__title:hover {background: #fff!important;}
	.dark .mobile-nav {background: var(--el-bg-color);}
	.lylybbnmobilenavside:deep(.el-menu-item.is-active)::before{
		position: absolute;
		border-radius: 4px;
		left: 12px;
		width: 4px;
		height: 14px;
		content: "";
		background-color: var(--el-color-primary-light-3) !important;
	}
	.mobileheader{
		display: flex;
		align-items: center;
	}
	.headertitle{
		font-size: 15px;
    	font-weight: bold;
		color: #fff;
	}
</style>
