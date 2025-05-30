<!--
 * @Descripttion: 封装数据表格组件table
 * @version: 1.2
 * @Author: lybbn
 * @Date: 2023-11-02
*  @Date: 2025-05-30
 * @program: dvlyadmin-mini
-->

<template>
	<div class="lyTable" :style="{'height':_height}" ref="lyTableMain" v-loading="loading">
		<div class="lyTable-table" :style="{'height':_table_height}">
			<el-table v-bind="$attrs" :data="tableData" :row-key="rowKey" :key="toggleIndex" ref="lyTable" :height="height=='auto'?null:'100%'" :size="config.size" :border="config.border" :stripe="config.stripe" :summary-method="remoteSummary?remoteSummaryMethod:summaryMethod" @sort-change="sortChange" @filter-change="filterChange" @selection-change="handleSelectionChange">
				<el-table-column type="selection" width="60" align="center" v-if="showSelectable"></el-table-column>
                <el-table-column type="index" width="60" align="center" label="序号" v-if="showSequence">
                    <template #default="scope">
                        <span v-text="getTableIndex(scope.$index)"></span>
                    </template>
                </el-table-column>
				<slot></slot>
				<template v-for="(item, index) in userColumn" :key="index">
					<el-table-column v-if="!item.hide" :column-key="item.prop" :label="item.label" :prop="item.prop" :min-width="item.minWidth" :width="item.width" :sortable="item.sortable" :fixed="item.fixed" :filters="item.filters" :filter-method="remoteFilter||!item.filters?null:filterHandler" :show-overflow-tooltip="getShowOverflowTooltip(item.showOverflowTooltip)">
						<template #default="scope">
							<slot :name="item.prop" v-bind="scope">
								{{getNestedValue(scope.row, item.prop)}}
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
		<div class="lyTable-page" :class="{'lyTable-page-bk':paginationColorBackground,'lyTable-page-border':config.border}" v-if="!hidePagination || !hideDo">
			<div class="lyTable-pagination lyPagination-page">
				<el-pagination v-if="!hidePagination" :disabled="paginationDisabled" :background="paginationBackground" :size="paginationSmall?'small':'default'" :layout="paginationLayout" :total="total" :page-size="lyPageSize" :page-sizes="pageSizes" v-model:currentPage="currentPage" @current-change="paginationChange" @update:page-size="pageSizeChange"></el-pagination>
			</div>
			<div class="lyTable-do" v-if="!hideDo">
				<el-button v-if="!hideRefresh" @click="refreshData" icon="refresh" circle style="margin-left:15px"></el-button>
				<el-popover v-if="column != undefined && column != null && column.length > 0" placement="top" title="列设置" :width="500" trigger="click" :hide-after="0" @show="customColumnShow=true" @after-leave="customColumnShow=false">
					<template #reference>
						<el-button icon="set-up" circle style="margin-left:15px"></el-button>
					</template>
					<columnSetting v-if="customColumnShow" ref="lyColumnSetting" @userChange="columnSettingChange" @save="columnSettingSave" @back="columnSettingBack" :column="userColumn"></columnSetting>
				</el-popover>
				<el-popover v-if="!hideSetting" placement="top" title="表格设置" :width="400" trigger="click" :hide-after="0">
					<template #reference>
						<el-button icon="setting" circle style="margin-left:15px"></el-button>
					</template>
					<el-form label-width="80px" label-position="left">
						<el-form-item label="表格尺寸">
							<el-radio-group v-model="config.size" size="small" @change="configSizeChange">
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
			</div>
		</div>
	</div>
</template>

