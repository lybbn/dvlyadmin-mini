import axios from 'axios';
import { ElMessage,ElMessageBox } from 'element-plus'
import {getToken,autoStorage,getRereshToken,setToken,setRefreshToken} from '@/utils/util'
import sysConfig from "@/config"
import { useUserState } from "@/store/userState";
import { cancelRequestState } from "@/store/cancelRequest";

let API_BASE_URL = sysConfig.API_URL

// 当前是生产环境
if (import.meta.env.PROD) {
    // 获取浏览器地址
    API_BASE_URL = window.location.origin;
}

var request = axios.create({
    timeout: sysConfig.TIMEOUT,
});

request.interceptors.request.use(config => {
    const cancelRequest = cancelRequestState()
	config.cancelToken = new axios.CancelToken(cancel => {
    	cancelRequest.addCancelToken(cancel)
  	})
    return config
})

// http response 拦截器
request.interceptors.response.use(
    async (response) => {
        if (response.data.code === 4001 || response.data.code === 401) {
            try {
                const refreshToken = getRereshToken()
                const refreshResponse = await axios.post(API_BASE_URL+'/api/token/refresh/', {
                    refresh: refreshToken,
                });
                if(refreshResponse.data.hasOwnProperty("code") && refreshResponse.data.code === 4001){
                    ElMessageBox.alert('登录信息失效,请重新登录！','登录失效',{
                        confirmButtonText:'确定',
                        type: 'warning',
                        callback: action => {
                            //跳转登录页   callback点击确定按钮后的回调函数
                            autoStorage.clear()
                            ElMessage.success('已退出登录!')
                            window.location.href="/"
                        }
                    })
                }else{
                    // 刷新成功，将新的 Access Token 存储起来
                    setToken('logintoken', refreshResponse.data.access)
                    setRefreshToken('refreshtoken',refreshResponse.data.refresh)
                    response.data.msg = "已自动刷新登录信息"
                }
                return response
            } catch (refreshError) {
                console.error('Failed to refresh access token:', refreshError);
                // 刷新 Token 失败，可能是 Refresh Token 过期了,需要重新登录
                ElMessageBox.alert('登录信息失效,请重新登录！','登录失效',{
                    confirmButtonText:'确定',
                    type: 'warning',
                    callback: action => {
                        //跳转登录页   callback点击确定按钮后的回调函数
                        autoStorage.clear()
                        ElMessage.success('已退出登录!')
                        window.location.href="/"
                    }
                })
                return response
            }
        }
        else{
            return response
        }
    },
    error => {
        const userState = useUserState()
        if(error.response && error.response.status == 404){
            if (import.meta.env.PROD) {
                window.location.href="/404"
                return
            }
        }else if (error.message == "canceled") {
			return new Promise(() => {})
		}
        else if (error.message.indexOf('timeout') != -1) {
			ElMessage.error('网络超时');
		}else if (error.message == 'Network Error') {
            if(error.config.data == '{"action":"restart","type":"panel"}'){
                return new Promise(() => {})
            }else if(error.config.data == '{"action":"restart","type":"server"}'){
                return new Promise(() => {})
            }
			ElMessage.error('网络连接错误');
		}else {
			if (error.response &&error.response.data){
                ElMessage.error(error.response.statusText);
            } 
			else{
                ElMessage.error('接口路径找不到')
            } 
		}
        userState.loadingInfo.isLoading = false
        userState.loadingInfo.content = ""
		return Promise.reject(error);
	}
)

