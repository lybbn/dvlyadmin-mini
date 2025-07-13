<template>
	<div class="user-bar">
		<!-- <div class="panel-item" @click="searchFunc">
			<el-icon><Search /></el-icon>
		</div> -->
		<el-dropdown trigger="click" @command="changeLanguage" style="height: 100%;">
			<div class="changlang panel-item">
				<svg viewBox="0 0 24 24" width="1.2em" height="1.2em"><path fill="currentColor" d="m18.5 10l4.4 11h-2.155l-1.201-3h-4.09l-1.199 3h-2.154L16.5 10h2zM10 2v2h6v2h-1.968a18.222 18.222 0 0 1-3.62 6.301a14.864 14.864 0 0 0 2.336 1.707l-.751 1.878A17.015 17.015 0 0 1 9 13.725a16.676 16.676 0 0 1-6.201 3.548l-.536-1.929a14.7 14.7 0 0 0 5.327-3.042A18.078 18.078 0 0 1 4.767 8h2.24A16.032 16.032 0 0 0 9 10.877a16.165 16.165 0 0 0 2.91-4.876L2 6V4h6V2h2zm7.5 10.885L16.253 16h2.492L17.5 12.885z"></path></svg>
			</div>
			<template #dropdown>
				<el-dropdown-menu>
					<el-dropdown-item command="zh-cn" :disabled="currentLang === 'zh-cn'">
					简体中文
					</el-dropdown-item>
					<el-dropdown-item command="en" :disabled="currentLang === 'en'">
					English
					</el-dropdown-item>
				</el-dropdown-menu>
			</template>
		</el-dropdown>
		<div class="screen panel-item" @click="screenFunc">
			<el-icon><FullScreen /></el-icon>
		</div>
		<div class="msg panel-item" @click="showMsg">
			<el-badge :hidden="lywebsocket.msgInfo.msgNumber==0" :value="lywebsocket.msgInfo.msgNumber" class="badge" type="danger">
				<el-tooltip  effect="dark" content="消息列表" placement="bottom">
					<el-icon><ChatDotRound /></el-icon>
				</el-tooltip>
			</el-badge>
			<el-drawer title="新消息" v-model="msg" :size="600" append-to-body destroy-on-close>
				<el-container>
					<el-main class="nopadding" v-loading="isLoadingMsg">
						<el-scrollbar>
							<ul class="msg-list">
								<li v-for="item in msgList" v-bind:key="item.id">
									<a :href="item.link" target="_blank">
										<!-- <div class="msg-list__icon">
											<el-badge is-dot type="danger">
												<el-avatar :size="40" :src="item.avatar"></el-avatar>
											</el-badge>
										</div> -->
										<div class="msg-list__main">
											<h2>{{item.notification.title}}</h2>
											<p v-html="item.notification.content"></p>
										</div>
										<div class="msg-list__time">
											<p>{{item.notification.create_datetime}}</p>
										</div>
									</a>
								</li>
								<el-empty v-if="msgList.length==0" description="暂无新消息" :image-size="100"></el-empty>
							</ul>
						</el-scrollbar>
					</el-main>
					<el-footer>
						<el-button @click="markRead">全部设为已读</el-button>
					</el-footer>
				</el-container>
			</el-drawer>
		</div>
		<div class="theme panel-item" @click="changeDarkTheme">
			<el-icon v-if="siteThemeStore.siteTheme == 'dark'"><Sunny /></el-icon>
			<el-icon v-else><Moon /></el-icon>
		</div>
		<el-dropdown class="user-profile" @command="handleInfo">
			<div class="profile-content">
				<el-avatar :size="30" :src="userState.userInfo.avatar || defaultAvatar" class="profile-avatar"/>
				<div class="profile-info">
					<div class="profile-name">{{ userState.userInfo.name || '更多' }}</div>
				</div>
				<el-icon class="profile-arrow"><ArrowDown /></el-icon>
			</div>
			<template #dropdown>
				<el-dropdown-menu class="profile-menu">
					<!-- <el-dropdown-item command="clearCache">清除缓存</el-dropdown-item> -->
					<el-dropdown-item command="personCenter">
						<el-icon><User /></el-icon>个人中心
					</el-dropdown-item>
					<el-dropdown-item  @click="handleBuJUClick">
						<el-icon><Operation /></el-icon>布局设置
					</el-dropdown-item>
					<el-dropdown-item divided command="outLogin">
						<el-icon><SwitchButton /></el-icon>退出登录
					</el-dropdown-item>
				</el-dropdown-menu>
			</template>
		</el-dropdown>
	</div>

	<el-dialog v-model="searchVisible" :width="700"  title="搜索" center destroy-on-close>
		<search @success="searchVisible=false"></search>
	</el-dialog>
	<el-drawer title="布局设置" v-model="settingDialog" :size="400" append-to-body destroy-on-close>
		<lysettings></lysettings>
	</el-drawer>
</template>

