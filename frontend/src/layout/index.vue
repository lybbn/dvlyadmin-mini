<template>
	<header class="lybbn-panel-header">
		<div class="lybbn-panel-header-left">
			<div class="logo-bar">
				<img class="logo" src="@/assets/lybbn/imgs/logo.png">
				<span>{{ config.APP_NAME}}</span>
			</div>
		</div>
		<div class="lybbn-panel-header-right">
			<userbar></userbar>
		</div>
	</header>
	<section class="lybbn-panel-wrapper">
		<div v-if="!ismobile" :class="isMenuCollapse ? 'lybbn-panel-side isCollapse' : 'lybbn-panel-side'">
			<div class="lybbn-panel-side-scroll">
				<el-scrollbar>
					<el-menu class="rymenu" :default-active="active" router :collapse="isMenuCollapse" :unique-opened="true" :collapse-transition="false">
						<NavMenu :navMenus="menu" @contextmenuClick="openContextMenuItem"></NavMenu>
					</el-menu>
				</el-scrollbar>
			</div>
			<div class="lybbn-panel-side-bottom" @click="setMenuCollapsed">
				<el-icon>
					<expand v-if="isMenuCollapse" />
					<fold v-else />
				</el-icon>
			</div>
		</div>
		<SideMobile v-if="ismobile"></SideMobile>
		<div class="lybbn-panel-body el-container">
			<TabsView v-if="ismultitabs" />
			<div class="lybbn-panel-main" id="lybbn-panel-main">
				<router-view v-slot="{ Component, route }">
					<keep-alive :include="KeepAliveStore.keepAliveRoute">
						<component :is="Component" :key="route.path" v-if="KeepAliveStore.routeShow" />
					</keep-alive>
				</router-view>
				<iframeView></iframeView>
			</div>
		</div>
	</section>
	<transition name="el-zoom-in-top">
		<ul v-show="contextMenuVisible" :style="{ left: left + 'px', top: top + 'px' }" class="contextmenu"
			id="lyleftMenuContext" ref="lyleftMenuContext">
			<li @click="openNewTabs"><el-icon>
					<CopyDocument />
				</el-icon><span class="contextmenu-text">新标签打开</span></li>
			<li @click="handleRefreshPage"><el-icon>
					<Refresh />
				</el-icon><span class="contextmenu-text">刷新本页</span></li>
			<li @click="closeContextMenu"><el-icon>
					<Close />
				</el-icon><span class="contextmenu-text">取消操作</span></li>
		</ul>
	</transition>
	<div class="main-maximize-exit" @click="exitMaximize">
		<el-icon><Close /></el-icon>
	</div>
</template>

<script setup>

import { ref, onMounted, watch, computed, nextTick, onBeforeUnmount } from 'vue'

