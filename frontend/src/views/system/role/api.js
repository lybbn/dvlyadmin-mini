import {ajaxGet,ajaxPost,ajaxDelete,ajaxPut,ajaxPatch,uploadImg,ajaxGetDetailByID,ajaxDownloadExcel,uploadFileParams,getDownloadFile,downloadFile} from '@/api/request.js';

const api = {}

// 部门管理
api.list = params => ajaxGet({url: `/api/system/role/`,params})
// 部门管理 -- 新增
api.add = params => ajaxPost({url: `/api/system/role/`,params})
// 部门管理 -- 编辑
api.edit = params => ajaxPut({url: `/api/system/role/`,params})
// 部门管理 -- 删除
api.del = params => ajaxDelete({url: `/api/system/role/`,params})
// 部门管理 -- 禁用启用
api.setStatus = params => ajaxPost({url: `/api/system/role/set_status/`,params})

export default api