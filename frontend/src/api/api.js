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

export default Api
