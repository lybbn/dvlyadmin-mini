<template>
	<div class="login-container">
		<!-- 主登录卡片（极光背景由 App.vue 全局 lyAurora 提供） -->
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

			<!-- 品牌展示区 -->
			<div class="brand-section">
				<div class="logo-wrapper">
					<ly-img
						:alt="config.APP_NAME"
						:src="userState.sysConfig.logo"
						class="logo-image"
					/>
				</div>
				<h1 class="app-name">{{ config.APP_NAME }}</h1>
				<p class="welcome-text">欢迎回来，请登录您的账户</p>
				<div class="brand-art" aria-hidden="true">
					<svg class="brand-map" viewBox="0 0 340 110" fill="none">
						<path class="map-connector" d="M120 55H174C190 55 190 16 206 16H230" />
						<path class="map-connector" d="M120 55H230" />
						<path class="map-connector" d="M120 55H174C190 55 190 94 206 94H230" />
						<circle class="map-junction" cx="174" cy="55" r="3" />
						<rect class="map-hub" x="8" y="31" width="112" height="48" rx="14" />
						<text class="map-hub-title" x="64" y="51" text-anchor="middle">管理中枢</text>
						<text class="map-hub-caption" x="64" y="66" text-anchor="middle">DVLYADMIN</text>
						<rect class="map-node" x="230" y="3" width="98" height="26" rx="9" />
						<circle class="map-node-dot" cx="245" cy="16" r="3" />
						<text class="map-node-label" x="255" y="20">用户</text>
						<rect class="map-node" x="230" y="42" width="98" height="26" rx="9" />
						<circle class="map-node-dot" cx="245" cy="55" r="3" />
						<text class="map-node-label" x="255" y="59">权限</text>
						<rect class="map-node" x="230" y="81" width="98" height="26" rx="9" />
						<circle class="map-node-dot" cx="245" cy="94" r="3" />
						<text class="map-node-label" x="255" y="98">数据</text>
					</svg>
				</div>
			</div>

			<!-- 登录表单 -->
			<module-password-form />

			<!-- 页脚 -->
			<div class="login-footer">
				<p class="copyright">© 2025 lybbn All rights reserved. <span class="version">v{{ config.APP_VER }}</span></p>
			</div>
		</div>
		<BeianInfo />
	</div>
</template>

<script setup>
	import { onMounted } from 'vue'
	import { useSiteThemeStore } from "@/store/siteTheme"
	import config from "@/config"
	import ModulePasswordForm from './components/modulePasswordForm.vue'
	import BeianInfo from './components/beian.vue'
	import {useUserState} from "@/store/userState";

	const userState = useUserState()
	const siteThemeStore = useSiteThemeStore()

	// 设置主题
	function setSiteTheme() {
		siteThemeStore.setSiteTheme(siteThemeStore.siteTheme === 'light' ? 'dark' : 'light')
	}

	onMounted(() => {
		userState.getSystemConfig()
		// 动态添加viewport meta标签
		const viewportMeta = document.querySelector("meta[name='viewport']") || document.createElement('meta')
		viewportMeta.name = 'viewport'
		viewportMeta.content = "width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=no"
		document.head.appendChild(viewportMeta)
	})

</script>

