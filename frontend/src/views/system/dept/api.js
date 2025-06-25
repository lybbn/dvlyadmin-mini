import {ajaxGet,ajaxPost,ajaxDelete,ajaxPut,ajaxPatch,uploadImg,ajaxGetDetailByID,ajaxDownloadExcel,uploadFileParams,getDownloadFile,downloadFile} from '@/api/request.js';

const api = {}

// 部门管理
api.list = params => ajaxGet({url: `/api/system/dept/`,params})
// 部门管理 -- 新增
api.add = params => ajaxPost({url: `/api/system/dept/`,params})
// 部门管理 -- 编辑
api.edit = params => ajaxPut({url: `/api/system/dept/`,params})
// 部门管理 -- 删除
api.del = params => ajaxDelete({url: `/api/system/dept/`,params})
// 部门管理 -- 禁用启用
api.setStatus = params => ajaxPost({url: `/api/system/dept/set_status/`,params})
// 部门管理 -- 导出
api.export = (queryParams,params) => ajaxDownloadExcel({url: `/api/system/dept/export_data/`,queryParams:queryParams,params})
// 部门管理 -- 导入
api.import = params => uploadFileParams({url: `/api/system/dept/import_data/`,params})
// 部门管理 -- 下载导入模板
api.downloadTemplate = params => downloadFile({url: `/api/system/dept/download_template/`,params})

export default api