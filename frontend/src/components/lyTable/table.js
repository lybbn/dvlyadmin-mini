//el-table数据表格配置

import {autoStorage} from '@/utils/util.js'

export default {
	successCode: 2000,												//请求完成代码
	pageSize: 10,													//table表格每一页条数
	pageSizes: [10, 20, 30, 40, 100, 200],								//table表格可设置的一页条数
	paginationLayout: "total, sizes, prev, pager, next, jumper",	//el-table表格分页布局，可设置"total, sizes, prev, pager, next, jumper"
	request: {							//请求规定字段
		page: 'page',					//规定当前分页字段
		pageSize: 'limit',			//规定一页条数字段
		prop: 'prop',					//规定排序字段名字段
		order: 'order'					//规定排序规格字段
	},
	/**
	 * 自定义列保存处理
	 * @tableName lyTable组件的props->tableName
	 * @column 用户配置好的列
	 */
	columnSettingSave: function (tableName, column) {
		return new Promise((resolve) => {
			setTimeout(()=>{
				autoStorage.set(tableName,JSON.stringify(column))
				resolve(true)
			},500)
		})
	},
	/**
	 * 获取自定义列
	 * @tableName lyTable组件的props->tableName
	 * @column 组件接受到的props->column
	 */
	columnSettingGet: function (tableName, column) {
		return new Promise((resolve) => {
			const userColumn = JSON.parse(autoStorage.get(tableName)) || []
			if(userColumn){
				resolve(userColumn)
			}else{
				resolve(column)
			}
		})
	},
	/**
	 * 重置自定义列
	 * @tableName lyTable组件的props->tableName
	 * @column 组件接受到的props->column
	 */
	columnSettingReset: function (tableName, column) {
		return new Promise((resolve) => {
			setTimeout(()=>{
				autoStorage.remove(tableName)
				resolve(column)
			},500)
		})
	}
}
