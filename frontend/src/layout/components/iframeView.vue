<!--
 * @Descripttion: iframe页嵌套
 * @version: 1.0
 * @LastEditors: lybbn
 * @LastEditTime: 2024/1/1
 * @Program: django-vue-lyadmin mini
-->

<template>
	<div v-show="$route.meta.type=='iframe'" class="iframe-pages">
		<iframe v-for="item in iframeList" :key="item.meta.url" v-show="$route.meta.url==item.meta.url" :src="item.meta.url" frameborder='0'></iframe>
	</div>
</template>

<script setup>
    import { watch, ref,computed,onMounted } from 'vue';
    import { useRoute } from 'vue-router'
    import {useSiteThemeStore} from "@/store/siteTheme";
    import {useIframeList} from "@/store/iframeList";

    const siteThemeStore = useSiteThemeStore()
    const storeIframeList = useIframeList()
    const route = useRoute()

    watch(() => route,(newValue) => {
        push(newValue);
    });
    const iframeList = computed(() => {
        return storeIframeList.iframeList
    })
    const ismobile = computed(() => {
        return siteThemeStore.ismobile
    })
    const ismultitabs = computed(() => {
        return siteThemeStore.ismultitabs
    })

    function push(route){
        if(route.meta.type == 'iframe'){
            if(ismobile.value || !ismultitabs.value){
                storeIframeList.setIframeList(route)
            }else{
                storeIframeList.pushIframeList(route)
            }
        }else{
            if(ismobile.value){
                storeIframeList.clearIframeList()
            }
        }
    }

    onMounted(()=>{
        push(route)
    })
	
</script>

<style scoped>
	.iframe-pages {
        width:100%;
        height:100%;
        background: #fff;
    }
	iframe {
        border:0;
        width:100%;
        height:100%;
        display: block;
    }
</style>