function ajax(opt,method){
  var token= getToken()
  // var timestamp=new Date().getTime();
  var params;

  if(opt.params){
    //对传入的参数进行深拷贝，防止传入的参数对象被页面上其他逻辑改变，导致签名错误
    if (Object.prototype.toString.call(opt.params) != '[object FormData]') {
      // 不是formdata类型
      params = JSON.parse(JSON.stringify(opt.params));
    }else{//formdata类型
      params= opt.params
    }
    if(method=='GET') {
      params={
        ...params,
        // 't':timestamp
      }
    }
  }else{
    params={}
  }

  if(method == 'PUT' || method == 'DELETE') {
      var config={
          url: API_BASE_URL + opt.url + params.id+'/',
          method: method,
          headers:{
              Authorization: sysConfig.TOKEN_PREFIX + token,
          }
      }
      if(!params.id){
          config={
            url: API_BASE_URL + opt.url,
            method: method,
            headers:{
                Authorization: sysConfig.TOKEN_PREFIX + token,
            }
        }
      }

      method==="PUT"&&(config.params=params);
      return new Promise((resolve,reject)=>{
          request({
                url: config.url,
                method: method,
                headers:{
                    Authorization: sysConfig.TOKEN_PREFIX + token,
                },
                data: params
              }).then(res=>{
                resolve(res.data)
          }).catch(res=>{
              reject(res)
          })
      })
  }else if(method == 'GET2'){
      var config2={
          url: API_BASE_URL + opt.url + params.id+'/',
          method: 'GET',
          headers:{
              Authorization: sysConfig.TOKEN_PREFIX + token,
          }
      }
      if(!params.id){
          config2={
              url: API_BASE_URL + opt.url,
              method: 'GET',
              headers:{
                  Authorization: sysConfig.TOKEN_PREFIX + token,
              }
          }
      }
      return new Promise((resolve,reject)=>{
          // console.log(config,'config')
          request({
              url: config2.url,
              method: 'GET',
              headers:{
                  Authorization: sysConfig.TOKEN_PREFIX + token,
              },
              data: params
          }).then(res=>{
              resolve(res.data)
          }).catch(res=>{
              reject(res)
          })
      })
  }
  else if(method == 'excel'){
      var config3={
          url: API_BASE_URL + opt.url,
          method: 'POST',
          headers:{
              Authorization: sysConfig.TOKEN_PREFIX + token,
          },
          responseType:  'blob', //此属性非常重要，不然数据是乱码
      }
      config3.data=params
      return new Promise((resolve,reject)=>{
          request(config3).then(res=>{
              resolve(res)
          }).catch(res=>{
              resolve(res)
          })
      })
  }
  else {
      var config1={
          url: API_BASE_URL + opt.url,
          method: method,
          headers:{
              Authorization: sysConfig.TOKEN_PREFIX + token,
          }
      }
      method==="GET"&&(config1.params=params);
      method==="POST"&&(config1.data=params);
      method==="PATCH"&&(config1.data=params);
      return new Promise((resolve,reject)=>{
          request(config1).then(res=>{
              resolve(res.data)
          }).catch(res=>{
              reject(res)
          })
      })
  }
}



export function ajaxGet (opt) {
    return ajax(opt,"GET")
}
export function ajaxPut (opt) {
    return ajax(opt,"PUT")
}
export function ajaxDelete (opt) {
    return ajax(opt,"DELETE")
}
export function ajaxPost (opt) {
  return ajax(opt,"POST")
}
export function ajaxPatch (opt) {
  return ajax(opt,"PATCH")
}
// 单例详情获取get /api/test/12xxxxxxxx/
export function ajaxGetDetailByID (opt) {
    return ajax(opt,"GET2")
}
// 下载excel文件流（blob）
export function ajaxDownloadExcel (opt) {
    return ajax(opt,"excel")
}

//websocket获取jwt请求token
export function getJWTAuthorization() {
    var token= getToken()
    var jwt = 'JWTlybbn' + token
    return jwt
}

export function downloadFile (param) {
    let token= getToken()
    return axios({
        method: "post",
        url: API_BASE_URL+param.url,
        headers: {
            Authorization: 'JWT ' + token,
        },
        data:JSON.parse(JSON.stringify(param.params)),
        responseType: 'blob'
    }).then(res => res);
}

export function getDownloadFile (param) {
    const urlParams = new URLSearchParams(param.params);
    let url = API_BASE_URL + param.url;
    url += '?' + urlParams.toString()
    window.location.href = url
}

// 上传图片
export function uploadImg (param) {
    let formData = new FormData()
    formData.append('file', param.params.file)
    let token= getToken()
    return axios({
        method: 'post',
        url: API_BASE_URL+param.url ,
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: sysConfig.TOKEN_PREFIX + token,
        },
        data:formData,
        onUploadProgress: progressEvent => {
            // progressEvent.loaded:已上传文件大小
            // progressEvent.total:被上传文件的总大小
            let loadProgress = (progressEvent.loaded / progressEvent.total * 100)
            if(param.params.onProgress){
                param.params.onProgress({percent: loadProgress})
            }
            // console.info(progressEvent.loaded)
            // console.info(progressEvent.total)
          }
    }).then(res => res.data);
}

export function uploadFile (param,onProgress) {
    const token= getToken()
    return new Promise((resolve, reject) => {
        axios({
            method: 'post',
            url: API_BASE_URL+param.url ,
            headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: sysConfig.TOKEN_PREFIX + token,
            },
            data:param.formData,
            onUploadProgress: (progressEvent) => {
                if (onProgress) {
                    onProgress(progressEvent);
                }
            },
        })
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        });
    });
}

export function uploadFileParams (param,onProgress) {
    const token= getToken()
    return new Promise((resolve, reject) => {
        axios({
            method: 'post',
            url: API_BASE_URL+param.url ,
            headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: sysConfig.TOKEN_PREFIX + token,
            },
            data:param.params.formData,
            onUploadProgress: (progressEvent) => {
                if (onProgress) {
                    onProgress(progressEvent);
                }
            },
        })
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        });
    });
}