<!--
 * @Descripttion: 搜索组件
 * @author：lybbn
 * @version：1.0
 * @EditDate：2025-06-24
 * @program：dvlyadmin-mini
-->
<template>
    <div class="search-bar-container">
        <el-form
        ref="formRef"
        :inline="true"
        :model="model"
        label-position="left"
        class="search-bar-form"
        :class="{ 'is-collapsed': isCollapsed && hasOverflow }"
        >
            <!-- 所有搜索项 -->
            <div class="search-items-container">
                <slot name="default">
                <!-- 默认搜索项 -->
                </slot>
            </div>

            <!-- 操作按钮 -->
            <div class="action-buttons">
                <slot name="actions">
                    <!-- 默认操作按钮 -->
                    <el-button
                        @click="emit('search')"
                        type="primary"
                        icon="Search"
                        v-auth="'Search'"
                    >查询</el-button>
                    <el-button
                        @click="emit('reset')"
                        icon="Refresh"
                        v-auth="'Search'"
                    >重置</el-button>
                </slot>

                <!-- 展开/收起按钮 -->
                <el-button
                    v-if="hasOverflow"
                    @click="toggleCollapse"
                    type="text"
                    class="toggle-btn"
                >
                    {{ isCollapsed ? '展开' : '收起' }}
                    <el-icon :class="{ 'rotate-icon': !isCollapsed }">
                        <ArrowDown />
                    </el-icon>
                </el-button>
            </div>
        </el-form>
    </div>
</template>

<script setup>
    import { ref, onMounted, onUnmounted, nextTick } from 'vue'
    import { ArrowDown } from '@element-plus/icons-vue'

    const props = defineProps({
        model: {
            type: Object,
            required: true
        }
    })

    const emit = defineEmits(['search', 'reset'])

    const formRef = ref(null)
    const isCollapsed = ref(true)
    const hasOverflow = ref(false)

    // 检测内容是否超出
    const checkOverflow = () => {
        nextTick(() => {
            if (formRef.value?.$el) {
                const container = formRef.value.$el
                // 检查容器是否出现滚动高度（表示内容溢出）
                hasOverflow.value = container.scrollHeight > container.clientHeight
            }
        })
    }

    const toggleCollapse = () => {
        isCollapsed.value = !isCollapsed.value
    }

    // 暴露方法给父组件
    defineExpose({
        toggleCollapse,
        checkOverflow
    })

    onMounted(() => {
        checkOverflow()
        window.addEventListener('resize', checkOverflow)
    })

    onUnmounted(() => {
        window.removeEventListener('resize', checkOverflow)
    })
</script>

<style scoped>
    .search-bar-container {
        position: relative;
        margin-bottom: 16px;
    }

    .search-bar-form {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease;
    }

    .search-bar-form.is-collapsed {
        max-height: 62px; /* 大约一行的高度 */
        overflow: hidden;
    }

    .search-items-container {
        display: flex;
        flex-wrap: wrap;
        flex: 1;
        min-width: 0; /* 防止flex容器溢出 */
    }

    .search-item {
        margin-bottom: 0;
        flex-shrink: 0;
    }

    .action-buttons {
        display: flex;
        margin-left: auto;
        flex-shrink: 0;
    }

    .toggle-btn {
        padding: 0;
        color: var(--el-color-primary);
    }

    .toggle-btn .el-icon {
        transition: transform 0.3s;
        margin-left: 4px;
    }

    .rotate-icon {
        transform: rotate(180deg);
    }

    /* 移动端适配 */
    @media (max-width: 768px) {
        .search-bar-form {
            flex-direction: column;
            align-items: stretch;
        }
        
        .search-items-container {
            width: 100%;
        }
        
        .action-buttons {
            width: 100%;
            justify-content: flex-end;
            margin-left: 0;
            margin-top: 8px;
        }
        
        .search-item {
            width: 100%;
        }
        
        .el-input,
        .el-select {
            width: 100% !important;
        }
        
        .search-bar-form.is-collapsed {
            max-height: none; /* 移动端不折叠 */
        }
        
        .toggle-btn {
            display: none; /* 移动端隐藏展开/收起 */
        }
    }
</style>