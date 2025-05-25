<template>
	<div class="login-container">
		<!-- 动态背景层 -->
		<div class="background-layer">
			<ParticlesBackground />
			<div class="gradient-overlay"></div>
		</div>

		<!-- 主登录区域 -->
		<div class="login-card">
			<!-- 主题切换按钮 -->
			<div class="theme-toggle">
				<el-tooltip :content="siteThemeStore.siteTheme == 'dark' ? '切换至亮色模式' : '切换至暗色模式'">
					<el-button 
					:icon="siteThemeStore.siteTheme == 'dark' ? 'sunny' : 'moon'" 
					circle 
					class="theme-btn"
					@click="setSiteTheme"
					/>
				</el-tooltip>
			</div>
			
			<!-- 登录表单区域 -->
			<div class="login-content">
				<!-- 品牌展示区 -->
				<div class="brand-section">
					<div class="logo-wrapper">
						<img 
							:alt="config.APP_NAME" 
							src="@/assets/lybbn/imgs/logo.png"
							class="logo-image"
						>
					</div>
					<h1 class="app-name">{{ config.APP_NAME }}</h1>
					<p class="welcome-text">欢迎回来，请登录您的账户</p>
				</div>
				
				<!-- 登录表单 -->
				<div class="form-section">
					<el-tabs class="auth-tabs">
						<el-tab-pane label="账号密码登录" lazy>
							<module-password-form />
						</el-tab-pane>
					</el-tabs>
					<!-- 社交登录选项 -->
					<!-- <div class="social-login">
					<div class="divider">
						<span class="divider-text">或通过以下方式登录</span>
					</div>
					<div class="social-icons">
						<el-tooltip content="微信登录">
						<el-button circle class="social-icon wechat">
							<svg-icon icon-class="wechat" />
						</el-button>
						</el-tooltip>
						<el-tooltip content="微博登录">
						<el-button circle class="social-icon weibo">
							<svg-icon icon-class="weibo" />
						</el-button>
						</el-tooltip>
						<el-tooltip content="GitHub登录">
						<el-button circle class="social-icon github">
							<svg-icon icon-class="github" />
						</el-button>
						</el-tooltip>
					</div>
					</div> -->
				</div>
			</div>
			<!-- <div class="card-footer">
				<span>没有账户？</span>
				<el-link type="primary" :underline="false" @click="navigateToRegiter">立即注册</el-link>
			</div> -->
			<!-- 页脚 -->
			<div class="login-footer">
				<p class="copyright">© 2025 lybbn All rights reserved. <span class="version">v{{ config.APP_VER }}</span></p>
			</div>
			
		</div>
		<BeianInfo />
	</div>
</template>

<script setup>
	import { ref, onMounted } from 'vue'
	import { useSiteThemeStore } from "@/store/siteTheme"
	import { useRouter } from 'vue-router'
	import config from "@/config"
	import ModulePasswordForm from './components/modulePasswordForm.vue'
	import BeianInfo from './components/beian.vue'
	import ParticlesBackground from '@/components/tsParticles.vue'

	const router = useRouter()
	const siteThemeStore = useSiteThemeStore()

	// 设置主题
	function setSiteTheme() {
		siteThemeStore.setSiteTheme(siteThemeStore.siteTheme === 'light' ? 'dark' : 'light')
	}

	onMounted(() => {
		// 动态添加viewport meta标签
		const viewportMeta = document.querySelector("meta[name='viewport']") || document.createElement('meta')
		viewportMeta.name = 'viewport'
		viewportMeta.content = "width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=no"
		document.head.appendChild(viewportMeta)
	})

	const navigateToRegiter = () => {
		router.push('/register')
	}

</script>

