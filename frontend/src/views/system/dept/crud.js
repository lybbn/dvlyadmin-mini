import api from "./api.js"

/**
 * 创建CRUD配置,支持覆盖配置
 * @param {Object} options - 自定义配置选项
 * @returns {Object} CRUD配置对象
 */
export function createCrudConfig(options = {}){
    //需修改：命名规则（文件名+Table）
    let tableName = "deptManageTable"
    //crud请求方法配置
    const request = {
        add:api.add,
        del:api.del,
        edit:api.edit,
        list:api.list,
        export:api.export,
        detail:null,
        import:api.import,
        dltemplate:api.downloadTemplate,
        setStatus:api.setStatus,
        ...(options.request || {}) // 允许覆盖请求方法
    }
    //table列配置
    const defaultColumns = [
        {
            label: "部门名称",
            prop: "name",
            minWidth: "130"
        },
        {
            label: "标识字符",
            prop: "key",
            minWidth: "100",
        },
        {
            label: "负责人",
            prop: "owner",
            minWidth: "100"
        },
        {
            label: "状态",
            prop: "status",
            width: "100"
        },
        {
            label: "排序",
            prop: "sort",
            width: "100"
        },
        {
            label: "创建时间",
            prop: "create_datetime",
            minWidth: "180"
        }
    ]

    return {
        crudOptions:{
            //接口配置
            request: request,
            //搜索栏目配置
            searchBar:{
                showSearchBar:true,//显示搜索栏目
                ...(options.searchBar || {})
            },
            //分页
            pagination:{
                hidePagination:true,
                ...(options.pagination || {})
            },
            //crud按钮配置
            rowHandle:{
                width: 150,//操作列宽度,0表示不显示表格操作列
                fixed:"right",//固定操作列在右侧
                ...(options.rowHandle || {})
            },
            //table属性
            table: {
                tableName:tableName,
                pageSize:999,
				rowKey: 'id',
				lazy: false,
                isTree:true,
				treeProps: { children: 'children', hasChildren: 'hasChildren' },
                border:true,
                defaultExpandAll:true,
                showSelectable:true,//表格显示复选项框
                hideImport:true,
                hideExport:false,
                ...(options.table || {})
			},
            //table列字段
            columns:options.columns || defaultColumns
        }
    }
}