<template>
    <div class="error-container">
        <div class="error-content">
        <div class="error-graphic">
            <svg class="error-svg" viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg">
                <path class="error-path" d="M100,150 C150,50 350,50 400,150 C450,250 150,250 100,150 Z" />
                <circle class="error-dot" cx="150" cy="100" r="8" />
                <circle class="error-dot" cx="350" cy="100" r="8" />
                <path class="error-mouth" d="M150,180 Q250,220 350,180" />
            </svg>
        </div>
        
        <h1 class="error-title">500</h1>
        <h2 class="error-subtitle">服务器开小差了</h2>
        <p class="error-message">
            我们正在努力修复这个问题，请稍后再试或联系支持团队。
        </p>
        
        <div class="error-actions">
            <button @click="goHome" class="action-button home-button">
            <i class="icon-home"></i> 返回首页
            </button>
            <button @click="reload" class="action-button refresh-button">
            <i class="icon-refresh"></i> 重新加载
            </button>
        </div>
        
        <div class="error-tech" v-if="showDetails">
            <p><strong>错误详情：</strong></p>
            <code class="error-details">{{ errorDetails }}</code>
            <button @click="copyError" class="copy-button">
            <i class="icon-copy"></i> 复制错误
            </button>
        </div>
        
        <!-- <button @click="toggleDetails" class="details-toggle">
            {{ showDetails ? '隐藏技术细节' : '显示技术细节' }}
        </button> -->
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();
    const showDetails = ref(false);
    const errorDetails = ref('Internal Server Error: Something went wrong on our end.');

    const goHome = () => {
        router.push('/');
    };

    const reload = () => {
        window.location.reload();
    };

    const toggleDetails = () => {
        showDetails.value = !showDetails.value;
    };

    const copyError = async () => {
        try {
            await navigator.clipboard.writeText(errorDetails.value);
            alert('错误信息已复制到剪贴板');
        } catch (err) {
            console.error('复制失败:', err);
        }
    };
</script>

<style scoped>
    .error-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .error-content {
        max-width: 600px;
        width: 100%;
        background: white;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .error-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        background: linear-gradient(90deg, #ff4d4d, #f9cb28);
    }

    .error-graphic {
        margin: 0 auto 30px;
        width: 200px;
        height: 150px;
    }

    .error-svg {
        width: 100%;
        height: 100%;
    }

    .error-path {
        fill: #ffecec;
        stroke: #ff4d4d;
        stroke-width: 3;
        stroke-dasharray: 1000;
        stroke-dashoffset: 1000;
        animation: draw 3s ease-in-out forwards;
    }

    .error-dot {
        fill: #ff4d4d;
        opacity: 0;
        animation: fadeIn 1s ease-in-out 1.5s forwards;
    }

    .error-mouth {
        fill: none;
        stroke: #ff4d4d;
        stroke-width: 3;
        stroke-linecap: round;
        stroke-dasharray: 100;
        stroke-dashoffset: 100;
        animation: draw 1s ease-in-out 1s forwards;
    }

    .error-title {
        font-size: 5rem;
        margin: 0;
        color: #ff4d4d;
        font-weight: 700;
        line-height: 1;
    }

    .error-subtitle {
        font-size: 1.75rem;
        margin: 10px 0;
        color: #333;
        font-weight: 600;
    }

    .error-message {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 30px;
    }

    .error-actions {
        display: flex;
        gap: 15px;
        justify-content: center;
        margin-bottom: 30px;
    }

    .action-button {
        border: none;
        border-radius: 50px;
        padding: 12px 24px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
    }

    .home-button {
        background: #4a6cf7;
        color: white;
    }

    .home-button:hover {
        background: #3a5ce4;
        transform: translateY(-2px);
    }

    .refresh-button {
        background: #f5f7fa;
        color: #4a6cf7;
        border: 1px solid #ddd;
    }

    .refresh-button:hover {
        background: #eaeef5;
        transform: translateY(-2px);
    }

    /* 技术细节 */
    .error-tech {
        background: #f9f9f9;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        text-align: left;
    }

    .error-details {
        display: block;
        background: #2d2d2d;
        color: #f8f8f8;
        padding: 10px;
        border-radius: 4px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        margin: 10px 0;
    }

    .copy-button {
        background: #2d2d2d;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: background 0.3s;
    }

    .copy-button:hover {
        background: #4a4a4a;
    }

    .details-toggle {
        background: none;
        border: none;
        color: #4a6cf7;
        font-size: 0.9rem;
        cursor: pointer;
        text-decoration: underline;
        margin-top: 10px;
    }

    /* 动画 */
    @keyframes draw {
        to {
            stroke-dashoffset: 0;
        }
    }

    @keyframes fadeIn {
        to {
            opacity: 1;
        }
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .error-content {
            padding: 30px 20px;
            border-radius: 12px;
        }
        
        .error-title {
            font-size: 4rem;
        }
        
        .error-subtitle {
            font-size: 1.5rem;
        }
        
        .error-message {
            font-size: 1rem;
        }
        
        .error-actions {
            flex-direction: column;
            gap: 10px;
        }
        
        .action-button {
            width: 100%;
            justify-content: center;
        }
        
        .error-graphic {
            width: 150px;
            height: 120px;
        }
    }

    @media (max-width: 480px) {
        .error-title {
            font-size: 3.5rem;
        }
        
        .error-content {
            padding: 25px 15px;
        }
    }
</style>