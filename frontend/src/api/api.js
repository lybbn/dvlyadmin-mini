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

/**
 *个人中心
 * */
// 获取当前个人用户信息
Api.systemUserUserInfo= params => ajaxGet({url: `/api/system/user/user_info/`,params})
// 更新修改当前个人用户信息
Api.systemUserUserInfoEdit= params => ajaxPut({url: `/api/system/user/user_info/`,params})
// 用户重置个人密码
Api.systemUserChangePassword= params => ajaxPut({url: `/api/system/user/change_password/`,params})

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

export default Api
