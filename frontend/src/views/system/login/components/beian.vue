<template>
  <div class="beian-info">
    <a href="https://beian.miit.gov.cn/" target="_blank">豫ICP备xxxxx号-1</a>
  </div>
</template>

<style scoped>
    .beian-info {
        position: fixed;
        bottom: 20px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 13px;
        color: var(--el-text-color-secondary);
        z-index: 2;

        a {
            color: var(--el-text-color-secondary);
            text-decoration: none;
            transition: color 0.3s;

            &:hover {
                color: var(--el-color-primary);
                text-decoration: underline;
            }
        }
    }

    @media (max-width: 768px) {
        .beian-info {
            font-size: 11px;
            bottom: 10px;
        }
    }
</style>