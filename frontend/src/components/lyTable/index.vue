<!--
 * @Descripttion: 封装数据表格组件table
 * @version: 1.2
 * @Author: lybbn
 * @Date: 2023-11-02
*  @Date: 2025-05-30
 * @program: dvlyadmin-mini
-->
<template>
	<div class="lyTable" :style="{ height: _height }" ref="lyTableMain" v-loading="loading">
		<div class="lytopaction">
			<slot name="table-top-bar"></slot>
		</div>
		<div class="lyTable-table" :style="{ height: _table_height }">
			<el-table
				v-bind="$attrs"
				:data="tableData"
				:row-key="rowKey"
				:key="toggleIndex"
				ref="lyTable"
				:height="height === 'auto' ? null : '100%'"
				:size="config.size"
				:border="config.border"
				:stripe="config.stripe"
				:summary-method="remoteSummary ? remoteSummaryMethod : summaryMethod"
				@sort-change="sortChange"
				@filter-change="filterChange"
				@selection-change="handleSelectionChange"
			>
				<el-table-column
					type="selection"
					width="60"
					align="center"
					v-if="showSelectable"
					></el-table-column>
				<el-table-column
					type="index"
					width="60"
					align="center"
					label="序号"
					v-if="showSequence"
				>
					<template #default="scope">
						<span v-text="getTableIndex(scope.$index)"></span>
					</template>
				</el-table-column>
				<slot></slot>
				<template v-for="(item, index) in userColumn" :key="index">
					<el-table-column
						v-if="!item.hide"
						:column-key="item.prop"
						:label="item.label"
						:prop="item.prop"
						:min-width="item.minWidth"
						:width="item.width"
						:sortable="item.sortable"
						:fixed="item.fixed"
						:filters="item.filters"
						:filter-method="remoteFilter || !item.filters ? null : filterHandler"
						:show-overflow-tooltip="getShowOverflowTooltip(item.showOverflowTooltip)"
					>
						<template #default="scope">
							<slot :name="item.prop" v-bind="scope">
								{{ getNestedValue(scope.row, item.prop) }}
							</slot>
						</template>
					</el-table-column>
				</template>
				<slot name="lytable-r"></slot>
				<template #empty>
					<el-empty :description="emptyText" :image="emptyImage" :image-size="emptyImageSize"></el-empty>
				</template>
			</el-table>
		</div>
		<div class="lyTable-page"
			:class="{
				'lyTable-page-bk': paginationColorBackground,
				'lyTable-page-border': config.border
			}"
			v-if="!hidePagination || (!hideDo && doPositionBottom)"
		>
			<div class="lyTable-pagination lyPagination-page">
				<el-pagination
					v-if="!hidePagination"
					:disabled="paginationDisabled"
					:background="paginationBackground"
					:size="paginationSmall ? 'small' : 'default'"
					:layout="paginationLayout"
					:total="total"
					:page-size="lyPageSize"
					:page-sizes="pageSizes"
					v-model:current-page="currentPage"
					@current-change="paginationChange"
					@update:page-size="pageSizeChange"
				></el-pagination>
			</div>
			<TableActions
				v-if="!hideDo && doPositionBottom"
				:hide-refresh="hideRefresh"
				:hide-setting="hideSetting"
				:user-column="userColumn"
				:column="column"
				:config="config"
				@refresh="refreshData"
				@column-change="columnSettingChange"
				@column-save="columnSettingSave"
				@column-back="columnSettingBack"
				@size-change="configSizeChange"
				@border-change="val => config.border = val"
				@stripe-change="val => config.stripe = val"
			/>
			<!-- <div class="lyTable-do" v-if="!hideDo && doPositionBottom">
				<el-button
				v-if="!hideRefresh"
				@click="refreshData"
				icon="refresh"
				circle
				style="margin-left: 15px"
				></el-button>
				<el-popover
					v-if="column != undefined && column != null && column.length > 0"
					placement="top"
					title="列设置"
					:width="500"
					trigger="click"
					:hide-after="0"
					@show="customColumnShow = true"
					@after-leave="customColumnShow = false"
					>
						<template #reference>
							<el-button icon="set-up" circle style="margin-left: 15px"></el-button>
						</template>
					<column-setting
						v-if="customColumnShow"
						ref="lyColumnSetting"
						@userChange="columnSettingChange"
						@save="columnSettingSave"
						@back="columnSettingBack"
						:column="userColumn"
					></column-setting>
				</el-popover>
				<el-popover
					v-if="!hideSetting"
					placement="top"
					title="表格设置"
					:width="400"
					trigger="click"
					:hide-after="0"
					>
					<template #reference>
						<el-button icon="setting" circle style="margin-left: 15px"></el-button>
					</template>
					<el-form label-width="80px" label-position="left">
						<el-form-item label="表格尺寸">
							<el-radio-group
								v-model="config.size"
								size="small"
								@change="configSizeChange"
							>
								<el-radio-button value="large">大</el-radio-button>
								<el-radio-button value="default">正常</el-radio-button>
								<el-radio-button value="small">小</el-radio-button>
							</el-radio-group>
						</el-form-item>
						<el-form-item label="样式">
							<el-checkbox v-model="config.border" label="纵向边框"></el-checkbox>
							<el-checkbox v-model="config.stripe" label="斑马纹"></el-checkbox>
						</el-form-item>
					</el-form>
				</el-popover>
			</div> -->
		</div>
	</div>
