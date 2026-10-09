<template>
	<ly-aurora />
	<el-config-provider :locale="locale" :size="siteThemeStore.elementSize" :zIndex="siteThemeStore.elementzIndex">
		<router-view></router-view>
	</el-config-provider>
</template>

<script setup>
    import lyAurora from '@/components/lyAurora/lyAurora.vue'
    import {ref, onMounted,computed,watch} from 'vue'
    import {useSiteThemeStore} from "@/store/siteTheme";
    import {useUserState} from "@/store/userState";
    import config from '@/config'
    import {autoStorage} from '@/utils/util'
    import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
    import en from 'element-plus/dist/locale/en.mjs'
    import { useLywebsocket } from "@/store/websocket";
    import { useRoute } from 'vue-router';
    const route = useRoute()
    const lywebsocket = useLywebsocket()
    const userState = useUserState()
    const siteThemeStore = useSiteThemeStore()
    const colorPrimary = siteThemeStore.colorPrimary
    const menuHeaderColor01 = siteThemeStore.menuHeaderColor01
    const menuHeaderColor02 = siteThemeStore.menuHeaderColor02

    const language = ref(config.LANG)
    const locale = computed(() => (language.value === 'zh-cn' ? zhCn : en))

    onMounted(()=>{
        siteThemeStore.setColorPrimary(colorPrimary)
        // 旧版主题缓存迁移：localStorage 中仍是历史旧默认色时自动升级为新蓝调玻璃色
        const OLD_HEADER_COLORS = ['#272E39', 'rgba(255, 255, 255, 0.72)']
        const OLD_MENU_COLORS = ['#fff', 'rgba(255, 255, 255, 0.62)']
        if (OLD_HEADER_COLORS.includes(autoStorage.get('menuHeaderColor01'))) {
            siteThemeStore.setMenuHeaderColor01(menuHeaderColor01)
        }
        if (OLD_MENU_COLORS.includes(autoStorage.get('menuHeaderColor02'))) {
            siteThemeStore.setMenuHeaderColor02(menuHeaderColor02)
        }
        if (siteThemeStore.siteTheme === 'dark') {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
            siteThemeStore.setMenuHeaderColor01(menuHeaderColor01)
            siteThemeStore.setMenuHeaderColor02(menuHeaderColor02)
        }

    })

    watch( () => route.path, () => {
            if (!lywebsocket.isWebsocket()) {
                try {
                    lywebsocket.initWebSocket()
                } catch (e) {
                    console.log('websocket错误');
                }
            }
        },
        {
            deep: true,
        }
    );

    // 监听宽度变化，更新全局 CSS 变量
    watch(() => siteThemeStore.menuWidth,
        (mwidth) => {
            document.documentElement.style.setProperty('--ry-menu-width', mwidth+"px");
        },
        { immediate: true } // 立即执行以初始化
    );

    //此内容不能删除
    console.info(`%cdvlyadmin-mini %cVer${userState.sysConfig.sysVersion} %chttps://doc.lybbn.cn/`,
        "color:#296dff;font-size: 22px;font-weight:bolder",
        "color:#999;font-size: 12px",
        "color:#333"
      )
</script>

<style lang="scss">
    @use '@/assets/lybbn/css/style.scss' as *;
</style>

