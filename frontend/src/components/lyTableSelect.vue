<!--
 * @Descripttion: 表格选择器组件
 * @version: 1.1
 * @Program: django-vue-lyadmin
 * @Author: lybbn
 * @EditDate: 2025/07/11
-->

<template>
	<el-select
		ref="selectRef"
		v-model="defaultValue"
		:size="size"
		:clearable="clearable"
		:multiple="multiple"
		:collapse-tags="collapseTags"
		:collapse-tags-tooltip="collapseTagsTooltip"
		:filterable="filterable"
		:placeholder="placeholder"
		:disabled="disabled"
		:filter-method="filterMethod"
		@remove-tag="removeTag"
		@visible-change="visibleChange"
		@clear="clear"
		class="table-select"
	>
		<template #empty>
			<div class="ly-table-select__table" :style="{width: tableWidth > 0? tableWidth+ 'px':'100%'}" v-loading="loading">
				<div class="ly-table-select__header">
					<slot name="header" :form="formData" :submit="formSubmit"></slot>
				</div>
				
				<el-table
					ref="tableRef"
					border
					:data="tableData"
					:height="isMobile ? 'auto' : 350"
					:highlight-current-row="!multiple"
					@row-click="click"
					@select="select"
					@select-all="selectAll"
					style="width: 100%;"
					>
				<el-table-column v-if="multiple" type="selection" width="45"></el-table-column>
				<el-table-column v-else type="index" width="45">
					<template #default="scope">
						<span v-text="getIndex(scope.$index)"></span>
					</template>
				</el-table-column>
				<slot></slot>
				</el-table>
				
				<div class="ly-table-select__page">
					<Pagination 
						:small="true" 
						v-bind:child-msg="pageparm"  
						@callFather="callFather"
					/>
				</div>
			</div>
		</template>
	</el-select>
</template>

