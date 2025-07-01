/*
 * @Descripttion: 工具集
 * @version: 1.1
 * @LastEditors: lybbn
 * @LastEditTime: 2024/07/13
 * @Program: django-vue-lyadmin mini
 */

import CryptoJS from 'crypto-js'
import appConfig from '@/config'
import Cookies from 'js-cookie'
import useClipboard from 'vue-clipboard3';
const { toClipboard } = useClipboard();
import { MsgError, MsgOk,MsgWarn } from '@/utils/message';
import Api from '@/api/api';

export function safeDelete(obj, key) {
	try {
		if (obj && typeof obj === 'object') {
			delete obj[key]
		}
	} catch (e) {
		console.warn('删除属性失败:', e)
	}
}

//拷贝文字
export const copyText = async function (content) {
    try {
        await toClipboard(content);
        MsgOk('复制成功');
    } catch (e) {
        MsgError('复制失败');
    }
}

//数据拷贝
export const deepClone = function(data){
    if(data){
       return JSON.parse(JSON.stringify(data))
    }
    return data
}

export const autoStorage = {
	set(key, val) {
		//过期时间
		let datetime = 0
		let newVal = val
		//加密
		if(appConfig.LS_ENCRYPTION == "AES"){
			val = crypto.AES.encrypt(JSON.stringify(val), appConfig.LS_ENCRYPTION_KEY)
			newVal = {
				content: val,
				datetime: parseInt(datetime) === 0 ? 0 : new Date().getTime() + parseInt(datetime) * 1000
			}
		}
		
		appConfig.STORAGE_METHOD === "localStorage" ? window.localStorage.setItem(key,newVal):window.sessionStorage.setItem(key,newVal)
	},
	get(key) {
		try {
			const result =  appConfig.STORAGE_METHOD === "localStorage" ? window.localStorage.getItem(key):window.sessionStorage.getItem(key)
			if (result != null) {
				//解密
				if(appConfig.LS_ENCRYPTION == "AES"){
					let nowTime = new Date().getTime()
					if (nowTime > result.datetime && result.datetime != 0) {
						autoStorage.removeItem(key)
						return null;
					}
					result.content = JSON.parse(crypto.AES.decrypt(result.content, appConfig.LS_ENCRYPTION_KEY))
				}
				return result
			}
			return null
		}catch (err) {
            return null
        }
	},
	remove(key) {
        appConfig.STORAGE_METHOD === "localStorage" ? window.localStorage.removeItem(key):window.sessionStorage.removeItem(key)
	},
	clear() {
        appConfig.STORAGE_METHOD === "localStorage" ? window.localStorage.clear():window.sessionStorage.clear()
		Cookies.remove('logintoken');
	},
	clearAll(){
		window.localStorage.clear()
		window.sessionStorage.clear()
	}
}

export const getToken = function(key = 'logintoken') {
	//return Cookies.get(key)
    return autoStorage.get(key)
}

export const setToken = function(key='logintoken',val) {
	//Cookies.set(key, val,{ sameSite: 'None', secure: true })
    return autoStorage.set(key,val)
}

export const getRereshToken = function(key = 'refreshtoken') {
	//return Cookies.get(key)
    return autoStorage.get(key)
}

export const setRefreshToken = function(key='refreshtoken',val) {
	//Cookies.set(key, val,{ sameSite: 'None', secure: true })
    return autoStorage.set(key,val)
}

export const Local = {
    // 设置永久缓存
	set(key, val) {
		window.localStorage.setItem(key, JSON.stringify(val));
	},
	// 获取永久缓存
	get(key) {
		let json = window.localStorage.getItem(key);
		return JSON.parse(json);
	},
	// 移除永久缓存
	remove(key) {
		window.localStorage.removeItem(key);
	},
	// 移除全部永久缓存
	clear() {
		window.localStorage.clear();
	},
}

export const Session = {
    // 设置临时缓存
	set(key, val) {
		window.sessionStorage.setItem(key, JSON.stringify(val));
	},
	// 获取临时缓存
	get(key) {
		let json = window.sessionStorage.getItem(key);
		return JSON.parse(json);
	},
	// 移除临时缓存
	remove(key) {
		window.sessionStorage.removeItem(key);
	},
	// 移除全部临时缓存
	clear() {
		window.sessionStorage.clear();
	},
}

export const dateFormat = function (date, fmt='yyyy-MM-dd hh:mm:ss') {
	date = new Date(date)
	var o = {
		"M+" : date.getMonth()+1,                 //月份
		"d+" : date.getDate(),                    //日
		"h+" : date.getHours(),                   //小时
		"m+" : date.getMinutes(),                 //分
		"s+" : date.getSeconds(),                 //秒
		"q+" : Math.floor((date.getMonth()+3)/3), //季度
		"S"  : date.getMilliseconds()             //毫秒
	};
	if(/(y+)/.test(fmt)) {
		fmt=fmt.replace(RegExp.$1, (date.getFullYear()+"").substr(4 - RegExp.$1.length));
	}
	for(var k in o) {
		if(new RegExp("("+ k +")").test(fmt)){
			fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
		}
	}
	return fmt;
}