import TabsView from './components/TabsView.vue'
import SideMobile from './components/sideMobile.vue';
import NavMenu from './components/NavMenu.vue';
import userbar from './components/userbar.vue';
import iframeView from './components/iframeView.vue';
import { useSiteThemeStore } from "@/store/siteTheme";
import { useKeepAliveStore } from "@/store/keepAlive";
import { useUserState } from "@/store/userState";
import { useRoutesList } from "@/store/routesList";
import { useRouter, useRoute } from 'vue-router'
import config from '@/config'
import Api from "@/api/api";
import { isEmpty } from '@/utils/util';
import { ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()

const siteThemeStore = useSiteThemeStore()
const KeepAliveStore = useKeepAliveStore()
const storesRoutesList = useRoutesList()
const userState = useUserState()

// let menu = ref([])
let active = ref("")

let contextMenuVisible = ref(false)
let left = ref(0)
let top = ref(0)

let ismobile = computed(() => {
	return siteThemeStore.ismobile
})

let ismultitabs = computed(() => {
	return siteThemeStore.ismultitabs
})

let isMenuCollapse = computed(() => {
	return siteThemeStore.isMenuCollapse
})

function setIsmultitabs() {
	siteThemeStore.setIsmultitabs(!ismultitabs.value)
}

function setMenuCollapsed() {
	siteThemeStore.setMenuCollapsed(!isMenuCollapse.value)
	setTimeout(() => {
		window.dispatchEvent(new Event('resize'));
	}, 1000);
}

//退出最大化
function exitMaximize() {
	document.getElementById('app').classList.remove('main-maximize')
}

//转换外部链接的路由
function filterUrl(map) {
	var newMap = []
	map && map.forEach(item => {
		item.meta = item.meta ? item.meta : {};
		//处理隐藏
		if (item.meta.hidden || item.meta.type == "button") {
			return false
		}
		//处理http
		if (item.meta.type == 'iframe') {
			item.path = `/i/${item.name}`;
		}
		//递归循环
		if (item.children && item.children.length > 0) {
			item.children = filterUrl(item.children)
		}
		newMap.push(item)
	})
	return newMap;
}

//路由监听高亮
function showThis() {
	nextTick(() => {
		//新增嵌套路由根据activeMenu决定高亮菜单
		if(route.meta && route.meta.activeMenu){
			active.value = route.meta.activeMenu;
		}else{
			active.value = route.path;
		}
	})
}

function onLayoutResize() {
	nextTick(() => {
		siteThemeStore.setIsmobile(document.body.clientWidth < 992)
	})
}

function closeContextMenu() {
	contextMenuVisible.value = false
}

// 点击其他地方时关闭右键菜单
let lyleftMenuContext = ref(null)
function handleClickOutside(event) {
	if (lyleftMenuContext.value && !lyleftMenuContext.value.contains(event.target)) {
		closeContextMenu();
	}
}

let targetPath = ref("")

function openNewTabs() {
	if (!!targetPath.value) {
		let baseurl = window.location.origin
		window.open(baseurl + "/#" + targetPath.value, '_blank');
	}
	closeContextMenu()
}

function handleRefreshPage(){
	if (!!targetPath.value) {
		if(route.path == targetPath.value){
			window.location.reload()
		}else{
			router.push({path: targetPath.value})
		}
	}
	closeContextMenu()
}

//暂时废弃
function openContextMenu(e) {
	e.preventDefault();// 隐藏默认的浏览器右键菜单
	e.stopPropagation(); // 阻止事件冒泡
	var obj = e.target;
	if (obj.role == 'menuitem') {
		targetPath.value = obj.querySelector("#rightContextMenuItem").innerText
		contextMenuVisible.value = true
		left.value = e.clientX + 1;
		top.value = e.clientY + 1;
		//右键菜单边缘化位置处理（防止在最边缘右键右健菜单消失部分）
		nextTick(() => {
			let ct = document.getElementById("lyleftMenuContext");
			if (document.body.offsetWidth - e.clientX < ct.offsetWidth) {
				left.value = document.body.offsetWidth - ct.offsetWidth - 1;
				top.value = e.clientY + 1;
			}
		})
	} else {
		targetPath.value = ""
	}
}

function openContextMenuItem(e,path){
	if (!path) return
	e.preventDefault();// 隐藏默认的浏览器右键菜单
	e.stopPropagation(); // 阻止事件冒泡
	targetPath.value = path
	contextMenuVisible.value = true
	left.value = e.clientX + 1;
	top.value = e.clientY + 1;
	//右键菜单边缘化位置处理（防止在最边缘右键右健菜单消失部分）
	nextTick(() => {
		let ct = document.getElementById("lyleftMenuContext");
		if (document.body.offsetWidth - e.clientX < ct.offsetWidth) {
			left.value = document.body.offsetWidth - ct.offsetWidth - 1;
			top.value = e.clientY + 1;
		}
	})
}

let dataInfo = ref({
	c_ver:userState.sysConfig.sysVersion,
	can_update:false,
	n_ver:"",
})

function filterUrl2(map) {
	var newMap = []
	map && map.forEach(item => {
		item.meta = item.meta ? item.meta : {};
		//处理隐藏
		if (item.meta?.hidden) {
			return false
		}
		//递归循环
		if (item.children && item.children.length > 0) {
			item.children = filterUrl2(item.children)
			// 如果处理后children为空，则移除children属性
            if (item.children.length === 0) {
                delete item.children
            }
		}
		newMap.push(item)
	})
	return newMap;
}

let menu = computed(()=> {
    return filterUrl2(storesRoutesList.routesList)
});

onMounted(() => {
	onLayoutResize();
	window.addEventListener('resize', onLayoutResize);
	// menu.value = filterUrl(storesRoutesList.routesList);
	showThis()
	router.afterEach(showThis);
	// 监听点击事件
    document.addEventListener('click', handleClickOutside);
})

onBeforeUnmount(() => {
	window.removeEventListener('resize', onLayoutResize)
	// 组件销毁时移除事件监听
    document.removeEventListener('click', handleClickOutside);
})

</script>
<style scoped>
.contextmenu {
	width: 130px;
	margin: 0;
	border: 1px solid #ccc;
	background: var(--el-menu-bg-color);
	z-index: 3000;
	position: absolute;
	list-style-type: none;
	padding: 5px 0;
	border-radius: 4px;
	font-size: 14px;
}

.contextmenu li {
	margin: 0;
	padding: 9px 16px;
	display: flex;
	align-items: center;
}

.contextmenu li:hover {
	background: var(--el-color-primary-light-6);
	cursor: pointer;
	color: var(--el-color-primary);
}

.contextmenu-text {
	margin-left: 5px;
}

.lybbn-panel-side-scroll:deep(.el-menu-item).is-active{
	background-color: var(--el-color-primary-light-8) !important;
}
.lybbn-panel-side-scroll:deep(.el-menu-item.is-active)::before{
	position: absolute;
    border-radius: 4px;
    left: 12px;
    width: 4px;
    height: 14px;
    content: "";
	background-color: var(--el-color-primary-light-3) !important;
}
.lybbn-panel-side-scroll:deep(.el-menu-item:hover){
	background-color: var(--el-color-primary-light-9) !important;
}
</style>
