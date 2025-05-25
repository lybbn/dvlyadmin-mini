<template>
    <div></div>
</template>
<script setup>
    import { useRouter, useRoute } from 'vue-router'

    const router = useRouter()
    const route = useRoute()

    // 获取原始路径
    const path = route.params.path
    // 获取原始查询参数（排除我们添加的时间戳）
    const query = {...route.query}
    delete query.t

    // 立即重定向回原始路由
    router.replace({ path: '/' + path, query }).then(() => {
        // 可选：滚动到顶部
        window.scrollTo(0, 0)
    })
</script>