</template>

<script setup>
	import { ref, watch, computed, onMounted, onActivated, onDeactivated } from 'vue'
	import { ElMessage } from 'element-plus'
	import tableConfig from "./table.js"
	// import ColumnSetting from './columnSetting.vue'
	import TableActions from './TableActions.vue'

	const props = defineProps({
		tableName: { type: String, default: "lyTable" },
		successCode: { type: Number, default: 2000 },
		apiObj: { type: Function, default: null },//api接口
		params: { type: Object, default: () => ({}) },
		data: { type: Array, default: () => [] },
		height: { type: [String, Number], default: "100%" },
		size: { type: String, default: "default" },
		border: { type: Boolean, default: false },
		stripe: { type: Boolean, default: false },
		showSelectable: { type: Boolean, default: false },//显示复选框
		showSequence: { type: Boolean, default: false },//显示索引
		pageSize: { type: Number, default: tableConfig.pageSize },//显示一页几行数据
		pageSizes: { type: Array, default: tableConfig.pageSizes },
		rowKey: { type: String, default: "id" },
		summaryMethod: { type: Function, default: null },
		column: { type: Array, default: () => [] },
		remoteSort: { type: Boolean, default: false },
		remoteFilter: { type: Boolean, default: false },
		remoteSummary: { type: Boolean, default: false },
		doPositionBottom:{ type: Boolean, default: true },//操作栏是否在底部
		hidePagination: { type: Boolean, default: false },//隐藏分页
		hideDo: { type: Boolean, default: false },//隐藏底部操作栏
		hideRefresh: { type: Boolean, default: false },//隐藏刷新
		hideSetting: { type: Boolean, default: false },//隐藏设置
		paginationLayout: { type: String, default: tableConfig.paginationLayout },
		paginationSmall: { type: Boolean, default: true },
		paginationBackground: { type: Boolean, default: true },
		paginationDisabled: { type: Boolean, default: false },
		paginationColorBackground: { type: Boolean, default: true },
		emptyImage: { type: String, default: "" },
		emptyImageSize: { type: Number, default: 150 },
	})

	const emit = defineEmits(['dataChange', 'selectionChange'])
	
	const lyTableMain = ref(null)
	const lyTable = ref(null)
	const lyColumnSetting = ref(null)

	// Computed properties
	const _height = computed(() => Number(props.height) ? `${Number(props.height)}px` : props.height)
	const _table_height = computed(() => props.hidePagination && (props.hideDo || !props.doPositionBottom) ? "100%" : "calc(100% - 50px)")

	// Reactive state
	const lyPageSize = ref(props.pageSize)
	const isActivat = ref(true)
	const emptyText = ref("暂无数据")
	const toggleIndex = ref(0)
	const tableData = ref([])
	const total = ref(0)
	const currentPage = ref(1)
	const prop = ref(null)
	const order = ref(null)
	const loading = ref(false)
	const tableHeight = ref('100%')
	const tableParams = ref({ ...props.params })
	const userColumn = ref([])
	const customColumnShow = ref(false)
	const summary = ref({})

	const config = ref({
	size: props.size,
	border: props.border,
	stripe: props.stripe
	})

	// Watchers
	watch(() => props.data, (newVal) => {
		tableData.value = newVal
		total.value = newVal.length
	})

	watch(() => props.apiObj, () => {
		tableParams.value = { ...props.params }
		refreshData()
	})

	watch(() => props.column, (newVal) => {
		userColumn.value = newVal
	})

	watch(() => props.params, (newVal) => {
		tableParams.value = { ...newVal }
	}, { immediate: true, deep: true })

	// Methods
	const getNestedValue = (obj, prop) => {
		const props = prop.split('.')
		if (props.length === 1) return obj[prop]
		
		let value = obj
		for (const p of props) {
			value = value[p]
			if (!value) break
		}
		return value
	}

	const loadingPage = (bools) => {
		loading.value = bools
	}

	const getTableIndex = ($index) => {
		return (currentPage.value - 1) * lyPageSize.value + $index + 1
	}

	const getShowOverflowTooltip = (flag) => {
		if (flag === false) return false
		if (flag === true) return true
		return true
	}

	const getCustomColumn = async () => {
		if (props.tableName) {
			const userCol = await tableConfig.columnSettingGet(props.tableName, props.column)
			userColumn.value = userCol.length < 1 ? props.column : userCol
		} else {
			userColumn.value = props.column
		}
	}

	const getData = async () => {
		loading.value = true
		const reqData = {
			[tableConfig.request.page]: currentPage.value,
			[tableConfig.request.pageSize]: lyPageSize.value,
			[tableConfig.request.prop]: prop.value,
			[tableConfig.request.order]: order.value
		}

		if (props.hidePagination) {
			delete reqData[tableConfig.request.page]
			delete reqData[tableConfig.request.pageSize]
		}

		Object.assign(reqData, tableParams.value)

		try {
			const res = await props.apiObj(reqData)
			if (res.code !== props.successCode) {
				emptyText.value = res.msg
			} else {
				emptyText.value = "暂无数据"
				tableData.value = res.data.data || []
				total.value = res.data.total || 0
				summary.value = res.data.summary || {}
				emit('dataChange', res, tableData.value)
			}
		} catch (error) {
			emptyText.value = error.statusText || "请求失败"
		} finally {
			loading.value = false
			lyTable.value?.setScrollTop(0)
		}
	}

	const paginationChange = () => {
		getData()
	}

	const pageSizeChange = (size) => {
		lyPageSize.value = size
		getData()
	}

	const refreshData = () => {
		lyTable.value?.clearSelection()
		getData()
	}

	const updateData = (params, page = 1) => {
		currentPage.value = page
		lyTable.value?.clearSelection()
		Object.assign(tableParams.value, params || {})
		getData()
	}

	const search = (page = 1) => {
		currentPage.value = page
		lyTable.value?.clearSelection()
		lyTable.value?.clearSort()
		lyTable.value?.clearFilter()
		getData()
	}

	const reload = (params, page = 1) => {
		currentPage.value = page
		tableParams.value = params || {}
		lyTable.value?.clearSelection()
		lyTable.value?.clearSort()
		lyTable.value?.clearFilter()
		getData()
	}

	const columnSettingChange = (userCol) => {
		userColumn.value = userCol
		toggleIndex.value += 1
	}

	const columnSettingSave = async (userCol) => {
		if (!lyColumnSetting.value) return
		
		lyColumnSetting.value.isSave = true
		try {
			await tableConfig.columnSettingSave(props.tableName, userCol)
			ElMessage.success('保存成功')
		} catch (error) {
			ElMessage.error('保存失败')
		} finally {
			lyColumnSetting.value.isSave = false
		}
	}

	const columnSettingBack = async () => {
		if (!lyColumnSetting.value) return
		
		lyColumnSetting.value.isSave = true
		try {
			const column = await tableConfig.columnSettingReset(props.tableName, props.column)
			userColumn.value = column
			lyColumnSetting.value.usercolumn = JSON.parse(JSON.stringify(userColumn.value))
		} catch (error) {
			ElMessage.error('重置失败')
		} finally {
			lyColumnSetting.value.isSave = false
		}
	}

	const sortChange = (obj) => {
		if (!props.remoteSort) return
		
		if (obj.column && obj.prop) {
			prop.value = obj.prop
			order.value = obj.order
		} else {
			prop.value = null
			order.value = null
		}
		getData()
	}

	const filterHandler = (value, row, column) => {
		const property = column.property
		return row[property] === value
	}

	const filterChange = (filters) => {
		if (!props.remoteFilter) return
		
		const newFilters = {}
		Object.keys(filters).forEach(key => {
			newFilters[key] = filters[key].join(',')
		})
		updateData(newFilters)
	}

	const handleSelectionChange = (selection) => {
		emit('selectionChange', selection)
	}

	const remoteSummaryMethod = (param) => {
		const { columns } = param
		const sums = []
		columns.forEach((column, index) => {
			if (index === 0) {
				sums[index] = '合计'
				return
			}
			const values = summary.value[column.property]
			sums[index] = values || ''
		})
		return sums
	}

	const configSizeChange = () => {
		lyTable.value?.doLayout()
	}

	const unshiftRow = (row) => {
		tableData.value.unshift(row)
	}

	const pushRow = (row) => {
		tableData.value.push(row)
	}

	const updateKey = (row, rowKey = props.rowKey) => {
		tableData.value
			.filter(item => item[rowKey] === row[rowKey])
			.forEach(item => {
			Object.assign(item, row)
			})
	}

	const updateIndex = (row, index) => {
		if (index >= 0 && index < tableData.value.length) {
			Object.assign(tableData.value[index], row)
		}
	}

	const removeIndex = (index) => {
		if (index >= 0 && index < tableData.value.length) {
			tableData.value.splice(index, 1)
		}
	}

	const removeIndexes = (indexes = []) => {
		indexes
			.filter(index => index >= 0 && index < tableData.value.length)
			.sort((a, b) => b - a) // Remove from end to beginning to avoid index issues
			.forEach(index => {
			tableData.value.splice(index, 1)
			})
	}

	const removeKey = (key, rowKey = props.rowKey) => {
		const index = tableData.value.findIndex(item => item[rowKey] === key)
		if (index !== -1) {
			tableData.value.splice(index, 1)
		}
	}

	const removeKeys = (keys = [], rowKey = props.rowKey) => {
		const indexes = keys
			.map(key => tableData.value.findIndex(item => item[rowKey] === key))
			.filter(index => index !== -1)
			.sort((a, b) => b - a) // Remove from end to beginning to avoid index issues
		
		indexes.forEach(index => {
			tableData.value.splice(index, 1)
		})
	}

	// Native table methods
	const clearSelection = () => lyTable.value?.clearSelection()
	const toggleRowSelection = (row, selected) => lyTable.value?.toggleRowSelection(row, selected)
	const toggleAllSelection = () => lyTable.value?.toggleAllSelection()
	const toggleRowExpansion = (row, expanded) => lyTable.value?.toggleRowExpansion(row, expanded)
	const setCurrentRow = (row) => lyTable.value?.setCurrentRow(row)
	const clearSort = () => lyTable.value?.clearSort()
	const clearFilter = (columnKey) => lyTable.value?.clearFilter(columnKey)
	const doLayout = () => lyTable.value?.doLayout()
	const sort = (prop, order) => lyTable.value?.sort(prop, order)

	// Lifecycle hooks
	onMounted(() => {
		if (props.column) getCustomColumn()
		if (props.apiObj) {
			getData()
		} else if (props.data && props.data.length) {
			tableData.value = props.data
			total.value = props.data.length
		}
	})

	onActivated(() => {
		if (!isActivat.value) {
			lyTable.value?.doLayout()
		}
	})

	onDeactivated(() => {
		isActivat.value = false
	})

	// Expose methods
	defineExpose({
		loadingPage,
		refreshData,
		updateData,
		search,
		reload,
		unshiftRow,
		pushRow,
		updateKey,
		updateIndex,
		removeIndex,
		removeIndexes,
		removeKey,
		removeKeys,
		clearSelection,
		toggleRowSelection,
		toggleAllSelection,
		toggleRowExpansion,
		setCurrentRow,
		clearSort,
		clearFilter,
		doLayout,
		sort,
		getData,
		tableData,
		tableParams
	})
</script>

<style scoped>
	.lyTable {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
	}

	.lyTable-table {
		height:100%;
	}

	.lyTable-page {
		height: 50px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 15px;
		flex-shrink: 0; /* 禁止收缩 */
	}

	.lyTable-page-bk {
		background: var(--el-fill-color-blank);
	}

	.lyTable-page-border {
		border-bottom: 1px solid var(--el-border-color-lighter);
		border-left: 1px solid var(--el-border-color-lighter);
		border-right: 1px solid var(--el-border-color-lighter);
	}

	.lyTable-do {
		white-space: nowrap;
	}

	:deep(.lyTable .el-table__footer .cell) {
		font-weight: bold;
	}

	:deep(.lyTable .el-table__body-wrapper .el-scrollbar__bar.is-horizontal) {
		height: 8px;
		border-radius: 8px;
	}

	:deep(.lyTable .el-table__body-wrapper .el-scrollbar__bar.is-vertical) {
		width: 8px;
		border-radius: 8px;
	}
</style>