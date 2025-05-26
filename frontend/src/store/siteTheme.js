import { defineStore } from 'pinia'
import colorTool from '@/utils/color'
import {autoStorage} from '@/utils/util'
import config from "@/config"
import i18n from '@/locales'

export const useSiteThemeStore = defineStore('siteTheme', {
    state:() => {
        return {
            //是否移动端布局
		    ismobile: false,
            //多标签
            ismultitabs:autoStorage.get('ismultitabs') || config.ISMULTITABS,
            frameLayout:autoStorage.get('frameLayout') || config.FRAMELAYOUT,
            //菜单是否折叠
            isMenuCollapse:config.IS_MENU_COLLAPSE,
            //控制主题:light正常模式、dark暗黑模式
            siteTheme:autoStorage.get('siteTheme') || config.THEME,
            //主题色
            colorPrimary:autoStorage.get('colorPrimary') || config.COLOR,
            // elementplus 组件大小： small、default、large
            elementSize:autoStorage.get('elementSize') || config.ELEMENT_SIZE,
            // elementplus 组件 zIndex
            elementzIndex:autoStorage.get('elementzIndex') || config.ELEMENT_ZINDEX,
            // elementplus button组件 autoInsertSpace 是否自动在两个中文字符之间插入空格
            elementButton:autoStorage.get('elementButton') || config.ELEMENT_BUTTON,
            //菜单宽度
            menuWidth:autoStorage.get('menuWidth') || config.MENU_WIDTH,
            //顶部导航颜色
            menuHeaderColor01:autoStorage.get('menuHeaderColor01') || config.MENU_HEADER_COLOR01,
            //左侧菜单颜色
            menuHeaderColor02:autoStorage.get('menuHeaderColor02') || config.MENU_HEADER_COLOR02,
            //语言
            language:autoStorage.get('language') || config.LANG,
        }
    },
    getters:{
    },
    actions: {
        setIsmobile(val) {
            this.ismobile = val;
            autoStorage.set('ismobile',val);
        },
        setIsmultitabs(val) {
            this.ismultitabs = val;
            autoStorage.set('ismultitabs',val);
        },
        setSiteTheme(val) {
            this.siteTheme = val;
            autoStorage.set('siteTheme',val);
            if (this.siteTheme === 'dark') {
                document.documentElement.style.setProperty('--ly-header-bg', this.menuHeaderColor01);
                document.documentElement.classList.add('dark')
            } else {
                document.documentElement.style.setProperty('--ly-header-bg', this.menuHeaderColor01);
                document.documentElement.classList.remove('dark')
            }
        },
        setColorPrimary(val) {
            this.colorPrimary = val;
            autoStorage.set('colorPrimary',val);
            if(this.colorPrimary){
                document.documentElement.style.setProperty('--el-color-primary', this.colorPrimary);
                for (let i = 1; i <= 9; i++) {
                    document.documentElement.style.setProperty(`--el-color-primary-light-${i}`, colorTool.lighten(this.colorPrimary,i/10));
                }
                for (let i = 1; i <= 9; i++) {
                    document.documentElement.style.setProperty(`--el-color-primary-dark-${i}`, colorTool.darken(this.colorPrimary,i/10));
                }
            }
        },
        setMenuCollapsed(val){
            this.isMenuCollapse = val
        },
        setElementSize(val){
            this.elementSize = val
            autoStorage.set('elementSize',val);
        },
        setElementzIndex(val){
            this.elementzIndex = val
            autoStorage.set('elementzIndex',val);
        },
        setElementButton(val){
            this.elementButton = val
            autoStorage.set('elementButton',val);
        },
        setMenuWidth(val){
            this.menuWidth = val
            autoStorage.set('menuWidth',val);
        },
        setMenuHeaderColor01(val){
            this.menuHeaderColor01 = val
            autoStorage.set('menuHeaderColor01',val);
            if(this.menuHeaderColor01 && this.siteTheme === 'light'){
                document.documentElement.style.setProperty('--ly-header-bg', this.menuHeaderColor01);
            }
        },
        setMenuHeaderColor02(val){
            this.menuHeaderColor02 = val
            autoStorage.set('menuHeaderColor02',val);
            if(this.menuHeaderColor02 && this.siteTheme === 'light'){
                document.documentElement.style.setProperty('--ry-menu-bg', this.menuHeaderColor02);
            }
        },
        setFrameLayout(val){
            this.frameLayout = val
            autoStorage.set('frameLayout',val);
        },
        setLanguage(val){
            i18n.global.locale.value = val;
            this.language = val
            autoStorage.set('language',val)
        },
    },
})