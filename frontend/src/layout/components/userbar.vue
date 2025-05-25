<template>
	<div class="user-bar">
		<!-- <div class="panel-item hidden-sm-and-down" @click="searchFunc">
			<el-icon><Search /></el-icon>
		</div> -->
		<div class="screen panel-item hidden-sm-and-down" @click="screenFunc">
			<el-icon><FullScreen /></el-icon>
		</div>
		<div class="msg panel-item" @click="showMsg" v-if="false">
			<el-badge :hidden="msgList.length==0" :value="msgList.length" class="badge" type="danger">
				<el-tooltip  effect="dark" content="消息列表" placement="bottom">
					<el-icon><ChatDotRound /></el-icon>
				</el-tooltip>
			</el-badge>
			<el-drawer title="新消息" v-model="msg" :size="400" append-to-body destroy-on-close>
				<el-container>
					<el-main class="nopadding">
						<el-scrollbar>
							<ul class="msg-list">
								<li v-for="item in msgList" v-bind:key="item.id">
									<a :href="item.link" target="_blank">
										<div class="msg-list__icon">
											<el-badge is-dot type="danger">
												<el-avatar :size="40" :src="item.avatar"></el-avatar>
											</el-badge>
										</div>
										<div class="msg-list__main">
											<h2>{{item.title}}</h2>
											<p>{{item.describe}}</p>
										</div>
										<div class="msg-list__time">
											<p>{{item.time}}</p>
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
	
	const router = useRouter()
	const siteThemeStore = useSiteThemeStore()
	const userState = useUserState()

    let settingDialog = ref(false)

	let searchVisible = ref(false)
	let msg = ref(false)
	let msgList = ref([])
	let onlyRestartVisiable = ref(false)

	//全屏
	function screenFunc(){
		var element = document.documentElement;
		fullScreen(element)
	}
	//显示短消息
	function showMsg(){
		msg.value = true
	}
	//标记已读
	function markRead(){
		msgList.value = []
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
			
		}
		else if(command == "outLogin"){
			ElMessageBox.confirm('退出登录, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				autoStorage.clear()
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
	.msg-list__time {width: 100px;text-align: right;color: #999;}

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
</style>
