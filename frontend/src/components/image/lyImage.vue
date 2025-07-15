<!--
 * @Descripttion: 封装el-image标签组件，方便替换127.0.0.1地址
 * @author：lybbn
 * @version：1.0
 * @EditDate：2025-07-15
 * @program：dvlyadmin-mini
-->
<template>
    <el-image :src="processedUrl" v-bind="$attrs">
        <!-- 透传插槽 -->
        <template v-for="(_, slot) in $slots" #[slot]="scope">
            <slot :name="slot" v-bind="scope || {}" />
        </template>
    </el-image>
</template>

<script setup>
    import { computed } from 'vue';
    import sysConfig from "@/config"

    const props = defineProps({
        src: {
            type: String,
            required: true,
        },
        productionBase: {
            type: String,
            default: sysConfig.API_URL,
        },
    });

    const processedUrl = computed(() => {
        if (import.meta.env.PROD && props.src.includes('127.0.0.1:8000')) {
            return props.src.replace('http://127.0.0.1:8000', props.productionBase);
        }
        return props.src;
    });
</script>