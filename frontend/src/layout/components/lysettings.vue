<template>
	<el-form ref="form" label-width="120px" label-position="left" style="padding:0 20px;">
		<el-divider></el-divider>
		<el-form-item :label="$t('frameSettings.language')">
			<el-select v-model="language" @change="changeLang">
				<el-option label="简体中文" value="zh-cn"></el-option>
				<el-option label="English" value="en"></el-option>
			</el-select>
		</el-form-item>
        <el-divider></el-divider>
        <el-form-item :label="$t('frameSettings.framebuju')">
			<!-- <el-select v-model="frameLayout" placeholder="请选择" @change="setFrameLayout">
				<el-option label="经典" value="default"></el-option>
				<el-option label="顶部" value="header"></el-option>
				<el-option label="分栏" value="fenlan"></el-option>
			</el-select> -->
            <div class="layout-drawer-content-flex">
                <div class="layout-drawer-content-item" @click="handleSetLayout('default')">
                    <section class="el-container is-vertical el-circular" :class="{ 'drawer-layout-active': frameLayout === 'default' }">
                        <header class="el-header" style="height: 10px"></header>
                        <section class="el-container">
                            <aside class="el-aside" style="width: 20px"></aside>
                            <section class="el-container is-vertical">
                                <main class="el-main"></main>
                            </section>
                        </section>
                    </section>
                    <div class="layout-tips-warp" :class="{ 'layout-tips-warp-active': frameLayout === 'default' }">
                        <div class="layout-tips-box">
                            <p class="layout-tips-txt">经典</p>
                        </div>
                    </div>
                </div>
                <div class="layout-drawer-content-item" @click="handleSetLayout('header')">
                    <section class="el-container is-vertical el-circular" :class="{ 'drawer-layout-active': frameLayout === 'header' }">
                        <header class="el-header" style="height: 10px"></header>
                        <section class="el-container">
                            <section class="el-container is-vertical">
                                <main class="el-main"></main>
                            </section>
                        </section>
                    </section>
                    <div class="layout-tips-warp" :class="{ 'layout-tips-warp-active': frameLayout === 'header' }">
                        <div class="layout-tips-box">
                            <p class="layout-tips-txt">顶部</p>
                        </div>
                    </div>
                </div>
                <div class="layout-drawer-content-item" @click="handleSetLayout('fenlan')">
                    <section class="el-container" :class="{ 'drawer-layout-active': frameLayout === 'fenlan' }">
                        <section class="el-container is-vertical">
                            <header class="el-header" style="height: 10px"></header>
							<section class="el-container">
								<aside class="el-aside-dark" style="width: 10px"></aside>
                        		<aside class="el-aside" style="width: 20px"></aside>
								<main class="el-main"></main>
							</section>
                        </section>
                    </section>
                    <div class="layout-tips-warp" :class="{ 'layout-tips-warp-active': frameLayout === 'fenlan' }">
                        <div class="layout-tips-box">
                            <p class="layout-tips-txt">分栏</p>
                        </div>
                    </div>
                </div>
            </div>
		</el-form-item>
		<el-divider></el-divider>
		<el-form-item :label="$t('frameSettings.themecolor')">
			<el-color-picker v-model="colorPrimary" :predefine="colorList"  @change="setColorPrimary"></el-color-picker>
		</el-form-item>
        <el-form-item :label="$t('frameSettings.headercolor')">
			<el-color-picker v-model="menuHeaderColor01" :predefine="menuColorList01"  @change="changeMenuHeaderColor01"></el-color-picker>
		</el-form-item>
        <el-form-item :label="$t('frameSettings.menucolor')">
			<el-color-picker v-model="menuHeaderColor02" :predefine="menuColorList02"  @change="changeMenuHeaderColor02"></el-color-picker>
		</el-form-item>
        <el-form-item :label="$t('frameSettings.menuwidth')+'(px)'">
			<el-input-number v-model="menuWidth"  @change="changeMenuWidth" style="width: 100%"></el-input-number>
		</el-form-item>
		<el-divider></el-divider>
        <el-form-item :label="$t('frameSettings.componentsize')">
			<el-select v-model="size" placeholder="请选择" @change="changeSize">
				<el-option label="默认" value="default"></el-option>
				<el-option label="小" value="small"></el-option>
                <el-option label="大" value="large"></el-option>
			</el-select>
		</el-form-item>
		<el-divider></el-divider>
	</el-form>
</template>

