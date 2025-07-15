<template>
	<el-form ref="loginFormRef" :model="formData" :rules="rules" label-width="0" size="large" @keyup.enter="submitLogin" :disabled="islogining">
		<el-form-item prop="username">
			<el-input v-model="formData.username" prefix-icon="user" clearable placeholder="请输入用户名">
			</el-input>
		</el-form-item>
		<el-form-item prop="password">
			<el-input v-model="formData.password" prefix-icon="lock" clearable show-password placeholder="请输入密码"></el-input>
		</el-form-item>
		<el-form-item prop="captcha">
            <el-input type="text" prefix-icon="circle-check" v-model.trim="formData.captcha" auto-complete="off" placeholder="验证码">
                  <template #append>
                    <ly-img class="login-captcha" :src="image_base" @click="getCaptchas" />
                  </template>
            </el-input>
          </el-form-item>
		<el-form-item>
			<el-button type="primary" class="login-btn" style="width: 100%;" :loading="islogining" round @click="submitLogin">注册</el-button>
		</el-form-item>
	</el-form>
</template>

<script setup>
	import {ref, onMounted,watch,computed ,nextTick} from 'vue'
	import {autoStorage,setToken,setRefreshToken} from '@/utils/util'
	import { ElMessage } from 'element-plus'
	import { useRouter,useRoute } from 'vue-router'
	import Api from "@/api/api"
	import sysConfig from "@/config"
	import {useUserState} from "@/store/userState";

	const userState = useUserState()

	// let API_BASE_URL = sysConfig.API_URL

	// // 当前是生产环境
	// if (import.meta.env.PROD) {
	// 	// 获取浏览器地址
	// 	API_BASE_URL = window.location.origin;
	// }
	const API_BASE_URL = window.location.origin

	const router = useRouter()

	let formData = ref({
		username: "",
		password: "",
		captcha: "",
		captchaKey: null,
	})
	let image_base = ref(null)
	let rules = ref({
		username: [
			{required: true, message: "请输入账号", trigger: 'blur'}
		],
		password: [
			{required: true, message: "请输入密码", trigger: 'blur'}
		],
		captcha: [
			{required: true, message: "请输入验证码", trigger: 'blur'}
		],
	})
	let islogining = ref(false)

	/**
	* 获取验证码
	*/
	function getCaptchas () {
		Api.getCaptcha().then((res) => {
			if(res.code == 2000){
				formData.value.captcha = null
				formData.value.captchaKey = res.data.key
				image_base.value = res.data.image_base
			}else{
				ElMessage.error(res.msg)
			}
		})
	}

	let loginFormRef = ref(null)

	// function submitLogin() {
	// 	islogining.value = true
	// 	loginFormRef.value.validate(obj=>{
    //         if(obj) {
    //             Api.getToken(formData.value).then(res => {
	// 				islogining.value = false
	// 				if (res.code === 2000) {
	// 					setToken('logintoken',res.data.access)
	// 					setRefreshToken('refreshtoken',res.data.refresh)
	// 					userState.userInfo.username = formData.value.username
	// 					loginSuccess()
	// 				} else {
	// 					getCaptchas()
	// 					ElMessage.error(res.msg)
	// 				}
	// 			})
                
    //         }
	// 		islogining.value = false
    //     })
	// }

	const submitLogin = async () => {
		if (islogining.value) return; // 防止重复提交

		try {
			islogining.value = true; // 开启加载状态

			// 1. 表单验证
			await loginFormRef.value.validate();

			// 2. 调用登录接口（重点修改部分）
			const res = await Api.getToken(formData.value);
    
			if (res.code === 2000) {
				// 3. 登录成功处理
				setToken('logintoken', res.data.access);
				setRefreshToken('refreshtoken', res.data.refresh);
				userState.userInfo.username = formData.value.username;
				loginSuccess(); // 执行跳转等操作
				ElMessage.success('登录成功');
			} else {
				// 4. 登录失败（服务端返回错误）
				ElMessage.error(res.msg || '登录失败');
				getCaptchas(); // 刷新验证码
			}

		} catch (error) {
			// 区分验证失败和请求失败
			if (error.fields) {
				ElMessage.warning('请填写正确的登录信息');
			} else {
				ElMessage.error('登录失败，请重试');
			}
		} finally {
			islogining.value = false; // 关闭加载状态
		}
	}

	function loginSuccess(){
		// router.push('/');
		window.location.href = API_BASE_URL+"/#/"
	}

	onMounted(()=>{
		//请求数据
		getCaptchas()
	})

</script>

<style scoped>
	.login-captcha{
		cursor: pointer;
		height: 38px;
		width: 128px;
		display: block;
		margin: 0px -19px;
		border-top-right-radius: 2px;
		border-bottom-right-radius: 2px;
	}
	.login-btn{
		margin-top: 10px;
	}
</style>