export const crypto = {
	//MD5加密
	MD5(data){
		return CryptoJS.MD5(data).toString()
	},
	//BASE64加解密
	BASE64: {
		encrypt(data){
			return CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(data))
		},
		decrypt(cipher){
			return CryptoJS.enc.Base64.parse(cipher).toString(CryptoJS.enc.Utf8)
		}
	},
	//AES加解密
	AES: {
		encrypt(data, secretKey, config={}){
			if(secretKey.length % 8 != 0){
				console.warn("[lybbn error]: 秘钥长度需为8的倍数，否则解密将会失败。")
			}
			const result = CryptoJS.AES.encrypt(data, CryptoJS.enc.Utf8.parse(secretKey), {
				iv: CryptoJS.enc.Utf8.parse(config.iv || ""),
				mode: CryptoJS.mode[config.mode || "ECB"],
				padding: CryptoJS.pad[config.padding || "Pkcs7"]
			})
			return result.toString()
		},
		decrypt(cipher, secretKey, config={}){
			const result = CryptoJS.AES.decrypt(cipher, CryptoJS.enc.Utf8.parse(secretKey), {
				iv: CryptoJS.enc.Utf8.parse(config.iv || ""),
				mode: CryptoJS.mode[config.mode || "ECB"],
				padding: CryptoJS.pad[config.padding || "Pkcs7"]
			})
			return CryptoJS.enc.Utf8.stringify(result);
		}
	}
}

export const fullScreen = function (element) {
	var isFull = !!(document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || document.fullscreenElement);
	if(isFull){
		if(document.exitFullscreen) {
			document.exitFullscreen();
		}else if (document.msExitFullscreen) {
			document.msExitFullscreen();
		}else if (document.mozCancelFullScreen) {
			document.mozCancelFullScreen();
		}else if (document.webkitExitFullscreen) {
			document.webkitExitFullscreen();
		}
	}else{
		if(element.requestFullscreen) {
			element.requestFullscreen();
		}else if(element.msRequestFullscreen) {
			element.msRequestFullscreen();
		}else if(element.mozRequestFullScreen) {
			element.mozRequestFullScreen();
		}else if(element.webkitRequestFullscreen) {
			element.webkitRequestFullscreen();
		}
	}
}

//检查是否为IP
export const checkIsIp = function(rule,value,callback){
    if (value === '' || typeof value === 'undefined' || value == null) {
		let required = rule.required
		if(!required){
			callback();
		}
        callback(new Error("请输入IP"));
    } else {
        const reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
        if (!reg.test(value) && value !== '') {
            callback(new Error("请输入正确IP"));
        } else {
            callback();
        }
    }
}

//检查是否为IPv4 子网
export const checkIsIpv4Subnet = function(rule,value,callback){
    if (value === '' || typeof value === 'undefined' || value == null) {
		let required = rule.required
		if(!required){
			callback();
		}
        callback(new Error("请输入子网"));
    } else {
        const reg = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\/(3[0-2]|[12]?[0-9]))$/;
        if (!reg.test(value) && value !== '') {
            callback(new Error("请输入正确ipv4网段"));
        } else {
            callback();
        }
    }
}

//检查是否为有效容器 镜像名:标签 形式（镜像名必须）
export const checkIsDockerImageAndTag = function(rule,value,callback){
    if (value === '' || typeof value === 'undefined' || value == null) {
		let required = rule.required
		if(!required){
			callback();
		}
        callback(new Error("请输入必填项，如：mysql:latest"));
    } else {
        const reg = /^[a-zA-Z0-9@:/\.-_,]{1,200}(?::[a-zA-Z0-9@:/\.-_,]{1,200})?$/;
        if (!reg.test(value) && value !== '') {
            callback(new Error("格式错误：支持字母、数字、@:/.-_ 且长度1-200"));
        } else {
            callback();
        }
    }
}

//触发全屏
//element this.$refs.xxx  需要全屏的元素
export const triggerFullScreen =function(element) {
	if (element.requestFullscreen) {
		element.requestFullscreen();
	} else if (element.mozRequestFullScreen) {
		element.mozRequestFullScreen();
	} else if (element.webkitRequestFullscreen) {
		element.webkitRequestFullscreen();
	} else if (element.msRequestFullscreen) {
		element.msRequestFullscreen();
	}
	// window.dispatchEvent(new Event('resize'))
}

