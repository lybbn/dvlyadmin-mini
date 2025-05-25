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
		<el-dropdown class="user panel-item" trigger="click" @command="handleInfo">
			<div class="user-avatar">
				<label>{{ "更多" }}</label>
				<el-icon class="el-icon--right"><ArrowDown /></el-icon>
			</div>
			<template #dropdown>
				<el-dropdown-menu>
					<!-- <el-dropdown-item command="clearCache">清除缓存</el-dropdown-item> -->
					<el-dropdown-item command="updateLogs"><el-icon><Share /></el-icon>更新日志</el-dropdown-item>
					<el-dropdown-item command="checkUpdate"><el-icon><StarFilled /></el-icon>检查更新</el-dropdown-item>
					<el-dropdown-item command="fixPanel"><el-icon><EditPen /></el-icon>修复面板</el-dropdown-item>
                	<el-dropdown-item @click="handleBuJUClick"><el-icon><Tools /></el-icon>布局设置</el-dropdown-item>
					<el-dropdown-item divided command="outLogin"><el-icon><CircleCloseFilled /></el-icon>退出登录</el-dropdown-item>
				</el-dropdown-menu>
			</template>
		</el-dropdown>
	</div>

	<el-dialog v-model="searchVisible" :width="700"  title="搜索" center destroy-on-close>
		<search @success="searchVisible=false"></search>
	</el-dialog>
	<el-dialog v-model="shutdownVisible" :width="300"  title="重启服务器或面板" destroy-on-close>
		<shutdown></shutdown>
	</el-dialog>
	<shutdown v-if="onlyRestartVisiable" ref="onlyShudownRef"></shutdown>
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
	import {fullScreen,autoStorage} from "@/utils/util"
	import {useSiteThemeStore} from "@/store/siteTheme";
	import {useUserState} from "@/store/userState";
	import { useRouter } from 'vue-router';
	
	const router = useRouter()
	const siteThemeStore = useSiteThemeStore()
	const userState = useUserState()

    let settingDialog = ref(false)

	let searchVisible = ref(false)
	let shutdownVisible = ref(false)
	let msg = ref(false)
	let msgList = ref([])
	let onlyRestartVisiable = ref(false)
	let onlyShudownRef = ref(null)

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
		else if(command == "updateLogs"){
			window.open("https://lybbn.lybbn.cn/doc/lybbn/update.html")
		}
		else if(command == "checkUpdate"){
			checkUpdateInfo()
		}
		else if(command == "fixPanel"){
			fixMessageBox()
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

	function checkUpdateInfo(){
        userState.loadingInfo.isLoading = true
        userState.loadingInfo.content = "获取中..."
        Api.sysGetSysUpdate().then(res=>{
            userState.loadingInfo.isLoading = false
            userState.loadingInfo.content = ""
            if(res.code ==2000) {
                let tempdata = res.data
				updateMessageBox(tempdata)
            }else{
                ElMessage.warning(res.msg)
            }
        })
    }

	function updateMessageBox(tempdata){
		if(!tempdata.can_update){
			ElMessage.success("当前已是最新版本")
		}else{
			let htmlcont = `<div style="font-size:15px;">发现新版本<span style="color:red;">【${tempdata.n_ver}】</span>,是否确定更新？<br/><a target="_blank" href="https://lybbn.lybbn.cn/doc/lybbn/update.html" style="color:#008040">查看更新日志</a><div>`
			ElMessageBox({
				title: '更新提示',
				message: htmlcont,
				dangerouslyUseHTMLString: true, // 允许 HTML 字符串
				showCancelButton: true,
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning',
				icon:'Download',
				customClass:"lybbnMessageBoxClass",
				beforeClose: (action, instance, done) => {
					if (action === 'confirm') {
						UpdateSysPack("update")
					} else if (action === 'cancel') {
						// console.log('取消');
					}
					done(); // 关闭 MessageBox 实例
				}
			}).then(action => {
			}).catch(() => {
			})
		}
	}

	function UpdateSysPack(type="update"){
        userState.loadingInfo.isLoading = true
        userState.loadingInfo.content = "更新中..."
        Api.sysStartSysUpdate({action:type}).then(res=>{
            userState.loadingInfo.isLoading = false
            userState.loadingInfo.content = ""
            if(res.code ==2000) {
                onlyRestartVisiable.value = true
				nextTick(()=>{
					onlyShudownRef.value.onlyRestartPanel()
				})
            }else{
                ElMessage.warning(res.msg)
            }
        })
    }

	function fixMessageBox(){
		let htmlcont = `<div style="font-size:15px;">该操作能修复使用中遇到的异常问题，是否确定执行修复面板操作？<div>`
		ElMessageBox({
			title: '修复面板提示',
			message: htmlcont,
			dangerouslyUseHTMLString: true, // 允许 HTML 字符串
			showCancelButton: true,
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
			icon:'EditPen',
			customClass:"lybbnMessageBoxClass",
			beforeClose: (action, instance, done) => {
				if (action === 'confirm') {
					fixSysPack("fix")
				} else if (action === 'cancel') {
					// console.log('取消');
				}
				done(); // 关闭 MessageBox 实例
			}
		}).then(action => {
		}).catch(() => {
		})
	}

	function fixSysPack(type="fix"){
        userState.loadingInfo.isLoading = true
        userState.loadingInfo.content = "修复中..."
        Api.sysStartSysUpdate({action:type}).then(res=>{
            userState.loadingInfo.isLoading = false
            userState.loadingInfo.content = ""
            if(res.code ==2000) {
                onlyRestartVisiable.value = true
				nextTick(()=>{
					onlyShudownRef.value.onlyRestartPanel()
				})
            }else{
                ElMessage.warning(res.msg)
            }
        })
    }

	function handleBuJUClick(){
		settingDialog.value=true
	}

	onMounted(()=>{
	})

</script>

<style scoped>
	.user-bar {display: flex;align-items: center;height: 100%;}
	.user-bar .panel-item {padding: 0 10px;cursor: pointer;height: 100%;display: flex;align-items: center;}
	.user-bar .panel-item i {font-size: 16px;}
	.user-bar .panel-item:hover {background: rgba(0, 0, 0, 0.1);}
	.user-bar .user-avatar {height:49px;display: flex;align-items: center;}
	.user-bar .user-avatar label {display: inline-block;margin-left:5px;font-size: 12px;cursor:pointer;}

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
</style>