<script>
	import tableConfig from "./table.js";
	import columnSetting from './columnSetting.vue'

	export default {
		name: 'lyTable',
		components: {
			columnSetting
		},
		emits: ['dataChange','selectionChange'],
		props: {
			tableName: { type: String, default: "lyTable" },//用于标志该表格的名字（本地存储等时会用到此字段信息）
			successCode:{ type: Number, default: 2000 },//请求完成代码
			apiObj: { type: Function, default:null },//请求数据api方法
			params: { type: Object, default: () => ({}) },//请求api的额外自定义参数
			data: { type: Array, default: () => [] },//表格table数据
			height: { type: [String,Number], default: "100%" },//表格高度
			size: { type: String, default: "default" },//组件大小
			border: { type: Boolean, default: false },//纵向边框
			stripe: { type: Boolean, default: false },//表格斑马线
			showSelectable:{ type: Boolean, default: false },//是否显示表格多选
			showSequence:{ type: Boolean, default: false },//是否显示表格序号
			pageSize: { type: Number, default: tableConfig.pageSize },//table表格每一页条数
			pageSizes: { type: Array, default: tableConfig.pageSizes },//table表格可设置的一页条数[10, 20, 30, 40, 100, 200]
			rowKey: { type: String, default: "id" },
			summaryMethod: { type: Function, default: null },
			column: { type: Array, default: () => [] },//基于配置的动态列，与参数data二选一
			remoteSort: { type: Boolean, default: false },
			remoteFilter: { type: Boolean, default: false },
			remoteSummary: { type: Boolean, default: false },
			hidePagination: { type: Boolean, default: false },//隐藏底部分页
			hideDo: { type: Boolean, default: false },//隐藏底部功能按钮
			hideRefresh: { type: Boolean, default: false },//隐藏底部刷新按钮
			hideSetting: { type: Boolean, default: false },//隐藏底部设置按钮
			paginationLayout: { type: String, default: tableConfig.paginationLayout },
			paginationSmall:{ type: Boolean, default: true },//分页组件是否使用小型分页样式
			paginationBackground:{ type: Boolean, default: true },//分页组件是否为分页按钮添加背景色
			paginationDisabled:{ type: Boolean, default: false },//分页组件是否禁用
			paginationColorBackground:{ type: Boolean, default: true },//分页组件背景是否同表格
			emptyImage:{ type: String, default: "" },//空组件默认背景图片
			emptyImageSize:{ type: Number, default: 150 },//空组件默认背景图片大小
		},
		watch: {
			data(){
				this.tableData = this.data;
				this.total = this.tableData.length;
			},
			apiObj(){
				this.tableParams = this.params;
				this.refreshData();
			},
			column(){
				this.userColumn=this.column;
			},
			params: {
				handler(newVal, oldVal){
					this.tableParams = newVal;
				},
				immediate: true,
				deep: true
			}
		},
		computed: {
			_height() {
				return Number(this.height)?Number(this.height)+'px':this.height
			},
			_table_height() {
				return this.hidePagination && this.hideDo ? "100%" : "calc(100% - 50px)"
			}
		},
		data() {
			return {
				lyPageSize: this.pageSize,
				isActivat: true,
				emptyText: "暂无数据",
				toggleIndex: 0,
				tableData: [],
				total: 0,//总数据
				currentPage: 1,//当前页码
				prop: null,
				order: null,
				loading: false,
				tableHeight:'100%',
				tableParams: this.params,
				userColumn: [],
				customColumnShow: false,
				summary: {},//合计行字段结构
				config: {
					size: this.size,
					border: this.border,
					stripe: this.stripe
				}
			}
		},
		mounted() {
			//判断是否开启自定义列
			if(this.column){
				this.getCustomColumn()
			}else{
				this.userColumn = this.column
			}
			//判断是否静态数据
			if(!!this.apiObj){
				this.getData()
			}else if(this.data){
				this.tableData = this.data;
				this.total = this.tableData.length
			}
		},
		activated(){
			if(!this.isActivat){
				this.$refs.lyTable.doLayout()
			}
		},
		deactivated(){
			this.isActivat = false;
		},
		methods: {
			//获取表格el-table-column的prop属性的对应值，支持嵌套传入，如 数据为：scope.row 数据为 {a:{b:1,c:2}} prop传入为 a.b ，则取值为1 
			getNestedValue(obj, prop) {
				const props = prop.split('.');
				if(props.length==1){
					return obj[prop]
				}
				let value = obj;
				for (const p of props) {
					value = value[p];
					if (!value) {
						break;
					}
				}
				return value;
			},
			//页面loading
			loadingPage(bools){
				this.loading = bools
			},
			// 表格序列号
            getTableIndex($index) {
                // (当前页 - 1) * 当前显示数据条数 + 当前行数据的索引 + 1
                return (this.currentPage-1)*this.lyPageSize + $index +1
            },
			//获取默认表格列的省略
			getShowOverflowTooltip(flag){
				if(flag === false){
					return false
				}else if(flag === true){
					return true
				}
				return true
			},
			//获取列
			async getCustomColumn(){
				if(!!this.tableName){
					const userColumn = await tableConfig.columnSettingGet(this.tableName, this.column)
					if(userColumn.length<1){
						this.userColumn = this.column
					}else{
						this.userColumn = userColumn
					}
				}else{
					this.userColumn = this.column
				}
			},
			//获取数据
			async getData(){
				this.loading = true;
				var reqData = {
					[tableConfig.request.page]: this.currentPage,
					[tableConfig.request.pageSize]: this.lyPageSize,
					[tableConfig.request.prop]: this.prop,
					[tableConfig.request.order]: this.order
				}
				if(this.hidePagination){
					delete reqData[tableConfig.request.page]
					delete reqData[tableConfig.request.pageSize]
				}
				Object.assign(reqData, this.tableParams)
				try {
					var res = await this.apiObj(reqData);
				}catch(error){
					this.loading = false;
					this.emptyText = error.statusText;
					return false;
				}
				if(res.code != this.successCode){
					this.loading = false;
					this.emptyText = res.msg;
				}else{
					this.emptyText = "暂无数据";
					this.tableData = res.data.data || [];
					this.total = res.data.total || 0;
					this.summary = res.data.summary || {};
					this.loading = false;
				}
				if(!!this.$refs.lyTable){
					this.$refs.lyTable.setScrollTop(0)
				}
				this.$emit('dataChange', res, this.tableData)
			},
			//分页点击
			paginationChange(){
				this.getData();
			},
			//条数变化
			pageSizeChange(size){
				this.lyPageSize = size
				this.getData();
			},
			//刷新数据
			refreshData(){
				this.$refs.lyTable.clearSelection();
				this.getData();
			},
			//更新数据 合并上一次params
			updateData(params, page=1){
				this.currentPage = page;
				this.$refs.lyTable.clearSelection();
				Object.assign(this.tableParams, params || {})
				this.getData()
			},
			//重载数据 不替换params
			search(page=1){
				this.currentPage = page;
				this.$refs.lyTable.clearSelection();
				this.$refs.lyTable.clearSort()
				this.$refs.lyTable.clearFilter()
				this.getData()
			},
			//重载数据 替换params
			reload(params, page=1){
				this.currentPage = page;
				this.tableParams = params || {}
				this.$refs.lyTable.clearSelection();
				this.$refs.lyTable.clearSort()
				this.$refs.lyTable.clearFilter()
				this.getData()
			},
			//自定义变化事件
			columnSettingChange(userColumn){
				this.userColumn = userColumn;
				this.toggleIndex += 1;
			},
			//自定义列保存
			async columnSettingSave(userColumn){
				this.$refs.lyColumnSetting.isSave = true
				try {
					await tableConfig.columnSettingSave(this.tableName, userColumn)
				}catch(error){
					this.$message.error('保存失败')
					this.$refs.lyColumnSetting.isSave = false
				}
				this.$message.success('保存成功')
				this.$refs.lyColumnSetting.isSave = false
			},
			//自定义列重置
			async columnSettingBack(){
				this.$refs.lyColumnSetting.isSave = true
				try {
					const column = await tableConfig.columnSettingReset(this.tableName, this.column)
					this.userColumn = column
					this.$refs.lyColumnSetting.usercolumn = JSON.parse(JSON.stringify(this.userColumn||[]))
				}catch(error){
					this.$message.error('重置失败')
					this.$refs.lyColumnSetting.isSave = false
				}
				this.$refs.lyColumnSetting.isSave = false
			},
			//排序事件
			sortChange(obj){
				if(!this.remoteSort){
					return false
				}
				if(obj.column && obj.prop){
					this.prop = obj.prop
					this.order = obj.order
				}else{
					this.prop = null
					this.order = null
				}
				this.getData()
			},
			//本地过滤
			filterHandler(value, row, column){
				const property = column.property;
				return row[property] === value;
			},
			//过滤事件
			filterChange(filters){
				if(!this.remoteFilter){
					return false
				}
				Object.keys(filters).forEach(key => {
					filters[key] = filters[key].join(',')
				})
				this.updateData(filters)
			},
			//多选表格事件
			handleSelectionChange(selection) {
                this.$emit('selectionChange', selection)
            },
			//远程合计行处理
			remoteSummaryMethod(param){
				const {columns} = param
				const sums = []
				columns.forEach((column, index) => {
					if(index === 0) {
						sums[index] = '合计'
						return
					}
					const values =  this.summary[column.property]
					if(values){
						sums[index] = values
					}else{
						sums[index] = ''
					}
				})
				return sums
			},
			configSizeChange(){
				this.$refs.lyTable.doLayout()
			},
			//插入行 unshiftRow
			unshiftRow(row){
				this.tableData.unshift(row)
			},
			//插入行 pushRow
			pushRow(row){
				this.tableData.push(row)
			},
			//根据key覆盖数据
			updateKey(row, rowKey=this.rowKey){
				this.tableData.filter(item => item[rowKey]===row[rowKey]).forEach(item => {
					Object.assign(item, row)
				})
			},
			//根据index覆盖数据
			updateIndex(row, index){
				Object.assign(this.tableData[index], row)
			},
			//根据index删除
			removeIndex(index){
				this.tableData.splice(index, 1)
			},
			//根据index批量删除
			removeIndexes(indexes=[]){
				indexes.forEach(index => {
					this.tableData.splice(index, 1)
				})
			},
			//根据key删除
			removeKey(key, rowKey=this.rowKey){
				this.tableData.splice(this.tableData.findIndex(item => item[rowKey]===key), 1)
			},
			//根据keys批量删除
			removeKeys(keys=[], rowKey=this.rowKey){
				keys.forEach(key => {
					this.tableData.splice(this.tableData.findIndex(item => item[rowKey]===key), 1)
				})
			},
			//原生方法转发
			clearSelection(){
				this.$refs.lyTable.clearSelection()
			},
			toggleRowSelection(row, selected){
				this.$refs.lyTable.toggleRowSelection(row, selected)
			},
			toggleAllSelection(){
				this.$refs.lyTable.toggleAllSelection()
			},
			toggleRowExpansion(row, expanded){
				this.$refs.lyTable.toggleRowExpansion(row, expanded)
			},
			setCurrentRow(row){
				this.$refs.lyTable.setCurrentRow(row)
			},
			clearSort(){
				this.$refs.lyTable.clearSort()
			},
			clearFilter(columnKey){
				this.$refs.lyTable.clearFilter(columnKey)
			},
			doLayout(){
				this.$refs.lyTable.doLayout()
			},
			sort(prop, order){
				this.$refs.lyTable.sort(prop, order)
			}
		}
	}
</script>

<style scoped>
	.lyTable {

	}
	.lyTable-table {
		height: calc(100% - 50px);
	}
	.lyTable-page {
		height:50px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding:0 15px;
	}
	.lyTable-page-bk {
		background: var(--el-fill-color-blank);
	}
	.lyTable-page-border{
		border-bottom: 1px solid var(--el-border-color-lighter);
        border-left: 1px solid var(--el-border-color-lighter);
        border-right: 1px solid var(--el-border-color-lighter);
	}
	.lyTable-do {
		white-space: nowrap;
	}
	.lyTable:deep(.el-table__footer) .cell {
		font-weight: bold;
	}
	.lyTable:deep(.el-table__body-wrapper) .el-scrollbar__bar.is-horizontal {
		height: 8px;
		border-radius: 8px;
	}
	.lyTable:deep(.el-table__body-wrapper) .el-scrollbar__bar.is-vertical {
		width: 8px;
		border-radius: 8px;
	}
</style>