// 退出全屏
export const exitFullScreen=function(element) {
	if (element == undefined) {
		element = document.documentElement;
	}
	var exitMethod = document.exitFullscreen || document.mozCancelFullScreen || document.webkitExitFullscreen;
	if (exitMethod) {
		exitMethod.call(document);
	} else if (typeof window.ActiveXObject !== "undefined") { //IE
		var wscript = new ActiveXObject("WScript.Shell");
		!!wscript && wscript.SendKeys("{F11}");
	}
	// window.dispatchEvent(new Event('resize'))
}

//字节转换，到指定单位结束 is_unit：是否显示单位  fixed：小数点位置 end_unit：结束单位
export const formatUnitSize = function (bytes, is_unit = true, fixed = 2, end_unit = '') {
    if (bytes === undefined) return 0;

    bytes = typeof bytes === 'string' ? parseInt(bytes) : bytes;
    
    const unit = [' B', ' KB', ' MB', ' GB', 'TB'];
    const divisor = 1024;

    for (let i = 0; i < unit.length; i++) {
        if ((end_unit && unit[i].trim() === end_unit.trim()) || (!end_unit && bytes < divisor)) {
            const val = i === 0 ? bytes : (fixed === 0 ? bytes : bytes.toFixed(fixed));
            return is_unit ? val + unit[i] : parseFloat(val);
        }
        bytes /= divisor;
    }
};

export const downloadFileContent = function (content, fileName) {
    const downloadUrl = window.URL.createObjectURL(new Blob([content]));
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = downloadUrl;
    a.download = fileName;
    const event = new MouseEvent('click');
    a.dispatchEvent(event);
}

export const getDownloadFile = function (fileName) {
	Api.sysFileGetToken({filename:fileName}).then(res => {
		if (res.code == 2000) {
			let params = res.data
			Api.downloadFile(params)
		} else {
			MsgWarn(res.msg)
		}
	})
}

export const addCopySuffix = function (name) {
	const parts = name.split('.');
	if (parts.length > 1) {
	  	// 如果有扩展名，则在扩展名之前加上'-副本'
	  	return parts.slice(0, -1).join('.') + '-副本.' + parts[parts.length - 1];
	} else {
	  	// 如果没有扩展名，则在最后加上'-副本'
	  	return name + '-副本';
	}
}

export const getFileExt = function (fileName) {
	// 从文件名中获取扩展名
	const lastDotIndex = fileName.lastIndexOf('.');
	if (lastDotIndex === -1) {
		// 如果没有找到点，返回空字符串或其他默认值
		return '';
	} else {
		// 使用 substring 方法获取最后一个点之后的部分作为扩展名
		return fileName.substring(lastDotIndex + 1).toLowerCase();
	}
}

// 生成指定长度随机字符串
export const generateRandomString = function (length) {
	const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	let result = '';
	for (let i = 0; i < length; i++) {
	  const randomIndex = Math.floor(Math.random() * characters.length);
	  result += characters.charAt(randomIndex);
	}
	return result;
}

// 获取路径中的文件名，如果为目录则获取目录名
export const getFileNameFromPath = function(path) {
	const isWindowsPath = /^[A-Za-z]:\//.test(path);
	if(isWindowsPath){
		if(path.length>3){
			path = path.replace(/\/$/, '');
		}else{
			return ""
		}
	}else{
		if(path.length>1){
			path = path.replace(/\/$/, '');
		}
		if(path === "/"){
			return ""
		}
	}
    // 使用 split('/') 将路径按照斜杠分割成数组，并取最后一个元素作为文件名
    const parts = path.split('/');
    return parts[parts.length - 1];
}


// 获取assets静态资源
export const getAssetsFile = (fileName="",forder=null) => {
	const path = forder?`/src/assets/lybbn/imgs/${forder}/${fileName}`:`/src/assets/lybbn/imgs/${fileName}`
	const modules = import.meta.glob(`@/assets/lybbn/imgs/**/*.{png,svg,jpg,jpeg}`, { eager: true });
	if (modules[path]) return modules[path].default;
	else {
	  // 地址错误
	  //console.error("Error url is wrong path");
	}
};

export const formatSecondsTime = (seconds) =>{
	if (seconds < 60) {
	  return `${seconds}秒`;
	} else if (seconds < 3600) {
	  const mins = Math.floor(seconds / 60);
	  const secs = seconds % 60;
	  return `${mins}分钟${secs}秒`;
	} else {
	  const hours = Math.floor(seconds / 3600);
	  const mins = Math.floor((seconds % 3600) / 60);
	  const secs = seconds % 60;
	  return `${hours}小时${mins}分钟${secs}秒`;
	}
}

export const UnitsTime = [
    { label: "秒", value: 's' },
    { label: "分钟", value: 'm' },
    { label: "小时", value: 'h' },
    { label: "天", value: 'd' },
    { label: "周", value: 'w' },
    { label: "月", value: 'M' },
    { label: "年", value: 'y' },
];

