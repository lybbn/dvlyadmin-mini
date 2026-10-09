<template>
	<div class="lysearch">
		<el-input ref="refInput" v-model="searchContent" placeholder="搜索" size="large" clearable prefix-icon="search" :trigger-on-focus="false" @input="inputChange"/>
		<div class="lysearch-history" v-if="history.length>0">
			<el-tag closable effect="plain" type="info" v-for="(item, index) in history" :key="item" @click="historyClick(item)" @close="historyClose(index)">{{item}}</el-tag>
		</div>
		<div class="lysearch-result">
			<div class="lysearch-no-result" v-if="result.length<=0">暂无搜索结果</div>
			<ul v-else>
				<el-scrollbar max-height="366px">
					<li v-for="item in result" :key="item.path" @click="to(item)">
						<el-icon><component :is="item.icon || 'menu'" /></el-icon>
						<span class="title">{{ item.breadcrumb }}</span>
					</li>
				</el-scrollbar>
			</ul>
		</div>
	</div>
</template>

<script setup>
	import {ref, onMounted } from 'vue'
	import { useRouter,useRoute } from 'vue-router'
	import { autoStorage } from '@/utils/util'

	const emits = defineEmits(['success'])

	const router = useRouter()

	let refInput = ref(null)
	let searchContent = ref("")
	let menu = ref([])
	let result = ref([])
	let history = ref([])

	function inputChange(value){
		if(value){
			result.value = menuFilter(value)
		}else{
			result.value = []
		}
	}
	function filterMenu(map){
		map.forEach(item => {
			if(!item.meta || item.meta.hidden || item.meta.type=="button"){
				return false
			}
			if(item.meta.type=='iframe'){
				item.path = `/i/${item.name}`
			}
			if(item.children&&item.children.length > 0&&!item.component){
				filterMenu(item.children)
			}else{
				menu.value.push(item)
			}
		})
	}
	function menuFilter(queryString){
		var res = []
		//过滤菜单树
		var filterMenu = menu.value.filter((item) => {
			if((item.meta.title).toLowerCase().indexOf(queryString.toLowerCase()) >= 0){
				return true
			}
			if(((item.name) || '').toLowerCase().indexOf(queryString.toLowerCase()) >= 0){
				return true
			}
		})
		//匹配系统路由（注意：原 var router = router.getRoutes() 中 var 提升遮蔽了外层 useRouter 实例，
		//右侧 router 为 undefined 必抛 TypeError，导致搜索永远"暂无搜索结果"，改名 allRoutes 修复）
		var allRoutes = router.getRoutes()
		var filterRouter= filterMenu.map((m) => {
			if(m.meta.type == "link"){
				return allRoutes.find(r => r.path == '/'+m.path)
			}else{
				return allRoutes.find(r => r.path == m.path)
			}
		}).filter(Boolean)
		//重组对象
		filterRouter.forEach(item => {
			res.push({
				name: item.name,
				type: item.meta.type,
				path: item.meta.type=="link"?item.path.slice(1):item.path,
				icon: item.meta.icon,
				title: item.meta.title,
				//breadcrumb 元素是 {title, path} 普通对象（见 autoBreadcrumb.js），不是路由记录，取 v.title
				breadcrumb: item.meta.breadcrumb ? item.meta.breadcrumb.map(v => v.title).join(' - ') : item.meta.title
			})
		})
		return res
	}
	function to(item){
		//script setup 中 this 为 undefined（原 this.input 必抛 TypeError 导致点击结果无法跳转），改用 searchContent
		if(searchContent.value && !history.value.includes(searchContent.value)){
			history.value.push(searchContent.value)
			autoStorage.set("SEARCH_HISTORY", history.value)
		}
		if(item.type=="link"){
			setTimeout(()=>{
				let a = document.createElement("a")
					a.style = "display: none"
					a.target = "_blank"
					a.href = item.path
					document.body.appendChild(a)
					a.click()
					document.body.removeChild(a)
			}, 10);
		}else{
			router.push({path: item.path})
		}
		emits('success', true)
	}
	function historyClick(text){
		searchContent.value = text
		inputChange(text)
	}
	function historyClose(index){
		history.value.splice(index, 1);
		if(history.value.length <= 0){
			autoStorage.remove("SEARCH_HISTORY")
		}else{
			autoStorage.set("SEARCH_HISTORY", history.value)
		}
	}

	onMounted(()=>{
		var searchHistory = autoStorage.get("SEARCH_HISTORY") || []
		history.value = searchHistory
		var menuTree = router.getRoutes()
		filterMenu(menuTree)
		refInput.value.focus()
	})
</script>

<style scoped>
	.lysearch {}
	.lysearch-no-result {text-align: center;margin: 40px 0;color: var(--ly-text-2, #999);}
	.lysearch-history {margin-top: 10px;}
	/* 历史标签：v4 玻璃胶囊语言（半透明底+细描边+胶囊圆角），hover 淡蓝主色 */
	.lysearch-history .el-tag {cursor: pointer;border-radius: 999px;background: var(--ly-glass-bg-soft, rgba(255,255,255,0.45));border-color: var(--ly-line-soft, rgba(27,35,64,0.08));color: var(--ly-text-2, #606266);transition: all .15s ease;}
	.lysearch-history .el-tag:hover {color: var(--el-color-primary);border-color: var(--el-color-primary);background: rgba(58, 123, 255, 0.06);}
	/* 结果项对齐 v4 下拉选项语言：胶囊 hover 淡蓝底主色字，无描边块 */
	.lysearch-result {margin-top: 15px;}
	.lysearch-result li {height:44px;padding:0 14px;background: transparent;border: none;list-style:none;border-radius: 8px;margin-bottom: 2px;font-size: 14px;display: flex;align-items: center;cursor: pointer;color: var(--ly-text-1, #303133);transition: background-color .15s ease,color .15s ease;}
	.lysearch-result li  i {font-size: 18px;margin-right: 12px;color: var(--ly-text-2, #909399);}
	.lysearch-result li:hover {background: rgba(58, 123, 255, 0.08);color: var(--el-color-primary);}
	.lysearch-result li:hover i {color: var(--el-color-primary);}
</style>
