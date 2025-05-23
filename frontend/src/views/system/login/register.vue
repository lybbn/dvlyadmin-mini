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
            
            <!-- 注册表单区域 -->
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
                    <h1 class="app-name">立即注册</h1>
                    <p class="welcome-text">加入我们的社区，开启全新体验</p>
                </div>
                
                <!-- 注册表单 -->
                <ModuleRegisterForm />
            </div>
            <div class="card-footer">
                <span>已有账户？</span>
                <el-link type="primary" :underline="false" @click="navigateToLogin">立即登录</el-link>
            </div>
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
import { useRouter } from 'vue-router'
import { useSiteThemeStore } from "@/store/siteTheme"
import config from "@/config"
import ModuleRegisterForm from './components/moduleRegisterForm.vue'
import ParticlesBackground from '@/components/tsParticles.vue'
import BeianInfo from './components/beian.vue'

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

const navigateToLogin = () => {
    router.push('/login')
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
        }

        .card-footer {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            margin-top: 15px;
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