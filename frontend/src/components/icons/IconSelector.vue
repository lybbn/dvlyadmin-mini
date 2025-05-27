<!--
/**
 * description：icon选择器
 * author: lybbn
 * program django-vue-lyadmin
 * email: 1042594286@qq.com
 * website: http://www.lybbn.cn
 * date: 2022.11.17
 * EditDate: 2025.05.27
 * @version: 1.1
 * remark: 如果要分发django-vue-lyadmin源码或其中组件等，需在本文件顶部保留此文件头信息！！！
 */
-->
 <template>
    <div class="icon-selector-wrapper">
        <el-button @click="handleClick" class="icon-select-btn">
            <template #icon v-if="iconText">
            <svg-icon :icon-class="iconText" style="font-size: 18px;" />
            </template>
            {{ iconText ? iconText : '请选择图标' }}
        </el-button>

        <ly-dialog
            v-model="dialogVisible"
            :title="dialogTitle"
            width="60%"
            custom-class="glass-dialog"
            :before-close="handleClose"
        >
            <div class="search-container">
                <el-input
                    size="large"
                    v-model="searchIconText"
                    clearable
                    placeholder="搜索图标（如 dashboard）"
                    prefix-icon="Search"
                    class="search-input"
                />
                <el-button size="large" icon="Delete" @click="deleteAll" type="danger">清空</el-button>
            </div>

            <el-tabs stretch type="card">
                <el-tab-pane v-for="item in iconDataList" :key="item.name" lazy :label="`${item.name} (${item.icons.length})`">
                    <el-scrollbar height="500px">
                        <div class="icons-container">
                            <div v-for="(icon, index) in item.icons" :key="index" class="icon-card" @click="chooseIcon(icon)">
                                <div class="icon-wrapper">
                                    <svg-icon :icon-class="icon" style="font-size: 24px; margin-top: 10px;" />
                                    <span class="icon-text">{{ icon }}</span>
                                </div>
                            </div>
                        </div>
                    </el-scrollbar>
                </el-tab-pane>
            </el-tabs>
        </ly-dialog>
    </div>
</template>
<script setup>
    import { ref, watch, onMounted } from 'vue'
    import * as ElIcons from '@element-plus/icons-vue'
    import LyDialog from '@/components/dialog/dialog.vue'
    import { getIconList } from './iconlist.js'
    import { deepClone } from '@/utils/util.js'

    const props = defineProps({
        modelValue: {
            type: String,
            default: ''
        }
    })

    const emit = defineEmits(['update:modelValue'])

    const dialogTitle = ref('图标选择器')
    const dialogVisible = ref(false)
    const iconText = ref(props.modelValue)
    const searchIconText = ref('')
    const iconDataList = ref([])
    const oldIcons = ref([])

    const loadIcons = () => {
    const extendIcons = getIconList()
    const eleIcons = Object.keys(ElIcons)
    iconDataList.value = [
            {
            name: '默认图标',
            icons: eleIcons
        },
        {
            name: '扩展图标',
            icons: extendIcons
        }
    ]
        oldIcons.value = deepClone(iconDataList.value)
    }

    // Methods
    const handleClick = () => {
        dialogVisible.value = true
    }

    const handleClose = () => {
        dialogVisible.value = false
    }

    const chooseIcon = (iconName) => {
        iconText.value = iconName
        emit('update:modelValue', iconName)
        handleClose()
    }

    const handleChange = (val) => {
        if (val) {
            const filterData = deepClone(oldIcons.value)
            filterData.forEach((category) => {
                category.icons = category.icons.filter((icon) =>
                    icon.toLowerCase().includes(val.toLowerCase())
                )
            })
            iconDataList.value = filterData
        } else {
            iconDataList.value = deepClone(oldIcons.value)
        }
    }

    const deleteAll = () => {
        iconText.value = ''
        searchIconText.value = ''
        iconDataList.value = deepClone(oldIcons.value)
        emit('update:modelValue', '')
    }

    watch(
        () => props.modelValue,
        (newVal) => {
            iconText.value = newVal
        }
    )

    watch(
        () => iconText.value,
        (newVal) => {
            emit('update:modelValue', newVal)
        }
    )

    watch(
        searchIconText,
        (val) => {
            handleChange(val)
        }
    )

    onMounted(() => {
        loadIcons()
    })
</script>

<style lang="scss" scoped>
    .icon-selector-wrapper {
        display: inline-block;
    }

    .icon-select-btn {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease-in-out;
        &:hover {
            background-color: #f0f0f0;
        }
    }

    .glass-dialog {
        backdrop-filter: blur(10px);
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }

    .search-container {
        display: flex;
        gap: 12px;
        align-items: center;
        margin-bottom: 20px;
    }

    .search-input {
        flex: 1;
    }

    .icons-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 16px;
        padding: 10px;

        .icon-card {
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            border-radius: 10px;
            background-color: #fff;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s, box-shadow 0.2s;
            &:hover {
                transform: translateY(-4px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
                background: linear-gradient(to bottom right, #f9f9f9, #ffffff);
            }

            .icon-wrapper {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                width: 100%;
                height: 100%;
                padding: 10px 0;
            }

            .icon-text {
                font-size: 12px;
                color: #666;
                margin-top: 6px;
                text-align: center;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
        }
    }
</style>