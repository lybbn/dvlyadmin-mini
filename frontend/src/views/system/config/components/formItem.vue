<template>
    <div class="form-container">
        <!-- 响应式表格 -->
        <el-table 
        :data="formList" 
        ref="tableRef"
        v-loading="loading"
        style="width: 100%"
        class="responsive-table"
        >
            <!-- 名称列 -->
            <el-table-column min-width="100" label="名称">
                <template #default="{ row }">
                <el-input v-if="row.edit" v-model="row.title" placeholder="请输入名称" />
                <span v-else>{{ row.title }}</span>
                </template>
            </el-table-column>

            <!-- 变量值列 -->
            <el-table-column min-width="200" label="变量值">
                <template #default="{ row }">
                    <!-- 文本输入 -->
                    <template v-if="['text','textarea'].includes(row.form_item_type_label)">
                        <el-input
                        v-model="formData[row.key]"
                        :type="row.form_item_type_label"
                        :placeholder="row.placeholder"
                        clearable
                        />
                    </template>

                    <!-- 数字输入 -->
                    <lyInputNumber
                        v-else-if="row.form_item_type_label === 'number'"
                        v-model="formData[row.key]"
                        :placeholder="row.placeholder"
                        style="width:100%"
                        :controls="false"
                    />

                    <!-- 日期时间选择器 -->
                    <el-date-picker
                        v-else-if="['datetime','date','time'].includes(row.form_item_type_label)"
                        v-model="formData[row.key]"
                        :type="row.form_item_type_label"
                        :placeholder="row.placeholder"
                    />

                    <!-- 下拉选择 -->
                    <el-select
                        v-else-if="row.form_item_type_label === 'select'"
                        v-model="formData[row.key]"
                        :placeholder="row.placeholder"
                        clearable
                    >
                        <el-option
                        v-for="item in row.setting || []"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        />
                    </el-select>

                    <!--    checkbox      -->
                    <el-checkbox-group
                        :key="row.id"
                        v-else-if="row.form_item_type_label === 'checkbox'"
                        v-model="formData[row.key]"
                        :placeholder="row.placeholder">
                        <el-checkbox
                            v-for="item in row.data_options || []"
                            :key="item.value"
                            :value="item.value">
                            {{ item.label }}
                        </el-checkbox>
                    </el-checkbox-group>
                    <!--    radio      -->
                    <el-radio-group
                        :key="row.id"
                        v-else-if="row.form_item_type_label === 'radio'"
                        v-model="formData[row.key]"
                        :placeholder="row.placeholder"
                        clearable
                    >
                        <el-radio
                            v-for="item in row.data_options || []"
                            :key="item.value"
                            :value="item.value">
                            {{ item.label }}
                        </el-radio>
                    </el-radio-group>
                    <!--    switch      -->
                    <el-switch
                        :key="row.id"
                        v-else-if="row.form_item_type_label === 'switch'"
                        v-model="formData[row.key]"
                        active-color="#13ce66"
                        inactive-color="#ff4949">
                    </el-switch>
                    <!--     图片     -->
                    <div v-else-if="row.form_item_type_label === 'image'" :key="row.id">
                        <pictureSingleUpload v-model="formData[row.key]"
                                :disabled="false" :round="false" :cropper="false"
                                title="" :show-file-list="false"
                                :width="90" :height="90"></pictureSingleUpload>
                    </div>
                    <!--     富文本     -->
                    <RichTextEditor v-else-if="row.form_item_type_label === 'richtext'" v-model="formData[row.key]" />

                    <!-- 提示文本 -->
                    <span v-if="row.tip" class="tip-text">{{ row.tip }}</span>
                </template>
            </el-table-column>

            <!-- 变量名列 -->
            <el-table-column min-width="150" label="变量名">
                <template #default="{ row }">
                    <el-input 
                        v-if="row.edit"
                        v-model="row.new_key"
                        class="variable-input"
                        placeholder="请输入变量key"
                    >
                        <template #prepend>
                        <span class="prefix">{{ activeTab.key }}</span>
                        </template>
                    </el-input>
                    <span v-else class="variable-name">{{ activeTab.key }}.{{ row.key }}</span>
                </template>
            </el-table-column>

            <!-- 操作列 -->
            <el-table-column label="操作" fixed="right" width="170" class-name="action-column">
                <template #default="{ row, $index }">
                    <div class="action-buttons">
                        <el-button link type="primary" @click="handleSave(row)">保存</el-button>
                        <template v-if="row.edit">
                            <el-button link @click="handleCancel($index)">取消</el-button>
                        </template>
                        <template v-else>
                            <el-button link type="primary" @click="handleEdit($index)" v-auth="'systemConfig:Update'">编辑</el-button>
                        </template>
                        <el-popconfirm title="确定删除吗？" @confirm="handleDelete(row)">
                            <template #reference>
                                <el-button link type="danger" v-auth="'systemConfig:Delete'">删除</el-button>
                            </template>
                        </el-popconfirm>
                    </div>
                </template>
            </el-table-column>
        </el-table>

        <!-- 提交按钮 -->
        <!-- <div class="submit-area">
            <el-button type="primary" @click="handleSubmit" v-auth="'systemConfig:Save'">保存配置</el-button>
        </div> -->
    </div>
