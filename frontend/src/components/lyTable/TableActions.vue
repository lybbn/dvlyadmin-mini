<template>
    <div class="lyTable-do">
        <el-button
            v-if="!hideRefresh"
            @click="emit('refresh')"
            icon="refresh"
            circle
            style="margin-left: 15px"
        ></el-button>
        <el-popover
            v-if="hasColumns"
            :placement="placement"
            title="列设置"
            :width="500"
            trigger="click"
            :hide-after="0"
            @show="customColumnShow = true"
            @after-leave="customColumnShow = false"
        >
            <template #reference>
                <el-button icon="set-up" circle style="margin-left: 15px"></el-button>
            </template>
            <column-setting
                v-if="customColumnShow"
                ref="lyColumnSetting"
                @userChange="emit('columnChange', $event)"
                @save="emit('columnSave', $event)"
                @back="emit('columnBack')"
                :column="userColumn"
            ></column-setting>
        </el-popover>
        <el-popover
            v-if="!hideSetting"
            :placement="placement"
            title="表格设置"
            :width="400"
            trigger="click"
            :hide-after="0"
        >
            <template #reference>
                <el-button icon="setting" circle style="margin-left: 15px"></el-button>
            </template>
            <el-form label-width="80px" label-position="left">
                <el-form-item label="表格尺寸">
                    <el-radio-group
                    v-model="config.size"
                    size="small"
                    @change="emit('sizeChange', $event)"
                    >
                        <el-radio-button value="large">大</el-radio-button>
                        <el-radio-button value="default">正常</el-radio-button>
                        <el-radio-button value="small">小</el-radio-button>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="样式">
                    <el-checkbox v-model="config.border" @change="emit('borderChange', $event)" label="纵向边框"></el-checkbox>
                    <el-checkbox v-model="config.stripe" @change="emit('stripeChange', $event)" label="斑马纹"></el-checkbox>
                </el-form-item>
                <el-form-item label="序号列">
                    <el-radio-group v-model="config.sequence" @change="emit('sequenceChange', $event)">
                        <el-radio :value="true">显示</el-radio>
                        <el-radio :value="false">隐藏</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
        </el-popover>
        <el-button icon="Download" @click="handleExport" circle title="导出" v-if="!hideExport"></el-button>
        <el-button icon="Upload" @click="handleImport" circle title="导入" v-if="!hideImport"></el-button>
    </div>
</template>

<script setup>
    import { ref, computed } from 'vue'
    import ColumnSetting from './columnSetting.vue'

    const props = defineProps({
        placement:{ type: String, default: "top" },
        hideRefresh: { type: Boolean, default: false },
        hideSetting: { type: Boolean, default: false },
        hideExport:{ type: Boolean, default: false },
        hideImport:{ type: Boolean, default: true },
        userColumn: { type: Array, default: () => [] },
        column: { type: Array, default: () => [] },
        config: { 
            type: Object, 
            default: () => ({
                size: 'default',
                border: false,
                stripe: false,
                sequence : false,
            })
        }
    })

    const emit = defineEmits([
        'refresh',
        'columnChange',
        'columnSave',
        'columnBack',
        'sizeChange',
        'borderChange',
        'stripeChange',
        'sequenceChange',
        'import',
        'export'
    ])

    const customColumnShow = ref(false)
    const lyColumnSetting = ref(null)

    const hasColumns = computed(() => {
        return props.column != undefined && props.column != null && props.column.length > 0
    })

    function handleExport(){
        emit('export')
    }

    function handleImport(){
        emit('import')
    }

    defineExpose({
        lyColumnSetting
    })
</script>

<style scoped>
    .lyTable-do {
        white-space: nowrap;
    }
</style>