<script setup>
	import {ref, onMounted, nextTick } from 'vue'
	import Api from "@/api/api";
	import { ElMessage,ElMessageBox } from 'element-plus'
	import search from './search.vue'
	import lysettings from './lysettings.vue';
	import defaultAvatar from '@/assets/lybbn/imgs/avatar.jpg'
	import {fullScreen,autoStorage} from "@/utils/util"
	import {useSiteThemeStore} from "@/store/siteTheme";
	import {useUserState} from "@/store/userState";
	import { useRouter } from 'vue-router';
	import { useLywebsocket } from "@/store/websocket";
	
	const lywebsocket = useLywebsocket()
	const router = useRouter()
	const siteThemeStore = useSiteThemeStore()
	const userState = useUserState()

    let settingDialog = ref(false)

	let searchVisible = ref(false)
	let msg = ref(false)
	let msgList = ref([])
	let onlyRestartVisiable = ref(false)
	let isLoadingMsg = ref(false)

	let currentLang = ref(siteThemeStore.language || 'zh-cn')

	//全屏
	function screenFunc(){
		var element = document.documentElement;
		fullScreen(element)
	}
	//显示短消息
	function showMsg(){
		msg.value = true
		isLoadingMsg.value = true
		Api.getOwnMessage({is_read:false,page:1,limit:999}).then(res=>{
			isLoadingMsg.value = false
			if(res.code === 2000){
				msgList.value = res.data.data
			}else{
				ElMessage.warning(res.msg)
			}
		})
		
	}
	//标记已读
	function markRead(){
		if(msgList.value.length<1){
			return
		}
		Api.readOwnMessage({type:"ALL"}).then(res=>{
			if(res.code === 2000){
				ElMessage.success(res.msg)
				msgList.value = []
				lywebsocket.setUnread(0)
			}else{
				ElMessage.warning(res.msg)
			}
		})
	}
	//搜索
	function searchFunc(){
		searchVisible.value = true
	}

	function changeDarkTheme(){
		if(siteThemeStore.siteTheme=='light'){
			siteThemeStore.setSiteTheme('dark')
		}else{
			siteThemeStore.setSiteTheme('light')
			const menuHeaderColor01 = siteThemeStore.menuHeaderColor01
    		const menuHeaderColor02 = siteThemeStore.menuHeaderColor02
			siteThemeStore.setMenuHeaderColor01(menuHeaderColor01)
            siteThemeStore.setMenuHeaderColor02(menuHeaderColor02)
		}
	}

	function handleInfo(command) {
		if(command == "clearCache"){
		}
		else if(command == "personCenter"){
			router.push({name:"PersonalCenter"})
		}
		else if(command == "outLogin"){
			ElMessageBox.confirm('退出登录, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				autoStorage.clearAll()
				router.push('/login')
				ElMessage.success('已退出登录!')
			})
			.catch(() => {
			})
		}
	}

	function handleBuJUClick(){
		settingDialog.value=true
	}

	function changeLanguage(langstr){
		currentLang.value = langstr
		siteThemeStore.setLanguage(langstr)
	}

	onMounted(()=>{
		userState.getSystemUserInfo()
	})

</script>

<style lang="scss" scoped>
	.user-bar {display: flex;align-items: center;height: 100%;}
	.user-bar .panel-item {padding: 0 10px;cursor: pointer;height: 100%;display: flex;align-items: center;}
	.user-bar .panel-item i {font-size: 16px;}
	.user-bar .panel-item:hover {background: rgba(0, 0, 0, 0.1);}

	.msg-list li {border-top:1px solid #eee;}
	.msg-list li a {display: flex;padding:20px;}
	.msg-list li a:hover {background: #ecf5ff;}
	.msg-list__icon {width: 40px;margin-right: 15px;}
	.msg-list__main {flex: 1;}
	.msg-list__main h2 {font-size: 15px;font-weight: normal;color: #333;}
	.msg-list__main p {font-size: 12px;color: #999;line-height: 1.8;margin-top: 5px;}
	.msg-list__time {width: 120px;text-align: right;color: #999;}

	.dark .msg-list__main h2 {color: #d0d0d0;}
	.dark .msg-list li {border-top:1px solid #363636;}
	.dark .msg-list li a:hover {background: #383838;}

	.user-profile {
		margin-left: auto;
		cursor: pointer;
		.profile-content {
			display: flex;
			align-items: center;
			padding: 4px 8px;
			border-radius: 18px;
			transition: all 0.3s;
		
			&:hover {
				background:rgba(255, 255, 255, 0.1) !important;
				// background: var(--el-color-primary-light-9);
			}
			
			.profile-avatar {
				flex-shrink: 0;
			}
			
			.profile-info {
				margin: 0 12px;
				
				.profile-name {
					font-size: 14px;
					font-weight: 500;
					color: #fff;
					line-height: 1.2;
				}
			}
			
			.profile-arrow {
				font-size: 14px;
				color: #fff;
				// color: var(--el-text-color-secondary);
			}
		}
	}
	.changlang{
		color:var(--el-text-color-disabled);
	}
</style>