</template>

<script setup>
    import { ref, watch, nextTick } from 'vue'
    import { ElMessage, ElPopconfirm } from 'element-plus'
    import Api from '@/api/api'
    import RichTextEditor from '@/components/editor/wangEditor.vue'
    import pictureSingleUpload from '@/components/upload/single-picture.vue'
    import lyInputNumber from "@/components/lyInputNumber.vue"

    // 组件属性
    const props = defineProps({
        options: {
            type: Object,
            default: () => ({})
        },
        editableTabsItem: {
            type: Object,
            default: () => ({})
        }
    })

    // 响应式数据
    const loading = ref(false)
    const formList = ref([])
    const formData = ref({})
    const tableRef = ref(null)
    const activeTab = ref(props.editableTabsItem)

    // 获取数据
    const fetchData = async () => {
        try {
            loading.value = true
            const res = await Api.platformsettingsSysconfig({ 
                parent: props.options.id, 
                limit: 999 
            })
            
            formList.value = res.data.data.map(item => ({
                ...item,
                edit: false,
                new_key: item.key
            }))
            
            // 初始化表单数据
            formData.value = formList.value.reduce((acc, cur) => {
                acc[cur.key] = cur.value || (['checkbox', 'array'].includes(cur.form_item_type_label) ? [] : undefined)
                return acc
            }, {})
            
        } catch (error) {
            ElMessage.error('数据加载失败')
        } finally {
            loading.value = false
        }
    }

     // 监听选项变化
    watch(() => props.options, (newVal) => {
        if (newVal?.id) {
            fetchData()
        }
    }, { immediate: true })

    // 保存整个表单
    const handleSubmit = async () => {
        try {
            // 准备提交数据...
            const res = await Api.platformsettingsSysconfigSavecontent({
                ...formList.value,
                id: props.options.id
            })
            
            if (res.code === 2000) {
                ElMessage.success('保存成功')
                fetchData()
            } else {
                ElMessage.warning(res.msg)
            }
        } catch (error) {
            ElMessage.error('保存失败')
        }
    }

    // 行编辑
    const handleEdit = (index) => {
        formList.value[index].edit = true
    }

    // 取消编辑
    const handleCancel = (index) => {
        formList.value[index].edit = false
        formList.value[index].new_key = formList.value[index].key
    }

    function convertToString(val){
        if(val == undefined || val == null){
            return ""
        }
        return typeof val === 'string' ? val : val.toString();
    }
    // 保存行编辑
    const handleSave = async (row) => {
        try {
            let newvalue = formData.value[row.key]

            const res = await Api.platformsettingsSysconfigEdit({
                ...row,
                key: row.new_key,
                value: convertToString(newvalue)
            })
            
            if (res.code === 2000) {
                ElMessage.success('保存成功')
                fetchData()
            } else {
                ElMessage.warning(res.msg)
            }
        } catch (error) {
            ElMessage.error('保存失败')
        }
    }

    // 删除行
    const handleDelete = async (row) => {
        try {
            const res = await Api.platformsettingsSysconfigDelete({ id: row.id })
            if (res.code === 2000) {
                ElMessage.success('删除成功')
                fetchData()
            } else {
                ElMessage.warning(res.msg)
            }
        } catch (error) {
            ElMessage.error('删除失败')
        }
    }
</script>

<style lang="scss" scoped>
    .form-container {
        background: #fff;
        border-radius: 4px;
        
        // 响应式表格
        .responsive-table {
            width: 100%;
            overflow-x: auto;
            :deep(.is-vertical) {
                display: none !important;
            }
            
            // 提示文本样式
            .tip-text {
                color: #999;
                font-size: 12px;
                margin-top: 5px;
                display: block;
            }
            
            // 变量输入框
            .variable-input {
                width: 100%;
            
                .prefix {
                    display: inline-block;
                    padding: 0 5px;
                    color: #666;
                }
            }
            
            // 变量名显示
            .variable-name {
                word-break: break-all;
            }
            
            // 操作列
            .action-column {
                .action-buttons {
                    display: flex;
                    gap: 10px;
                    
                    .el-button {
                        padding: 0;
                        height: auto;
                    }
                }
            }
        }
        
        // 提交按钮区域
        .submit-area {
            margin: 20px 0;
            text-align: center;
        }
    }

    /* 移动端适配 */
    @media (max-width: 768px) {
        .form-container {
            padding: 10px;
            
            .responsive-table {
                :deep(.el-table__body-wrapper) {
                    overflow-x: scroll;
                }
                
                :deep(.el-table__cell) {
                    min-width: 120px !important;
                    padding: 8px 0;
                }
            }
            
            .submit-area {
                margin: 15px 0;
            
                .el-button {
                    width: 100%;
                }
            }
        }
    }
</style>