import api from "./api.js"

/**
 * 创建CRUD配置,支持覆盖配置
 * @param {Object} options - 自定义配置选项
 * @returns {Object} CRUD配置对象
 */
export function createCrudConfig(options = {}){
    //需修改：命名规则（文件名+Table）
    let tableName = "buserManageTable"
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
        resetPass:api.resetPass,
        ...(options.request || {}) // 允许覆盖请求方法
    }
    //table列配置
    const defaultColumns = [
        {
            label: "账号",
            prop: "username",
            minWidth: "130"
        },
        {
            label: "姓名",
            prop: "name",
            minWidth: "90",
        },
        {
            label: "头像",
            prop: "avatar",
            minWidth: "90"
        },
        {
            label: "邮箱",
            prop: "email",
            minWidth: "170"
        },
        {
            label: "联系电话",
            prop: "mobile",
            minWidth: "150"
        },
        {
            label: "部门",
            prop: "dept",
            exportField:"deptName",
            minWidth: "120"
        },
        {
            label: "角色",
            prop: "role",
            exportField:"roleNames",
            minWidth: "130"
        },
        {
            label: "状态",
            prop: "is_active",
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
                hidePagination:false,
                ...(options.pagination || {})
            },
            //crud按钮配置
            rowHandle:{
                width: 205,//操作列宽度,0表示不显示表格操作列
                fixed:"right",//固定操作列在右侧
                ...(options.rowHandle || {})
            },
            //table属性
            table: {
                tableName:tableName,
                pageSize:10,
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