<script setup>
	import {ref, onMounted, reactive, watch, computed} from 'vue'
    import {useSiteThemeStore} from "@/store/siteTheme";
	import { useI18n } from 'vue-i18n'

	const { t } = useI18n()

    const siteThemeStore = useSiteThemeStore()

    let colorList = ref(['#008040', '#536dfe','#722ed1','#009688','#52c41a','#faad14','#ff5c93', '#c62f2f', '#fd726d'])
	let menuColorList01 = ref(['#272E39','#3C444D','#465161','#222b45', '#2c3643','#545c64','#009688','#52c41a','#faad14','#ff5c93'])
    let menuColorList02 = ref(['#fff','#3C444D','#465161','#222b45', '#2c3643','#545c64','#009688','#52c41a','#faad14','#ff5c93'])
    let colorPrimary = ref(siteThemeStore.colorPrimary || '#409EFF')
    let frameLayout = ref(siteThemeStore.frameLayout || 'default')
	let pagingLayout = ref(siteThemeStore.pagingLayout)

    function setColorPrimary() {
        siteThemeStore.setColorPrimary(colorPrimary.value)
    }

    function setPagingLayout() {
        siteThemeStore.setPagingLayout(pagingLayout.value)
    }

    function setFrameLayout(){
        siteThemeStore.setFrameLayout(frameLayout.value)
    }

    function handleSetLayout(val){
        frameLayout.value = val
        siteThemeStore.setFrameLayout(frameLayout.value)
    }

    function isdark() {
        if(siteThemeStore.siteTheme=='light'){
            return false
        }else{
            return true
        }
    }

    let dark = ref(isdark())

    let language = ref(siteThemeStore.language || 'zh-cn')

    //设置语言
    function changeLang(val){
        siteThemeStore.setLanguage(val)
    }

    //设置主题
    function setSiteTheme(){
        if(siteThemeStore.siteTheme=='light'){
            siteThemeStore.setSiteTheme('dark')
        }else{
            siteThemeStore.setSiteTheme('light')
        }
    }

    let layout = ref(siteThemeStore.programLayout)

    function changeLayout(val) {
        siteThemeStore.setProgramLayout(val)
    }

    let size = ref(siteThemeStore.elementSize)
    //设置组件大小
    function changeSize(val) {
        siteThemeStore.setElementSize(val)
    }

    //设置头部颜色
    let menuHeaderColor01 = ref(siteThemeStore.menuHeaderColor01)
    function changeMenuHeaderColor01(val) {
        siteThemeStore.setMenuHeaderColor01(val)
    }
    //设置菜单颜色
    let menuHeaderColor02 = ref(siteThemeStore.menuHeaderColor02)
    function changeMenuHeaderColor02(val) {
        siteThemeStore.setMenuHeaderColor02(val)
    }
    //设置菜单宽度
    let menuWidth = ref(parseInt(siteThemeStore.menuWidth))
    function changeMenuWidth(val) {
        siteThemeStore.setMenuWidth(val)
    }
</script>

<style lang="scss" scoped>
    .layout-drawer-content-flex {
		overflow: hidden;
		display: flex;
		flex-wrap: wrap;
		align-content: flex-start;
		margin: 0 -5px;
		.layout-drawer-content-item {
			width: 50%;
			height: 70px;
			cursor: pointer;
			border: 1px solid transparent;
			position: relative;
			padding: 5px;
			.el-container {
				height: 100%;
				.el-aside-dark {
					background-color: #b3c0d0;
				}
				.el-aside {
					background-color: #d3dce5;
				}
				.el-header {
					background-color: #b3c0d0;
                    padding: unset;
				}
				.el-main {
					background-color: #e9eef2;
				}
			}
			.el-circular {
				border-radius: 2px;
				overflow: hidden;
				border: 1px solid transparent;
				transition: all 0.3s ease-in-out;
			}
			.drawer-layout-active {
				border: 1px solid;
				border-color: var(--el-color-primary);
			}
			.layout-tips-warp,
			.layout-tips-warp-active {
				transition: all 0.3s ease-in-out;
				position: absolute;
				left: 50%;
				top: 50%;
				transform: translate(-50%, -50%);
				border: 1px solid;
				border-color: var(--el-color-primary-light-5);
				border-radius: 100%;
				padding: 4px;
				.layout-tips-box {
					transition: inherit;
					width: 28px;
					height: 28px;
					z-index: 9;
					border: 1px solid;
					border-color: var(--el-color-primary-light-5);
					border-radius: 100%;
					.layout-tips-txt {
						transition: inherit;
						position: relative;
						top: 5px;
						font-size: 12px;
						line-height: 1;
						letter-spacing: 2px;
						white-space: nowrap;
						color: var(--el-color-primary-light-5);
						text-align: center;
						transform: rotate(10deg);
						left: -1px;
						background-color: #e9eef2;
						width: 32px;
						height: 17px;
						line-height: 17px;
					}
				}
			}
			.layout-tips-warp-active {
				border: 1px solid;
				border-color: var(--el-color-primary);
				.layout-tips-box {
					border: 1px solid;
					border-color: var(--el-color-primary);
					.layout-tips-txt {
						color: var(--el-color-primary) !important;
						background-color: #e9eef2 !important;
					}
				}
			}
			&:hover {
				.el-circular {
					transition: all 0.3s ease-in-out;
					border: 1px solid;
					border-color: var(--el-color-primary);
				}
				.layout-tips-warp {
					transition: all 0.3s ease-in-out;
					border-color: var(--el-color-primary);
					.layout-tips-box {
						transition: inherit;
						border-color: var(--el-color-primary);
						.layout-tips-txt {
							transition: inherit;
							color: var(--el-color-primary) !important;
							background-color: #e9eef2 !important;
						}
					}
				}
			}
		}
	}
</style>