<style lang="scss" scoped>
	.login-container {
		position: relative;
		width: 100%;
		height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		background-color: var(--el-bg-color-page);
	
		.background-layer {
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
		
			.particles-container {
				position: absolute;
				width: 100%;
				height: 100%;
				z-index: 1;
			}
			
			.gradient-overlay {
				position: absolute;
				width: 100%;
				height: 100%;
				background: linear-gradient(
					135deg, 
					rgba(var(--el-color-primary-rgb), 0.1) 0%, 
					rgba(var(--el-color-primary-rgb), 0) 50%
				);
				z-index: 2;
			}
		}
  
  	.login-card {
		position: relative;
		width: 460px;
		background: var(--el-bg-color-overlay);
		border-radius: 16px;
		box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
		padding: 40px;
		z-index: 10;
		backdrop-filter: blur(8px);
		border: 1px solid var(--el-border-color-light);
    
		.theme-toggle {
			position: absolute;
			top: 20px;
			right: 20px;
			
			.theme-btn {
			background: var(--el-fill-color-light);
			border: none;
			transition: all 0.3s ease;
			
			&:hover {
				transform: rotate(30deg);
				background: var(--el-fill-color);
			}
			}
		}
    
		.login-content {
			.brand-section {
				text-align: center;
				margin-bottom: 32px;
				
				.logo-wrapper {
					margin: 0 auto 16px;
					width: 80px;
					height: 80px;
					display: flex;
					align-items: center;
					justify-content: center;
					background: var(--el-color-primary-light-9);
					border-radius: 50%;
					padding: 12px;
				
					.logo-image {
						width: 100%;
						height: 100%;
						object-fit: contain;
					}
				}
				
				.app-name {
					font-size: 24px;
					font-weight: 600;
					color: var(--el-text-color-primary);
					margin: 0 0 8px;
				}
				
				.welcome-text {
					font-size: 14px;
					color: var(--el-text-color-secondary);
					margin: 0;
				}
			}
			
			.form-section {
				:deep(.auth-tabs) {
					.el-tabs__header {
						margin-bottom: 24px;
						
						.el-tabs__nav-wrap::after {
							display: none;
						}
						
						.el-tabs__item {
							font-size: 16px;
							font-weight: 500;
							padding: 0 16px 12px;
							
							&:first-child {
							padding-left: 0;
							}
						}
						
						.el-tabs__active-bar {
							height: 3px;
							border-radius: 3px;
						}
					}
				}

			.social-login {
				margin-top: 32px;
				
				.divider {
					display: flex;
					align-items: center;
					margin: 24px 0;
					color: var(--el-text-color-placeholder);
					
					&::before, &::after {
						content: "";
						flex: 1;
						height: 1px;
						background: var(--el-border-color);
					}
					
					.divider-text {
						padding: 0 12px;
						font-size: 12px;
					}
				}
				
				.social-icons {
					display: flex;
					justify-content: center;
					gap: 16px;
					
					.social-icon {
						width: 40px;
						height: 40px;
						font-size: 18px;
						border: none;
						transition: all 0.3s ease;
						
						&:hover {
							transform: translateY(-3px);
						}
						
						&.wechat {
							background: #07C160;
							color: white;
						}
						
						&.weibo {
							background: #E6162D;
							color: white;
						}
						
						&.github {
							background: #333;
							color: white;
						}
					}
					}
			}
			}
		}
		.card-footer {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            font-size: 14px;
            color: #7f8c8d;

            .el-link {
                font-size: 14px;
                margin-left: 5px;
            }
        }
		.login-footer {
			margin-top: 32px;
			text-align: center;
			
			.copyright {
				font-size: 12px;
				color: var(--el-text-color-secondary);
				margin: 0;
			
				.version {
					margin-left: 8px;
					color: var(--el-text-color-disabled);
				}
			}
		}
  }
}

@media (max-width: 768px) {
	.login-container {
		padding: 20px;

	.login-card {
		width: 100%;
		padding: 30px 20px;
		border-radius: 12px;
		
		.login-content {
			.brand-section {
				.logo-wrapper {
					width: 64px;
					height: 64px;
				}
				
				.app-name {
					font-size: 20px;
				}
			}
		}
	}
	}
}
</style>