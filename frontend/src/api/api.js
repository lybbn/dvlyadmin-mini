import {ajaxGet,ajaxPost,ajaxDelete,ajaxPut,ajaxPatch,uploadImg,ajaxGetDetailByID,ajaxDownloadExcel,uploadFileParams,getDownloadFile,downloadFile} from './request';

const Api = {}
// 获取验证码
Api.getCaptcha = params => ajaxGet({url: `/api/captcha/`,params})
// 登录
Api.getToken = params => ajaxPost({url: `/api/token/`,params})
// 刷新登录token
Api.refreshToken = params => ajaxPost({url: `/api/token/refresh/`,params})

/**
 *个人中心
 * */
// 获取当前个人用户信息
Api.systemUserUserInfo= params => ajaxGet({url: `/api/system/user/user_info/`,params})
// 更新修改当前个人用户信息
Api.systemUserUserInfoEdit= params => ajaxPut({url: `/api/system/user/user_info/`,params})
// 用户重置个人密码
Api.systemUserChangePassword= params => ajaxPut({url: `/api/system/user/change_password/`,params})

export default Api
