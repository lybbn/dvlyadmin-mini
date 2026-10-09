<template>
	<el-form ref="loginFormRef" :model="formData" :rules="rules" label-width="0" size="large" @keyup.enter="submitLogin" :disabled="islogining">
		<div class="login-heading">
			<p class="login-kicker">DVLYADMIN MINI</p>
			<h2>用户登录</h2>
			<p class="login-description">请输入账号信息以继续</p>
		</div>
		<el-form-item prop="username">
			<el-input v-model="formData.username" prefix-icon="user" clearable placeholder="请输入用户名">
			</el-input>
		</el-form-item>
		<el-form-item prop="password">
			<el-input v-model="formData.password" prefix-icon="lock" clearable show-password placeholder="请输入密码"></el-input>
		</el-form-item>
		<el-form-item prop="captcha" v-if="userState.sysConfig.loginCaptcha">
			<div class="captcha-row">
				<el-input type="text" prefix-icon="circle-check" v-model.trim="formData.captcha" auto-complete="off" placeholder="验证码" class="captcha-input"></el-input>
				<div class="captcha-box" @click="getCaptchas" title="看不清？点击刷新">
					<ly-img class="captcha-img" :src="image_base" />
					<div class="captcha-mask"><el-icon><Refresh /></el-icon></div>
				</div>
			</div>
		</el-form-item>
		<el-form-item>
			<el-button type="primary" class="login-btn" style="width: 100%;" :loading="islogining" round @click="submitLogin">登录</el-button>
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
	import { useTabsStore } from '@/store/tabs'

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
		]
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

	const submitLogin = async () => {
		if (islogining.value) return; // 防止重复提交

		try {
			islogining.value = true; // 开启加载状态

			// 1. 表单验证
			await loginFormRef.value.validate();

			// 2. 调用登录接口（重点修改部分）
			const res = await Api.getToken(formData.value);
    
			if (res.code === 2000) {
				islogining.value = true
				// 3. 登录成功处理
				setToken('logintoken', res.data.access);
				setRefreshToken('refreshtoken', res.data.refresh);
				await userState.getSystemWebRouter(router)
				loginSuccess(); // 执行跳转等操作
				ElMessage.success('登录成功');

				islogining.value = false
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

	function getCacheActiveTab(){
		let tabsStore = useTabsStore()
		return tabsStore.activeTab
	}

	function loginSuccess(){
		let firstpath = getCacheActiveTab()
		if(!firstpath){
			window.location.href = API_BASE_URL+"/#/"
		}else{
			router.push(firstpath);
		}
		
	}

	onMounted(()=>{
		//请求数据
		getCaptchas()
	})

</script>

<style scoped>
	/* 输入框沿用 v4 玻璃表面与语义色，聚焦时以主色描边。 */
	.login-heading {
		margin: 0 0 24px;
	}
	.login-kicker {
		margin: 0 0 9px;
		color: var(--ly-color-primary);
		font-size: 10px;
		font-weight: 700;
		letter-spacing: 1.2px;
		line-height: 1.4;
	}
	.login-heading h2 {
		margin: 0;
		color: var(--ly-text-1);
		font-size: 27px;
		font-weight: 700;
		letter-spacing: 0.02em;
		line-height: 1.35;
	}
	.login-description {
		margin: 7px 0 0;
		color: var(--ly-text-2);
		font-size: 13px;
		line-height: 1.6;
	}
	@media (max-width: 760px) {
		.login-heading {
			margin-bottom: 20px;
		}
		.login-heading h2 {
			font-size: 24px;
		}
	}
	.el-form :deep(.el-form-item) {
		display: block;
		margin-bottom: 18px;
	}
	.el-form :deep(.el-form-item:has([placeholder="请输入用户名"])::before),
	.el-form :deep(.el-form-item:has([placeholder="请输入密码"])::before),
	.el-form :deep(.el-form-item:has(.captcha-row)::before) {
		display: block;
		margin-bottom: 8px;
		color: var(--ly-text-2);
		font-size: 13px;
		font-weight: 600;
		line-height: 1.4;
	}
	.el-form :deep(.el-form-item:has([placeholder="请输入用户名"])::before) {
		content: '账号';
	}
	.el-form :deep(.el-form-item:has([placeholder="请输入密码"])::before) {
		content: '密码';
	}
	.el-form :deep(.el-form-item:has(.captcha-row)::before) {
		content: '验证码';
	}
	.el-form :deep(.el-input__wrapper) {
		min-height: 50px;
		padding: 0 15px;
		border-radius: 14px;
		background: var(--ly-glass-bg-soft);
		box-shadow: inset 0 0 0 1px var(--ly-line-soft);
		transition: background var(--ly-duration-fast) ease, box-shadow var(--ly-duration-fast) ease;
	}
	.el-form :deep(.el-input__wrapper:hover) {
		box-shadow: inset 0 0 0 1px var(--ly-glass-border);
	}
	.el-form :deep(.el-input__wrapper.is-focus) {
		background: var(--ly-glass-bg);
		box-shadow: inset 0 0 0 1px var(--ly-color-primary), var(--ly-input-focus-ring);
	}

	/* 验证码：输入框 + 独立验证码图片块，组成一行 */
	.captcha-row {
		display: flex;
		gap: 12px;
		width: 100%;
		align-items: stretch;
	}
	.captcha-row > .el-input {
		flex: 1;
	}
	.captcha-box {
		position: relative;
		width: 132px;
		min-height: 50px;
		flex-shrink: 0;
		border-radius: 14px;
		overflow: hidden;
		cursor: pointer;
		border: 1px solid var(--ly-line-soft);
		background: var(--ly-glass-bg-soft);
		box-sizing: border-box;
		transition: box-shadow var(--ly-duration-fast) ease;
	}
	.captcha-box:hover {
		box-shadow: var(--ly-input-focus-ring);
	}
	.captcha-img {
		width: 100%;
		height: 100%;
		min-height: 48px;
		display: block;
		object-fit: contain;
	}
	/* 悬停遮罩提示刷新 */
	.captcha-mask {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 16px;
		color: var(--ly-color-primary);
		background: var(--ly-glass-bg);
		backdrop-filter: blur(6px);
		opacity: 0;
		transition: opacity var(--ly-duration-fast) ease;
	}
	.captcha-box:hover .captcha-mask {
		opacity: 1;
	}

	.login-btn {
		margin-top: 8px;
		height: 50px;
		font-size: 15px;
		letter-spacing: 2px;
		box-shadow: var(--ly-shadow-primary);
	}
</style>