<style lang="scss" scoped>
	.login-container {
		position: relative;
		width: 100%;
		min-height: 100vh;
		min-height: 100svh;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow-x: hidden;
		overflow-y: auto;
		padding: 32px 24px 64px;
		box-sizing: border-box;

		.login-card {
			position: relative;
			display: grid;
			grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.08fr);
			grid-template-rows: 1fr auto;
			column-gap: clamp(32px, 5vw, 64px);
			width: min(960px, 100%);
			max-width: 100%;
			min-height: 540px;
			background: var(--ly-glass-bg-strong);
			backdrop-filter: var(--ly-glass-blur);
			-webkit-backdrop-filter: var(--ly-glass-blur);
			border: 1px solid var(--ly-glass-border);
			border-radius: var(--ly-radius-xl);
			box-shadow: var(--ly-glass-highlight), var(--ly-shadow-card);
			padding: 56px clamp(40px, 6vw, 68px) 42px;
			z-index: 1;
			box-sizing: border-box;
			animation: ly-login-in var(--ly-duration-slow) ease backwards;

			&::before {
				content: '';
				position: absolute;
				inset: 0 auto 0 0;
				width: 42%;
				border-radius: var(--ly-radius-xl) 0 0 var(--ly-radius-xl);
				background:
					radial-gradient(circle at 94% 43%,
						transparent 0 40px,
						color-mix(in srgb, var(--ly-color-on-primary) 24%, transparent) 41px 42px,
						transparent 43px 82px,
						color-mix(in srgb, var(--ly-color-on-primary) 13%, transparent) 83px 84px,
						transparent 85px 124px,
						color-mix(in srgb, var(--ly-color-on-primary) 7%, transparent) 125px 126px,
						transparent 127px),
					var(--ly-gradient-primary);
				pointer-events: none;
			}

			@keyframes ly-login-in {
				from { opacity: 0; transform: translateY(12px); }
				to { opacity: 1; transform: none; }
			}

			.theme-toggle {
				position: absolute;
				top: 20px;
				right: 20px;
				z-index: 2;

				.theme-btn {
					background: var(--ly-glass-bg-soft);
					backdrop-filter: blur(8px);
					border: 1px solid var(--ly-glass-border);
					color: var(--ly-header-text);
					transition: background var(--ly-duration-fast) ease, color var(--ly-duration-fast) ease, transform var(--ly-duration-fast) ease;

					&:hover {
						transform: translateY(-1px);
						background: var(--ly-header-item-hover);
					}

					&:focus-visible {
						outline: none;
						box-shadow: var(--ly-focus-ring);
					}
				}
			}

			.brand-section {
				position: relative;
				z-index: 1;
				grid-column: 1;
				grid-row: 1;
				align-self: center;
				display: grid;
				grid-template-columns: 62px minmax(0, 1fr);
				grid-template-rows: auto auto auto auto auto;
				column-gap: 16px;
				align-items: center;
				text-align: left;
				margin: 0;
				padding: 24px 28px 24px 4px;

				&::before {
					content: 'ADMIN CONSOLE';
					grid-column: 1 / -1;
					grid-row: 1;
					margin-bottom: 18px;
					color: color-mix(in srgb, var(--ly-color-on-primary) 76%, transparent);
					font-size: 11px;
					font-weight: 700;
					letter-spacing: 1.8px;
				}

				.logo-wrapper {
					grid-column: 1;
					grid-row: 2;
					margin: 0;
					width: 62px;
					height: 62px;
					display: flex;
					align-items: center;
					justify-content: center;
					background: color-mix(in srgb, var(--ly-color-on-primary) 18%, transparent);
					border: 1px solid color-mix(in srgb, var(--ly-color-on-primary) 38%, transparent);
					border-radius: var(--ly-radius-lg);
					padding: 10px;
					box-sizing: border-box;
					box-shadow: var(--ly-glass-highlight);

					.logo-image {
						width: 100%;
						height: 100%;
						object-fit: contain;
					}
				}

				.app-name {
					grid-column: 2;
					grid-row: 2;
					font-size: clamp(18px, 2vw, 22px);
					font-weight: 700;
					color: var(--ly-color-on-primary);
					margin: 0;
					line-height: 1.35;
					overflow-wrap: anywhere;
				}

				.welcome-text {
					grid-column: 1 / -1;
					grid-row: 4;
					font-size: 13px;
					color: color-mix(in srgb, var(--ly-color-on-primary) 82%, transparent);
					margin: 9px 0 0;
					letter-spacing: 0.2px;
					line-height: 1.8;
				}

				.brand-art {
					grid-column: 1 / -1;
					grid-row: 5;
					width: 100%;
					max-width: 340px;
					margin-top: 22px;
					color: color-mix(in srgb, var(--ly-color-on-primary) 82%, transparent);

					.brand-map {
						display: block;
						width: 100%;
						height: auto;
						overflow: visible;
					}

					.map-connector {
						stroke: currentColor;
						stroke-width: 1.5;
						stroke-linecap: round;
						stroke-opacity: 0.55;
					}

					.map-junction,
					.map-node-dot {
						fill: var(--ly-color-on-primary);
					}

					.map-junction {
						fill-opacity: 0.8;
					}

					.map-hub {
						fill: var(--ly-color-on-primary);
						fill-opacity: 0.16;
						stroke: var(--ly-color-on-primary);
						stroke-opacity: 0.35;
					}

					.map-node {
						fill: var(--ly-color-on-primary);
						fill-opacity: 0.08;
						stroke: var(--ly-color-on-primary);
						stroke-opacity: 0.24;
					}

					.map-hub-title,
					.map-node-label {
						fill: var(--ly-color-on-primary);
						font-size: 11px;
						font-weight: 600;
					}

					.map-hub-title {
						font-size: 13px;
						font-weight: 700;
					}

					.map-hub-caption {
						fill: color-mix(in srgb, var(--ly-color-on-primary) 75%, transparent);
						font-size: 7px;
						letter-spacing: 1.1px;
					}
				}

				&::after {
					content: '让管理工作更清晰';
					grid-column: 1 / -1;
					grid-row: 3;
					margin-top: 38px;
					color: var(--ly-color-on-primary);
					font-size: clamp(26px, 2.7vw, 32px);
					font-weight: 700;
					letter-spacing: 0.02em;
					line-height: 1.35;
				}
			}

			:deep(.el-form) {
				position: relative;
				z-index: 1;
				grid-column: 2;
				grid-row: 1;
				align-self: center;
				width: 100%;
				margin: 0;
			}

			.login-footer {
				position: relative;
				z-index: 1;
				grid-column: 2;
				grid-row: 2;
				margin-top: 20px;
				text-align: left;

				.copyright {
					font-size: 12px;
					color: var(--ly-text-3);
					margin: 0;

					.version {
						margin-left: 8px;
					}
				}
			}
		}
	}

	@media (max-width: 760px) {
		.login-container {
			padding: 24px 18px 58px;

			.login-card {
				grid-template-columns: minmax(0, 1fr);
				grid-template-rows: auto auto auto;
				row-gap: 26px;
				width: min(480px, 100%);
				min-height: 0;
				padding: 62px 30px 30px;

				&::before {
					inset: 0 0 auto;
					width: 100%;
					height: 35%;
					border-radius: var(--ly-radius-xl) var(--ly-radius-xl) 0 0;
				}

				.brand-section {
					grid-column: 1;
					grid-row: 1;
					grid-template-columns: 54px minmax(0, 1fr);
					grid-template-rows: auto auto auto auto;
					column-gap: 14px;
					padding: 0;
					text-align: left;

					&::after {
						margin-top: 24px;
						font-size: 23px;
						text-align: left;
					}

					.logo-wrapper {
						width: 54px;
						height: 54px;
						margin: 0;
						border-radius: var(--ly-radius-md);
					}

					.app-name {
						font-size: 20px;
					}

					.welcome-text {
						font-size: 12px;
					}

					.brand-art {
						display: none;
					}
				}

				:deep(.el-form) {
					grid-column: 1;
					grid-row: 2;
				}

				.login-footer {
					grid-column: 1;
					grid-row: 3;
					margin-top: 0;
					text-align: center;
				}
			}
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.login-card {
			animation: none;
		}
	}
</style>
