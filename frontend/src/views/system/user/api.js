import {ajaxGet,ajaxPost,ajaxDelete,ajaxPut,ajaxPatch,uploadImg,ajaxGetDetailByID,ajaxDownloadExcel,uploadFileParams,getDownloadFile,downloadFile} from '@/api/request.js';
import Api from "@/api/api.js"
const api = {}

// 用户管理
api.list = Api.apiSystemUser
// 用户管理 -- 新增
api.add = params => ajaxPost({url: `/api/system/user/`,params})
// 用户管理 -- 编辑
api.edit = params => ajaxPut({url: `/api/system/user/`,params})
// 用户管理 -- 删除
api.del = params => ajaxDelete({url: `/api/system/user/`,params})
// 用户管理 -- 禁用启用
api.setStatus = params => ajaxPost({url: `/api/system/user/set_status/`,params})
// 用户管理 -- 导出
api.export = (queryParams,params) => ajaxDownloadExcel({url: `/api/system/user/export_data/`,queryParams:queryParams,params})
// 用户管理 -- 导入
api.import = params => uploadFileParams({url: `/api/system/user/import_data/`,params})
// 用户管理 -- 下载导入模板
api.downloadTemplate = params => downloadFile({url: `/api/system/user/download_template/`,params})
// 用户管理 -- 编辑
api.resetPass = params => ajaxPut({url: `/api/system/user/reset_password/`,params})

export default api