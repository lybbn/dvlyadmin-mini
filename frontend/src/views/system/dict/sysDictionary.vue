<template>
	<div ref="containerRef" class="dict-container" :class="{ 'full-screen': isFullScreen }">
		<el-container class="main-container">
			<!-- 字典树面板 -->
			<el-aside :width="isMobile ? '100%' : '300px'" class="tree-panel">
				<el-container class="tree-container">
					<div class="panel-header">
						<el-input v-model="filterText" placeholder="输入关键字过滤..." clearable :suffix-icon="Search"/>
					</div>
					<el-main class="no-padding">
						<el-scrollbar>
							<el-tree
								ref="treeRef"
								node-key="id"
								class="leftTreeMenu"
								:data="dictionaryTree"
								:props="treeProps"
								:filter-node-method="filterNode"
								:highlight-current="true"
								:expand-on-click-node="false"
								@node-click="handleNodeClick"
								v-loading="treeLoading"
							>
								<template #default="{ node, data }">
									<div class="tree-node">
										<span class="node-label">{{ node.label }}</span>
										<span class="node-value">{{ data.value }}</span>
										<div class="node-actions">
											<el-button :icon="Edit" size="small" text  @click.stop="editDictionary(data)" v-auth="'Update'" type="primary"/>
											<el-button :icon="Delete" size="small" text @click.stop="deleteDictionary(node, data)" v-auth="'Delete'" type="danger" style="margin-left: 0px;"/>
										</div>
									</div>
								</template>
							</el-tree>
						</el-scrollbar>
					</el-main>
				</el-container>
			</el-aside>
			<!-- 字典项表格 -->
			<el-container
				class="content-container"
				:style="{ display: isMobile && !showTable ? 'none' : 'flex' }"
			>
				<div class="panel-header">
					<div class="action-buttons">
						<el-button type="primary" :icon="Plus" @click="addDictionary" v-auth="'Create'">
						{{ isMobile ? '' : '新增分类' }}
						</el-button>
						<el-button type="warning" :icon="Plus" @click="addDictionaryItem" :disabled="!selectedDictionary" v-auth="'Create'">
						{{ isMobile ? '' : '新增项' }}
						</el-button>
						<el-button type="danger" plain :icon="Delete" :disabled="selectedItems.length === 0" @click="batchDelete" v-auth="'Delete'">
						{{ isMobile ? '' : '删除' }}
						</el-button>
					</div>
				</div>
				
				<el-main class="no-padding">
					<el-table ref="tableRef" :data="tableData" row-key="id" @selection-change="handleSelectionChange" v-loading="tableLoading" stripe>
						<el-table-column type="selection" width="45" />
						<el-table-column type="index" width="60" align="center" label="序号" />
						<el-table-column prop="label" label="名称" min-width="150" sortable />
						<el-table-column prop="value" label="键值" min-width="150" sortable />
						<el-table-column prop="status" label="状态" width="120" align="center">
						<template #default="{ row }">
							<el-switch v-model="row.status" @change="toggleStatus(row)" :loading="row.loading"/>
						</template>
						</el-table-column>
						<el-table-column prop="sort" label="排序" width="100" sortable />
						<el-table-column prop="remark" label="备注" min-width="180" show-overflow-tooltip />
						<el-table-column label="操作" fixed="right" width="140" align="center">
						<template #default="{ row }">
							<div class="lyflexcenter">
								<el-button :icon="Edit" type="primary" text @click="editDictionaryItem(row)" v-auth="'Update'"/>
								<div v-auth="'Delete'">
									<el-popconfirm title="确认删除？" @confirm="deleteDictionaryItem(row)">
										<template #reference>
											<el-button :icon="Delete" text type="danger" />
										</template>
									</el-popconfirm>
								</div>
							</div>
						</template>
						</el-table-column>
					</el-table>
				</el-main>
			</el-container>
		</el-container>

		<!-- 字典分类弹窗 -->
		<SysDicModule ref="categoryDialog" @refreshData="fetchDictionaryTree" v-if="isDialogCategoryVisible" @closed="isDialogCategoryVisible = false"/>

		<!-- 字典项弹窗 -->
		<SysDicListModule ref="itemDialog" @refreshData="fetchDictionaryItems" v-if="isDialogItemVisible" @closed="isDialogItemVisible = false"/>
	</div>