<script setup>
	import { ref, computed, watch, onMounted, nextTick } from 'vue'
	import { useWindowSize } from '@vueuse/core'
	import Pagination from "@/components/Pagination.vue"
	import { ElMessage } from 'element-plus'

	const props = defineProps({
		modelValue: null,
		successCode: { type: Number, default: 2000 }, // 网络请求完成代码
		apiObj: { type: Function, default: null }, // 网络请求的实例
		params: { type: Object, default: () => ({}) }, // 网络请求的额外参数
		placeholder: { type: String, default: "请选择" },
		size: { type: String, default: "default" },
		clearable: { type: Boolean, default: false },
		multiple: { type: Boolean, default: false },
		filterable: { type: Boolean, default: false },
		collapseTags: { type: Boolean, default: false },
		collapseTagsTooltip: { type: Boolean, default: false },
		disabled: { type: Boolean, default: false },
		tableWidth: { type: Number, default: 0 },//0表示100%
		mode: { type: String, default: "popover" },
		props: { type: Object, default: () => ({}) }
	})

	const emit = defineEmits(['update:modelValue', 'change'])

	// 响应式数据
	const loading = ref(false)
	const defaultValue = ref(props.multiple ? [] : null)
	const tableData = ref([])
	const formInline = ref({
		page: 1,
		limit: 10
	})
	const pageparm = ref({
		page: 1,
		limit: 10,
		total: 0
	})
	const formData = ref({})
	const selectRef = ref(null)
	const tableRef = ref(null)

	// 默认属性配置
	const defaultProps = ref({
		label: 'label',
		value: 'value',
		page: 'page',
		pageSize: 'limit'
	})

	// 合并传入的props
	Object.assign(defaultProps.value, props.props)

	// 检测是否为移动端
	const { width: windowWidth } = useWindowSize()
	const isMobile = computed(() => windowWidth.value < 768)

	// 监听modelValue变化
	watch(() => props.modelValue, (newVal) => {
		defaultValue.value = newVal
		autoCurrentLabel()
	}, { deep: true })

	// 组件挂载时初始化
	onMounted(() => {
		defaultValue.value = props.modelValue
		autoCurrentLabel()
	})

	// 表格序列号
	const getIndex = (index) => {
		return (pageparm.value.page - 1) * pageparm.value.limit + index + 1
	}

	// 分页回调
	const callFather = (parm) => {
		formInline.value.page = parm.page
		formInline.value.limit = parm.limit
		getData()
	}

	// 检查默认值
	const checkDefaultValue = () => {
		if (props.multiple && defaultValue.value === undefined) {
			defaultValue.value = []
		}
	}

	// 表格显示隐藏回调
	const visibleChange = (visible) => {
		if (visible) {
			formInline.value.page = 1
			formData.value = {}
			getData()
		} else {
			autoCurrentLabel()
		}
	}

	// 获取表格数据
	const getData = async () => {
		loading.value = true
		const reqData = {
			[defaultProps.value.page]: formInline.value.page,
			[defaultProps.value.pageSize]: formInline.value.limit,
		}
		
		Object.assign(reqData, props.params, formData.value)
		
		try {
			const res = await props.apiObj(reqData)
			loading.value = false
			
			if (res.code === props.successCode) {
				tableData.value = res.data.data
				pageparm.value.page = res.data.page
				pageparm.value.limit = res.data.limit
				pageparm.value.total = res.data.total
			} else {
				ElMessage.warning(res.msg)
			}
			
			// 表格默认赋值
			nextTick(() => {
				if (props.multiple) {
					checkDefaultValue()
					defaultValue.value.forEach(row => {
						const setrow = tableData.value.filter(item => 
							item[defaultProps.value.value] === row[defaultProps.value.value]
						)
						if (setrow.length > 0) {
							tableRef.value.toggleRowSelection(setrow[0], true)
						}
					})
				} else {
					const setrow = tableData.value.filter(item => 
						item[defaultProps.value.value] === defaultValue.value[defaultProps.value.value]
					)
					tableRef.value.setCurrentRow(setrow[0])
				}
				tableRef.value.setScrollTop(0)
			})
		} catch (error) {
			loading.value = false
			console.log
			ElMessage.error('请求失败')
		}
	}

	// 表单提交
	const formSubmit = () => {
		formInline.value.page = 1
		getData()
	}

	// 自动模拟options赋值
	const autoCurrentLabel = () => {
		nextTick(() => {
			if (!selectRef.value) return
			if (props.multiple) {
				selectRef.value.states.selected.forEach(item => {
					item.currentLabel = item.value[defaultProps.value.label]
				})
			} else {
				selectRef.value.selectedLabel = defaultValue.value?.[defaultProps.value.label] || ''
			}
		})
	}

	// 表格勾选事件
	const select = (rows, row) => {
		checkDefaultValue()
		const isSelect = rows.length && rows.indexOf(row) !== -1
		
		if (isSelect) {
			defaultValue.value.push(row)
		} else {
			const index = defaultValue.value.findIndex(
			item => item[defaultProps.value.value] == row[defaultProps.value.value]
			)
			if (index !== -1) {
				defaultValue.value.splice(index, 1)
			}
		}
		
		autoCurrentLabel()
		emit('update:modelValue', defaultValue.value)
		emit('change', defaultValue.value)
	}

	// 表格全选事件
	const selectAll = (rows) => {
		checkDefaultValue()
		const isAllSelect = rows.length > 0
		
		if (isAllSelect) {
			rows.forEach(row => {
				const isHas = defaultValue.value.find(
					item => item[defaultProps.value.value] == row[defaultProps.value.value]
				)
				if (!isHas) {
					defaultValue.value.push(row)
				}
			})
		} else {
			tableData.value.forEach(row => {
				const isHas = defaultValue.value.find(
					item => item[defaultProps.value.value] == row[defaultProps.value.value]
				)
				if (isHas) {
					const index = defaultValue.value.findIndex(
					item => item[defaultProps.value.value] == row[defaultProps.value.value]
					)
					defaultValue.value.splice(index, 1)
				}
			})
		}
		
		autoCurrentLabel()
		emit('update:modelValue', defaultValue.value)
		emit('change', defaultValue.value)
	}

	// 点击行事件
	const click = (row) => {
		if (props.multiple) {
			// 处理多选点击行
		} else {
			defaultValue.value = row
			selectRef.value.blur()
			autoCurrentLabel()
			emit('update:modelValue', defaultValue.value)
			emit('change', defaultValue.value)
		}
	}

	// tags删除后回调
	const removeTag = (tag) => {
		const row = findRowByKey(tag[defaultProps.value.value])
		tableRef.value.toggleRowSelection(row, false)
		emit('update:modelValue', defaultValue.value)
	}

	// 清空后的回调
	const clear = () => {
		emit('update:modelValue', defaultValue.value)
	}

	// 关键值查询表格数据行
	const findRowByKey = (value) => {
		return tableData.value.find(item => item[defaultProps.value.value] === value)
	}

	// 过滤方法
	const filterMethod = () => {
		getData()
	}

	// 触发select隐藏
	const blur = () => {
		selectRef.value.blur()
	}

	// 触发select显示
	const focus = () => {
		selectRef.value.focus()
	}

	// 暴露方法给父组件
	defineExpose({
		blur,
		focus
	})
</script>

<style scoped>
	.ly-table-select__table {
		padding: 12px;
		max-width: 100%;
		box-sizing: border-box;
	}

	.ly-table-select__page {
		padding-top: 2px;
	}

	.ly-table-select__header{
		display: flex;
		align-items: center;
	}

	/* 移动端适配 */
	@media (max-width: 768px) {
		.ly-table-select__table {
			width: 100% !important;
			padding: 8px;
		}
		
		.table-select {
			width: 100%;
		}
	}
</style>