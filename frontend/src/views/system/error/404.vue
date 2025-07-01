<template>
    <div class="error-page">
        <div class="error-container">
            <div class="error-content">
                <div class="error-code">
                    <span>4</span>
                    <div class="planet">
                        <div class="crater"></div>
                        <div class="crater"></div>
                        <div class="crater"></div>
                    </div>
                    <span>4</span>
                </div>
                <h1 class="error-title">页面迷失在宇宙中</h1>
                <p class="error-description">我们无法找到您请求的页面，它可能已被移除、重命名或暂时不可用。</p>
                
                <div class="error-actions">
                    <el-button type="primary" round @click="goback" class="action-btn">
                        <el-icon><arrow-left /></el-icon> 返回上一页
                    </el-button>
                    <el-button type="primary" plain round @click="backhome" class="action-btn">
                        <el-icon><home-filled /></el-icon> 返回首页
                    </el-button>
                    <el-button type="primary" plain round @click="exit" class="action-btn">
                        <el-icon><refresh /></el-icon> 重新登录
                    </el-button>
                </div>
                
                <div class="stars">
                    <div v-for="(star, index) in stars" :key="index" class="star" :style="star"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ElMessage, ElMessageBox } from 'element-plus'
    import { autoStorage } from "@/utils/util";
    import { useRouter } from 'vue-router'
    import { ref, onMounted } from 'vue'

    const router = useRouter()
    const stars = ref([])

    onMounted(() => {
        createStars()
    })

    function createStars() {
        const newStars = []
        for (let i = 0; i < 100; i++) {
            newStars.push({
                top: `${Math.random() * 100}%`,
                left: `${Math.random() * 100}%`,
                width: `${Math.random() * 3 + 1}px`,
                height: `${Math.random() * 3 + 1}px`,
                animationDelay: `${Math.random() * 5}s`
            })
        }
        stars.value = newStars
    }

    function backhome() {
        router.push('/home')
    }

    function goback() {
        router.go(-1)
    }

    function exit() {
        ElMessageBox.confirm('确定要退出登录吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }).then(() => {
            autoStorage.clearAll()
            router.push('/login')
            ElMessage.success('已退出登录!')
        }).catch(() => {})
    }
</script>

<style lang="scss" scoped>
    .error-page {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        height: 100vh;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #fff;
        font-family: 'Arial', sans-serif;
        position: relative;
    }

    .error-container {
        position: relative;
        z-index: 2;
        text-align: center;
        padding: 2rem;
        max-width: 800px;
    }

    .error-content {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .error-code {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 30px;
        font-size: 10rem;
        font-weight: 900;
        color: #fff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        position: relative;
        
        span {
            display: inline-block;
            animation: float 3s ease-in-out infinite;
            
            &:first-child {
                animation-delay: 0.1s;
            }
            
            &:last-child {
                animation-delay: 0.2s;
            }
        }
    }

    .planet {
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, #6e45e2 0%, #88d3ce 100%);
        border-radius: 50%;
        margin: 0 30px;
        position: relative;
        box-shadow: 0 0 30px rgba(110, 69, 226, 0.5);
        animation: rotate 20s linear infinite;
    
    .crater {
        position: absolute;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 50%;
        
        &:nth-child(1) {
            width: 20px;
            height: 20px;
            top: 20px;
            left: 20px;
        }
        
        &:nth-child(2) {
            width: 15px;
            height: 15px;
            top: 60px;
            left: 30px;
        }
        
        &:nth-child(3) {
            width: 25px;
            height: 25px;
            top: 40px;
            left: 60px;
        }
    }
    }

    .error-title {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #fff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }

    .error-description {
        font-size: 1.1rem;
        margin-bottom: 2rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
    }

    .error-actions {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        position: relative;
        z-index: 3;
    }

    .action-btn {
        transition: all 0.3s ease;
        padding: 12px 24px;
        font-weight: 500;
        
        :deep(.el-icon) {
            margin-right: 8px;
        }
        
        &:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
    }

    .stars {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
    }

    .star {
        position: absolute;
        background-color: #fff;
        border-radius: 50%;
        animation: twinkle 2s infinite alternate;
    }

    @keyframes twinkle {
        0% {
            opacity: 0.2;
        }
        100% {
            opacity: 1;
        }
    }

    @keyframes float {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-20px);
        }
    }

    @keyframes rotate {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    @media (max-width: 768px) {
        .error-code {
            font-size: 6rem;
        }
        
        .planet {
            width: 60px;
            height: 60px;
            margin: 0 15px;
        }
        
        .error-actions {
            flex-direction: column;
            align-items: center;
        }

        .action-btn {
            width: 100%;
            max-width: 100%;
            margin: 0 0 10px 0;
        }
    }
</style>