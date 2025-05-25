<template>
	<el-form ref="form" label-width="120px" label-position="left" style="padding:0 20px;">
		<el-divider></el-divider>
		<el-form-item label="语言">
			<el-select v-model="language" @change="changeLang">
				<el-option label="简体中文" value="zh-cn"></el-option>
				<el-option label="English" value="en"></el-option>
			</el-select>
		</el-form-item>
		<el-divider></el-divider>
		<el-form-item label="主题颜色">
			<el-color-picker v-model="colorPrimary" :predefine="colorList"  @change="setColorPrimary"></el-color-picker>
		</el-form-item>
        <el-form-item label="头部颜色">
			<el-color-picker v-model="menuHeaderColor01" :predefine="menuColorList01"  @change="changeMenuHeaderColor01"></el-color-picker>
		</el-form-item>
        <el-form-item label="菜单颜色">
			<el-color-picker v-model="menuHeaderColor02" :predefine="menuColorList02"  @change="changeMenuHeaderColor02"></el-color-picker>
		</el-form-item>
        <el-form-item label="菜单宽度(px)">
			<el-input-number v-model="menuWidth"  @change="changeMenuWidth" style="width: 100%"></el-input-number>
		</el-form-item>
		<el-divider></el-divider>
        <el-form-item label="组件大小">
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

    const siteThemeStore = useSiteThemeStore()

    let colorList = ref(['#008040', '#536dfe','#722ed1','#009688','#52c41a','#faad14','#ff5c93', '#c62f2f', '#fd726d'])
	let menuColorList01 = ref(['#272E39','#3C444D','#465161','#222b45', '#2c3643','#545c64','#009688','#52c41a','#faad14','#ff5c93'])
    let menuColorList02 = ref(['#fff','#3C444D','#465161','#222b45', '#2c3643','#545c64','#009688','#52c41a','#faad14','#ff5c93'])
    let colorPrimary = ref(siteThemeStore.colorPrimary || '#409EFF')

	let pagingLayout = ref(siteThemeStore.pagingLayout)

    function setColorPrimary() {
        siteThemeStore.setColorPrimary(colorPrimary.value)
    }

    function setPagingLayout() {
        siteThemeStore.setPagingLayout(pagingLayout.value)
    }

    function isdark() {
        if(siteThemeStore.siteTheme=='light'){
            return false
        }else{
            return true
        }
    }

    let dark = ref(isdark())

    let language = ref(siteThemeStore.language)

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
    let menuWidth = ref(siteThemeStore.menuWidth)
    function changeMenuWidth(val) {
        siteThemeStore.setMenuWidth(val)
    }
</script>

<style scoped>
	.lyalert:deep(.el-alert__content){
		word-break: break-all;
		padding: 0 3px;
	}
</style>