//数据拷贝
export const isEmpty = function(value){
    // 如果值是 null 或 undefined，直接返回 true
	if (value === null || value === undefined) {
		return true;
	}

	// 如果值是字符串，判断是否为空字符串
	if (typeof value === 'string' && value.trim() === '') {
		return true;
	}

	// 如果值是数组，判断是否为空数组
	if (Array.isArray(value) && value.length === 0) {
		return true;
	}

	// 如果值是对象，判断是否为空对象
	if (typeof value === 'object' && Object.keys(value).length === 0) {
		return true;
	}

	// 对于其他类型，返回 false，表示不为空
	return false;
}

export function isNumber(value) {
	return typeof value === 'number' && !isNaN(value);
}

export function formatTimestampDatetime(timestamp) {
	if (!timestamp) {
	  return '';  // 如果时间为空，返回空字符串
	}
	if (!isNumber(timestamp)){
		return timestamp
	}
	if (timestamp < 1000000000000) {
		timestamp = timestamp * 1000;
	}
	const date = new Date(timestamp);
	
	const year = date.getFullYear();
	const month = ('0' + (date.getMonth() + 1)).slice(-2); // 月份是从0开始的，所以加1
	const day = ('0' + date.getDate()).slice(-2);
	const hour = ('0' + date.getHours()).slice(-2);
	const minute = ('0' + date.getMinutes()).slice(-2);
	const second = ('0' + date.getSeconds()).slice(-2);

	return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

export function formatTimestampDate(timestamp) {
	if (!timestamp) {
	  return '';  // 如果时间为空，返回空字符串
	}
	if (!isNumber(timestamp)){
		return timestamp
	}
	if (timestamp < 1000000000000) {
		timestamp = timestamp * 1000;
	}
	const date = new Date(timestamp);
	
	const year = date.getFullYear();
	const month = ('0' + (date.getMonth() + 1)).slice(-2); // 月份是从0开始的，所以加1
	const day = ('0' + date.getDate()).slice(-2);
	const hour = ('0' + date.getHours()).slice(-2);
	const minute = ('0' + date.getMinutes()).slice(-2);
	const second = ('0' + date.getSeconds()).slice(-2);

	return `${year}-${month}-${day}`;
}

export function convertToBeijingTime(utcString) {
	if(!utcString){return utcString}
	const utcDate = new Date(utcString);

	// 获取 UTC 时间的各个部分
	const year = utcDate.getUTCFullYear();
	const month = utcDate.getUTCMonth();
	const date = utcDate.getUTCDate();
	const hours = utcDate.getUTCHours();
	const minutes = utcDate.getUTCMinutes();
	const seconds = utcDate.getUTCSeconds();

	// 将 UTC 时间转换为北京时间（加 8 小时）
	const beijingDate = new Date(Date.UTC(year, month, date, hours + 8, minutes, seconds));

	// 格式化为 'YYYY-MM-DD HH:mm:ss' 格式
	const formattedDate = beijingDate.toISOString().slice(0, 19).replace('T', ' ');

	return formattedDate;
}

export function isNull(value) {
	return (value === null) || (value === undefined);
}

export function getTableHeight(tableSelectHeight,allowPage=true){
    var pagination_height = allowPage?176:0;
    let height = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - tableSelectHeight;
    var ua = navigator.userAgent;
    //获取当前设备类型（安卓或苹果）
    if (ua && /Android/.test(ua)) {
        return 700
    }
    else if (ua && /iPhone|ipad|ipod|ios/.test(ua)){
        return 700
    }
    else {
        return height - pagination_height
    }
}

/**
 * 从响应头解析文件名（兼容 RFC 5987 和传统格式）
 */
export function extractFilenameFromHeaders(headers) {
	const disposition = headers['content-disposition'];
	if (!disposition) return null;

	// 1. 匹配 RFC 5987 格式（现代浏览器）：filename*=UTF-8''中文名.xlsx
	const utf8Filename = disposition.match(/filename\*=UTF-8''([^;]+)/i);
	if (utf8Filename) {
		return decodeURIComponent(utf8Filename[1]);
	}

	// 2. 匹配传统格式：filename="%E4%B8%AD%E6%96%87.xlsx"
	const legacyFilename = disposition.match(/filename="([^"]+)"/i);
	if (legacyFilename) {
		return decodeURIComponent(legacyFilename[1]);
	}

	// 3. 无引号格式：filename=%E4%B8%AD%E6%96%87.xlsx
	const rawFilename = disposition.match(/filename=([^;]+)/i);
	if (rawFilename) {
		return decodeURIComponent(rawFilename[1].trim());
	}

	return null;
}