</template>

<script setup name="sysDictionary">
	import { ref, computed, onMounted, onUnmounted, nextTick,watch } from 'vue'
	import { fullScreen } from '@/utils/util'
	import { useRoute } from 'vue-router'
	import { useWindowSize } from '@vueuse/core'
	import { Search, Edit, Delete, Plus} from '@element-plus/icons-vue'
	import SysDicModule from './components/sysDicModule.vue'
	import SysDicListModule  from './components/sysDicListModule.vue'
	import Api from '@/api/api'
	import {ElMessage,ElMessageBox} from 'element-plus'

	const route = useRoute()
	const { width: windowWidth } = useWindowSize()

	// 响应式变量
	const treeRef = ref(null)
	const tableRef = ref(null)
	const categoryDialog = ref(null)
	const itemDialog = ref(null)
	const isFullScreen = ref(false)
	const filterText = ref('')
	const treeLoading = ref(false)
	const tableLoading = ref(false)
	const dictionaryTree = ref([])
	const tableData = ref([])
	const selectedDictionary = ref(null)
	const selectedItems = ref([])
	const showTable = ref(false)
	let isDialogItemVisible = ref(false)
	let isDialogCategoryVisible = ref(false)

	// 移动端布局判断
	const isMobile = computed(() => windowWidth.value < 768)

	// 树配置
	const treeProps = {
		label: 'label',
		children: 'children'
	}

	// 监听搜索词变化
	watch(filterText, (val) => {
		treeRef.value.filter(val)
	})

	// 生命周期钩子
	onMounted(() => {
		document.addEventListener('fullscreenchange', onFullscreenChange)
		document.addEventListener('webkitfullscreenchange', onFullscreenChange)
		fetchDictionaryTree()
		if (!isMobile.value) {
			showTable.value = true
		}
	})
	onUnmounted(() => {
		document.removeEventListener('fullscreenchange', onFullscreenChange)
		document.removeEventListener('webkitfullscreenchange', onFullscreenChange)
	})

	// 方法
	const filterNode = (value, data) => {
	if (!value) return true
		const searchText = value.toLowerCase()
		return (
			data.label.toLowerCase().includes(searchText) ||
			(data.value && data.value.toString().toLowerCase().includes(searchText))
		)
	}

	// 获取字典树数据
	const fetchDictionaryTree = async () => {
		try {
			treeLoading.value = true
			const res = await Api.systemDictionary({
				parent_isnull: true,
				page: 1,
				limit: 999
			})
			
			if (res.code === 2000) {
				dictionaryTree.value = res.data.data
				// 默认选中第一个节点
				if (dictionaryTree.value.length > 0) {
					nextTick(() => {
						treeRef.value.setCurrentKey(dictionaryTree.value[0].id)
						handleNodeClick(dictionaryTree.value[0])
					})
				}
			}
		} catch (error) {
			console.error('获取字典树失败:', error)
		} finally {
			treeLoading.value = false
		}
	}

	// 获取字典项数据
	const fetchDictionaryItems = async (parentId) => {
		if (!parentId) return
		
		try {
			tableLoading.value = true
			const res = await Api.systemDictionary({
				parent: parentId,
				page: 1,
				limit: 999
			})
			
			if (res.code === 2000) {
				tableData.value = res.data.data.map(item => ({
					...item,
					loading: false
				}))
			}
		} catch (error) {
			console.error('获取字典项失败:', error)
		} finally {
			tableLoading.value = false
		}
	}

	// 树节点点击事件
	const handleNodeClick = (data) => {
		selectedDictionary.value = data
		fetchDictionaryItems(data.id)
		if (isMobile.value) {
			showTable.value = true
		}
	}

	// 添加字典分类
	const addDictionary = () => {
		isDialogCategoryVisible.value = true
		nextTick(()=>{
			categoryDialog.value.addModuleFn(null,'新增')
		})
		
	}

	// 编辑字典分类
	const editDictionary = (data) => {
		isDialogCategoryVisible.value = true
		nextTick(()=>{
			categoryDialog.value.addModuleFn(data,'编辑')
		})
	}

	// 删除字典分类
	const deleteDictionary = async (node, data) => {
		try {
			await ElMessageBox.confirm(
				`确认删除字典分类"${data.label}"?`,
				'提示',
				{
					confirmButtonText: '确认',
					cancelButtonText: '取消',
					type: 'warning'
				}
			)
			
			const res = await Api.systemDictionaryDelete({ id: data.id })
			if (res.code === 2000) {
				ElMessage.success(res.msg)
				const parent = node.parent
				const children = parent.data.children || parent.data
				const index = children.findIndex(d => d.id === data.id)
				children.splice(index, 1)
				
				// 如果删除的是当前选中节点，则选中第一个节点
				if (selectedDictionary.value?.id === data.id) {
					if (dictionaryTree.value.length > 0) {
						treeRef.value.setCurrentKey(dictionaryTree.value[0].id)
						handleNodeClick(dictionaryTree.value[0])
					} else {
						selectedDictionary.value = null
						tableData.value = []
					}
				}
			} else {
				ElMessage.error(res.msg)
			}
		} catch (error) {
			if (error !== 'cancel') {
				ElMessage.error('删除失败')
				}
			}
	}

	// 添加字典项
	const addDictionaryItem = () => {
		if (!selectedDictionary.value) return
		isDialogItemVisible.value = true
		nextTick(()=>{
			itemDialog.value.addModuleFn(null,'新增',selectedDictionary.value.id)
		})
		
	}

	// 编辑字典项
	const editDictionaryItem = (row) => {
		isDialogItemVisible.value = true
		nextTick(()=>{
			itemDialog.value.addModuleFn(row,'编辑',selectedDictionary.value.id)
		})
	}

	// 删除字典项
	const deleteDictionaryItem = async (row) => {
		try {
			const res = await Api.systemDictionaryDelete({ id: row.id })
				if (res.code === 2000) {
					ElMessage.success(res.msg)
					const index = tableData.value.findIndex(item => item.id === row.id)
					if (index !== -1) {
						tableData.value.splice(index, 1)
					}
			} else {
				ElMessage.error(res.msg)
			}
		} catch (error) {
			ElMessage.error('删除失败')
		}
	}

	// 批量删除
	const batchDelete = async () => {
		try {
			await ElMessageBox.confirm(
			`确认删除选中的${selectedItems.value.length}项?`,
			'提示',
			{
				confirmButtonText: '确认',
				cancelButtonText: '取消',
				type: 'warning'
			}
			)
			
			const res = await Api.systemDictionaryDelete({
				id: selectedItems.value.map(item => item.id)
			})
			
			if (res.code === 2000) {
				ElMessage.success(res.msg)
				// 从表格中移除已删除项
				selectedItems.value.forEach(item => {
					const index = tableData.value.findIndex(i => i.id === item.id)
					if (index !== -1) {
					tableData.value.splice(index, 1)
					}
				})
				selectedItems.value = []
			} else {
				ElMessage.error(res.msg)
			}
		} catch (error) {
			if (error !== 'cancel') {
				ElMessage.error('删除失败')
			}
		}
	}

	// 切换状态
	const toggleStatus = async (row) => {
		try {
			row.loading = true
			const res = await Api.systemDictionarySetStatus({
				id: row.id,
				status: row.status
			})
			
			if (res.code !== 2000) {
				// 更新失败时恢复状态
				row.status = row.status ? false : true
				ElMessage.warning(res.msg)
			}else{
				ElMessage.success("设置成功")
			}
		} catch (error) {
			row.status = row.status ? false : true
			ElMessage.error('状态更新失败')
		} finally {
			row.loading = false
		}
	}

	// 表格选择变化
	const handleSelectionChange = (selection) => {
		selectedItems.value = selection
	}

	// 切换全屏：原生 Fullscreen API（fixed+z-index 模拟会被 header 的层叠上下文压住）
	const containerRef = ref(null)
	const toggleFullScreen = () => {
		fullScreen(containerRef.value)
		// API 被拒/不可用（部分 WebView、iframe）时降级为 fixed 模拟
		setTimeout(() => {
			if (!document.fullscreenElement && !document.webkitIsFullScreen) {
				isFullScreen.value = !isFullScreen.value
			}
		}, 80)
	}
	// 全屏状态以浏览器实际状态为准，Esc 退出时自动同步
	const onFullscreenChange = () => {
		isFullScreen.value = !!(document.fullscreenElement || document.webkitIsFullScreen)
	}
