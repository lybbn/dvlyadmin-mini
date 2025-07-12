import {ajaxGet,ajaxPost,ajaxDelete,ajaxPut,ajaxPatch,uploadImg,ajaxGetDetailByID,ajaxDownloadExcel,uploadFileParams,getDownloadFile,downloadFile} from './request';

const Api = {}
// 获取验证码
Api.getCaptcha = params => ajaxGet({url: `/api/captcha/`,params})
// 登录
Api.getToken = params => ajaxPost({url: `/api/token/`,params})
// 刷新登录token
Api.refreshToken = params => ajaxPost({url: `/api/token/refresh/`,params})
// 获取菜单
Api.apiSystemWebRouter = params => ajaxGet({url: `/api/system/menu/web_router/`,params})
// 获取路由json
Api.apiSchemeJson = params => ajaxGet({url: `/api/schema/lyjson/`,params})
// 上传图片
Api.apiSysImgUpload = params => uploadImg({url: `/api/system/sys_image_upload/`,params})

/**
 *个人中心
 * */
// 获取当前个人用户信息
Api.systemUserUserInfo= params => ajaxGet({url: `/api/system/user/user_info/`,params})
// 更新修改当前个人用户信息
Api.systemUserUserInfoEdit= params => ajaxPut({url: `/api/system/user/user_info/`,params})
// 用户重置个人密码
Api.systemUserChangePassword= params => ajaxPost({url: `/api/system/user/change_password/`,params})
// 用户修改头像
Api.systemUserChangeAvatar= params => ajaxPost({url: `/api/system/user/change_avatar/`,params})

/**
 *菜单管理
 * */
// 菜单管理列表
Api.apiSystemMenu = params => ajaxGet({url: `/api/system/menu/`,params})
// 菜单管理列表 -- 新增菜单
Api.apiSystemMenuAdd = params => ajaxPost({url: `/api/system/menu/`,params})
// 菜单管理列表 -- 编辑菜单
Api.apiSystemMenuEdit = params => ajaxPut({url: `/api/system/menu/`,params})
// 菜单管理列表 -- 删除菜单
Api.apiSystemMenuDelete = params => ajaxDelete({url: `/api/system/menu/`,params})
// 菜单管理列表 -- 新增菜单
Api.apiSystemMenuUpdateSort = params => ajaxPost({url: `/api/system/menu/update_sort/`,params})

// 获取菜单按钮模板
Api.apiSystemButtonTemplate = params => ajaxGet({url: `/api/system/button/`,params})
// 菜单按钮模板 -- 新增
Api.apiSystemButtonTemplateAdd = params => ajaxPost({url: `/api/system/button/`,params})
// 菜单按钮模板 -- 编辑
Api.apiSystemButtonTemplateEdit = params => ajaxPut({url: `/api/system/button/`,params})
// 菜单按钮模板 -- 删除
Api.apiSystemButtonTemplateDelete = params => ajaxDelete({url: `/api/system/button/`,params})

// 获取菜单按钮API
Api.apiSystemMenuButton = params => ajaxGet({url: `/api/system/menu_button/`,params})
// 菜单按钮API -- 新增
Api.apiSystemMenuButtonAdd = params => ajaxPost({url: `/api/system/menu_button/`,params})
// 菜单按钮API -- 编辑
Api.apiSystemMenuButtonEdit = params => ajaxPut({url: `/api/system/menu_button/`,params})
// 菜单按钮API -- 删除
Api.apiSystemMenuButtonDelete = params => ajaxDelete({url: `/api/system/menu_button/`,params})
// 菜单按钮API -- 批量生成
Api.apiSystemMenuButtonBatchGenerate = params => ajaxPost({url: `/api/system/menu_button/batch_generate/`,params})
// 根据角色获取菜单按钮
Api.apiSystemMenuButtonPermission= params => ajaxGet({url: `/api/system/menu_button/menu_button_permission/`,params})

// 获取菜单列
Api.apiSystemMenuField = params => ajaxGet({url: `/api/system/menu_field/`,params})
// 获取菜单列 -- 新增
Api.apiSystemMenuFieldAdd = params => ajaxPost({url: `/api/system/menu_field/`,params})
// 获取菜单列 -- 编辑
Api.apiSystemMenuFieldEdit = params => ajaxPut({url: `/api/system/menu_field/`,params})
// 获取菜单列 -- 删除
Api.apiSystemMenuFieldDelete = params => ajaxDelete({url: `/api/system/menu_field/`,params})
// 获取所有自定义modles信息
Api.apiSystemMenuFieldGetModels = params => ajaxGet({url: `/api/system/menu_field/get_models/`,params})
// 自动生成列
Api.apiSystemMenuFieldAutoCreate = params => ajaxPost({url: `/api/system/menu_field/auto_create/`,params})

// 部门管理
Api.apiSystemDept = params => ajaxGet({url: `/api/system/dept/`,params})
// 部门管理 -- 新增
Api.apiSystemDeptAdd = params => ajaxPost({url: `/api/system/dept/`,params})
// 部门管理 -- 编辑
Api.apiSystemDeptEdit = params => ajaxPut({url: `/api/system/dept/`,params})
// 部门管理 -- 删除
Api.apiSystemDeptDelete = params => ajaxDelete({url: `/api/system/dept/`,params})
// 部门管理 -- 禁用启用
Api.apiSystemDeptSetStatus = params => ajaxPost({url: `/api/system/dept/set_status/`,params})
// 部门管理 -- 导出
Api.apiSystemDeptExport = (queryParams,params) => ajaxDownloadExcel({url: `/api/system/dept/export_data/`,queryParams:queryParams,params})

