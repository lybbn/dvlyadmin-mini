<template>
	<div class="lysearch">
		<el-input ref="refInput" v-model="searchContent" placeholder="搜索" size="large" clearable prefix-icon="search" :trigger-on-focus="false" @input="inputChange"/>
		<div class="lysearch-history" v-if="history.length>0">
			<el-tag closable effect="dark" type="info" v-for="(item, index) in history" :key="item" @click="historyClick(item)" @close="historyClose(index)">{{item}}</el-tag>
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
			if(item.meta.hidden || item.meta.type=="button"){
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
			if((item.name).toLowerCase().indexOf(queryString.toLowerCase()) >= 0){
				return true
			}
		})
		//匹配系统路由
		var router = router.getRoutes()
		var filterRouter= filterMenu.map((m) => {
			if(m.meta.type == "link"){
				return router.find(r => r.path == '/'+m.path)
			}else{
				return router.find(r => r.path == m.path)
			}
		})
		//重组对象
		filterRouter.forEach(item => {
			res.push({
				name: item.name,
				type: item.meta.type,
				path: item.meta.type=="link"?item.path.slice(1):item.path,
				icon: item.meta.icon,
				title: item.meta.title,
				breadcrumb: item.meta.breadcrumb.map(v => v.meta.title).join(' - ')
			})
		})
		return res
	}
	function to(item){
		if(!history.value.includes(this.input)){
			history.value.push(this.input)
			autoStorage.set("SEARCH_HISTORY", this.history)
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
			autoStorage.set("SEARCH_HISTORY", this.history)
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
	.lysearch-no-result {text-align: center;margin: 40px 0;color: #999;}
	.lysearch-history {margin-top: 10px;}
	.lysearch-history .el-tag {cursor: pointer;}
	.lysearch-result {margin-top: 15px;}
	.lysearch-result li {height:56px;padding:0 15px;background: var(--el-bg-color-overlay);border: 1px solid var(--el-border-color-light);list-style:none;border-radius: 4px;margin-bottom: 5px;font-size: 14px;display: flex;align-items: center;cursor: pointer;}
	.lysearch-result li  i {font-size: 20px;margin-right: 15px;}
	.lysearch-result li:hover {background: var(--el-color-primary);color: #fff;border-color: var(--el-color-primary);}
</style>