</script>

<style scoped lang="scss">
	.dict-container {
		padding:14px 20px 20px 18px;
		height: 100%;
		display: flex;
		background: transparent; /* 透出全局蓝调渐变+极光，不再整块白底 */

	&.full-screen {
		/* 原生全屏下浏览器保证盖住 header，此样式只负责全屏视觉 */
		background-color: var(--ly-bg-page, #EEF2FB);
		background-image: var(--ly-page-gradient, none);
	}

	.main-container {
		height: 100%;
		flex: 1;
		gap: 14px;
		background: transparent;
		border: none;
		overflow: visible;

		.tree-panel {
			border-right: none;
			border-radius: 16px;
			background: var(--ly-glass-bg, rgba(246, 249, 255, 0.66));
			backdrop-filter: var(--ly-glass-blur, saturate(1.6) blur(20px));
			-webkit-backdrop-filter: var(--ly-glass-blur, saturate(1.6) blur(20px));
			border: 1px solid var(--ly-glass-border, rgba(255, 255, 255, 0.7));
			box-shadow: var(--ly-shadow-card, 0 10px 34px rgba(27, 35, 64, 0.08));
			transition: all 0.3s ease;

			.tree-container {
				height: 100%;
				display: flex;
				flex-direction: column;
			}
		}

		.content-container {
			flex: 1;
			display: flex;
			flex-direction: column;
			border-radius: 16px;
			background: var(--ly-glass-bg, rgba(246, 249, 255, 0.66));
			backdrop-filter: var(--ly-glass-blur, saturate(1.6) blur(20px));
			-webkit-backdrop-filter: var(--ly-glass-blur, saturate(1.6) blur(20px));
			border: 1px solid var(--ly-glass-border, rgba(255, 255, 255, 0.7));
			box-shadow: var(--ly-shadow-card, 0 10px 34px rgba(27, 35, 64, 0.08));
		}
	}

	.panel-header {
		padding: 16px;
		background: transparent;
		border-bottom: 1px solid var(--ly-line-soft, rgba(27, 35, 64, 0.06));
		display: flex;
		align-items: center;
		justify-content: space-between;

		.action-buttons {
			display: flex;
			flex-wrap: wrap;
		}
	}
	
	.no-padding {
		padding: 0 !important;
	}

	.leftTreeMenu{
		:deep(.el-tree-node__content){
			height: 32px;
		}
		:deep(.el-tree-node__expand-icon){
			width:0px;
		}
	}
	
	.tree-node {
		display: flex;
		align-items: center;
		width: 100%;
		padding-right: 2px;
		
		.node-label {
			flex: 1;
			overflow: hidden;
			text-overflow: ellipsis;
		}
		
		.node-value {
			font-size: 12px;
			color: var(--el-text-color-secondary);
			flex-shrink: 0;
		}
		
		.node-actions {
			transition: opacity 0.2s;
			display: flex;
			:deep(.el-button){
				padding: 5px 6px;
			}
		}
	}
	
		.mobile-back-btn {
			margin-left: auto;
		}
	}

	@media (max-width: 768px) {
		.dict-container {
			.main-container {
				flex-direction: column;
			
			.tree-panel,
			.content-container {
				width: 100% !important;
			}
			
			.tree-panel {
				border-right: none;
				border-bottom: 1px solid var(--el-border-color-light);
			}
			}
			
			.tree-node .node-actions {
				opacity: 1;
			}
		}
	}
</style>