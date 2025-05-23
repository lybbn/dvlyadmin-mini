import {ajaxGet,ajaxPost,ajaxDelete,ajaxPut,ajaxPatch,uploadImg,ajaxGetDetailByID,ajaxDownloadExcel,uploadFileParams,getDownloadFile,downloadFile} from './request';

const Api = {}
// 获取验证码
Api.getCaptcha = params => ajaxGet({url: `/api/captcha/`,params})
// 登录
Api.getToken = params => ajaxPost({url: `/api/token/`,params})
// 刷新登录token
Api.refreshToken = params => ajaxPost({url: `/api/token/refresh/`,params})

export default Api