// 角色管理
Api.apiSystemRole = params => ajaxGet({url: `/api/system/role/`,params})
// 角色管理 -- 新增
Api.apiSystemRoleAdd = params => ajaxPost({url: `/api/system/role/`,params})
// 角色管理 -- 编辑
Api.apiSystemRoleEdit = params => ajaxPut({url: `/api/system/role/`,params})
// 角色管理 -- 删除
Api.apiSystemRoleDelete = params => ajaxDelete({url: `/api/system/role/`,params})
// 角色管理 -- 禁用启用
Api.apiSystemRoleSetStatus = params => ajaxPost({url: `/api/system/role/set_status/`,params})
// 角色管理 -- 根据角色获取菜单
Api.apiSystemRoleIdToMenuid = (id) => ajaxGet({url: `/api/system/role_id_to_menu/`+id+'/'})

// 权限管理 - 获取角色+权限列表
Api.apiSystemRolePermission = params => ajaxGet({url: `/api/system/role_permission/`,params})

// 权限管理 - 保存
Api.apiSystemRolePermissionSave = params => ajaxPost({url: `/api/system/role_permission/save_permission/`,params})

// 用户管理 - 列表
Api.apiSystemUser = params => ajaxGet({url: `/api/system/user/`,params})

/**
 *日志管理
 * */
// 日志管理 查询
Api.systemOperationlog= params => ajaxGet({url: `/api/system/operation_log/`,params})
// 日志管理 我的日志
Api.getOwnerOperationLogs= params => ajaxGet({url: `/api/system/operation_log/getOwnerLogs/`,params})
// 日志管理 删除
Api.systemOperationlogDelete= params => ajaxDelete({url: `/api/system/operation_log/`,params})
// 日志管理 清空全部日志
Api.systemOperationlogDeletealllogsDelete= params => ajaxDelete({url: `/api/system/operation_log/deletealllogs/`,params})

/**
 *登录日志管理
 * */
// 登录日志管理 查询
Api.systemLoginlog= params => ajaxGet({url: `/api/system/login_log/`,params})
// 登录日志管理 我的日志
Api.getOwnerLoginlog= params => ajaxGet({url: `/api/system/login_log/getOwnerLogs/`,params})
// 登录日志管理 删除
Api.systemLoginlogDelete= params => ajaxDelete({url: `/api/system/login_log/`,params})
// 登录日志管理 清空全部日志
Api.systemLoginlogDeletealllogs= params => ajaxDelete({url: `/api/system/login_log/deletealllogs/`,params})

/**
*字典管理
 * */

// 字典管理
Api.systemDictionary = params => ajaxGet({url: `/api/system/dictionary/`,params})
// 字典管理 -- 新增
Api.systemDictionaryAdd = params => ajaxPost({url: `/api/system/dictionary/`,params})
// 字典管理 -- 编辑
Api.systemDictionaryEdit = params => ajaxPut({url: `/api/system/dictionary/`,params})
// 字典管理 -- 删除
Api.systemDictionaryDelete = params => ajaxDelete({url: `/api/system/dictionary/`,params})
// 字典管理 -- 设置状态
Api.systemDictionarySetStatus = params => ajaxPost({url: `/api/system/dictionary/set_status/`,params})

/**
*系统配置
 * */
// 获取系统配置，无需认证
Api.getSysConfig = params => ajaxGet({url: `/api/system/getconfig/`,params})
// 系统配置
Api.platformsettingsSysconfig = params => ajaxGet({url: `/api/system/sysconfig/`,params})
// 系统配置 -- 新增
Api.platformsettingsSysconfigAdd = params => ajaxPost({url: `/api/system/sysconfig/`,params})
// 系统配置 -- 编辑
Api.platformsettingsSysconfigEdit = params => ajaxPut({url: `/api/system/sysconfig/`,params})
// 系统配置 -- 删除
Api.platformsettingsSysconfigDelete = params => ajaxDelete({url: `/api/system/sysconfig/`,params})
// 系统配置 -- 保存子项
Api.platformsettingsSysconfigSavecontent = params => ajaxPut({url: `/api/system/sysconfig/save_content/`,params})
// 系统配置 -- 获取所有models列表信息
Api.platformsettingsSysconfigGetmodelsInfoList = params => ajaxGet({url: `/api/system/sysconfig/get_models_info_list/`,params})

//消息公告
Api.messagesMessagenotice = params => ajaxGet({url: `/api/system/msg/`,params})
//消息公告-新增
Api.messagesMessagenoticeAdd = params => ajaxPost({url: `/api/system/msg/`,params})
//消息公告-修改
Api.messagesMessagenoticeEdit = params => ajaxPut({url: `/api/system/msg/`,params})
//消息公告-删除
Api.messagesMessagenoticeDelete = params => ajaxDelete({url: `/api/system/msg/`,params})

//我的消息 列表
Api.getOwnMessage = params => ajaxGet({url: `/api/system/msg/ownmsg/`,params})
//我的消息 删除
Api.delOwnMessage = params => ajaxPost({url: `/api/system/msg/delownmsg/`,params})
//我的消息 设置已读
Api.readOwnMessage = params => ajaxPost({url: `/api/system/msg/readownmsg/`,params})

export default Api
