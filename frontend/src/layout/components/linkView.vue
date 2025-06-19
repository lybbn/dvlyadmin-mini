<template>
  <div class="redirecting">
    <p>正在跳转到外部链接...</p>
  </div>
</template>

<script setup>
    import { onMounted } from 'vue'
    import { useRoute, useRouter } from 'vue-router'

    const route = useRoute()
    const router = useRouter()

    onMounted(() => {
        if (route.meta?.type == 3 && route.meta?.link) {
            // 新窗口打开外链
            window.open(route.meta.link, '_blank')
            // 返回上一页（避免停留空白页）
            router.go(-1)
        }
    })
</script>

<style scoped>
    .redirecting {
    padding: 20px;
    text-align: center;
    }
</style>