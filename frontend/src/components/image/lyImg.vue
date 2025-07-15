<!--
 * @Descripttion: 封装img标签组件，方便替换127.0.0.1地址
 * @author：lybbn
 * @version：1.0
 * @EditDate：2025-07-15
 * @program：dvlyadmin-mini
-->
<template>
    <img :src="processedUrl" v-bind="$attrs" />
</template>

<script setup>
    import { computed } from 'vue';
    import sysConfig from "@/config"

    const props = defineProps({
        src: {
            type: String,
            required: true,
        },
        // 可选：自定义生产环境替换的目标地址（默认取当前域名）
        productionBase: {
            type: String,
            default: sysConfig.API_URL, // 默认替换为当前访问的域名
        },
    });
    const processedUrl = computed(() => {
        if (import.meta.env.PROD && props.src.includes('127.0.0.1:8000')) {
            return props.src.replace('http://127.0.0.1:8000', props.productionBase);
        }
        return props.src;
    });
</script>