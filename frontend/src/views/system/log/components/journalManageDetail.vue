<template>
    <ly-dialog v-model="dialogVisible" :title="loadingTitle" width="50%" :before-close="handleClose">
        <el-form label-position="right" class="journal-detail" label-width="auto">
            <el-form-item label="请求模块：">
                <div class="detail-content">
                {{ journalDetail?.req_modular || '' }}
                </div>
            </el-form-item>
            
            <el-form-item label="请求地址：">
                <div class="detail-content">
                {{ journalDetail?.req_path || '' }}
                </div>
            </el-form-item>
            
            <el-form-item label="请求方法：">
                <div class="detail-content">
                {{ journalDetail?.req_method || '' }}
                </div>
            </el-form-item>
            
            <el-form-item label="IP地址：">
                <div class="detail-content">
                {{ journalDetail?.req_ip || '' }}
                </div>
            </el-form-item>
            
            <el-form-item label="IP归属地：">
                <div class="detail-content">
                    {{ journalDetail?.ip_area || '' }}
                </div>
            </el-form-item>
            
            <el-form-item label="请求浏览器：">
                <div class="detail-content">
                {{ journalDetail?.req_browser || '' }}
                </div>
            </el-form-item>
            
            <el-form-item label="请求数据：">
                {{journalDetail && journalDetail.req_body ? journalDetail.req_body : ''}}
            </el-form-item>
            
            <el-form-item label="响应码：">
                <el-tag :type="journalDetail?.resp_code === '2000' ? 'success' : 'warning'">
                {{ journalDetail?.resp_code || '' }}
                </el-tag>
            </el-form-item>
            
            <el-form-item label="返回信息：">
                {{journalDetail?.json_result ? journalDetail.json_result : ''}}
            </el-form-item>
            
            <el-form-item label="操作人：">
                <div class="detail-content">
                {{ journalDetail?.creator_name || '' }}
                </div>
            </el-form-item>
            
            <el-form-item label="创建时间：">
                <div class="detail-content">
                {{ journalDetail?.create_datetime || '' }}
                </div>
            </el-form-item>
        </el-form>

        <template #footer>
            <el-button @click="handleClose">关闭</el-button>
        </template>
    </ly-dialog>
</template>

<script setup>
    import { ref } from 'vue'
    import LyDialog from "@/components/dialog/dialog.vue"

    const dialogVisible = ref(false)
    const loadingTitle = ref("日志详情")
    const journalDetail = ref(null)

    const parseJson = (str) => {
        try {
            return JSON.parse(str)
        } catch {
            return str
        }
    }

    const handleClose = () => {
        dialogVisible.value = false
        journalDetail.value = null
    }

    const journalManageDetailFn = (item) => {
        journalDetail.value = item
        dialogVisible.value = true
    }

    // Expose function to parent component
    defineExpose({
        journalManageDetailFn
    })
</script>

<style scoped lang="scss">
    .journal-detail {
        :deep(.el-form-item__content) {
            background: var(--l-headertitle-bg);
            padding-left: 10px;
            word-break: break-all;
            min-height: 20px;
            line-height: 1.5;
        }

        .detail-content {
            padding: 8px;
            border-radius: 4px;
            background-color: #f5f7fa;
        }

        .json-viewer {
            margin-top: 8px;
            max-height: 300px;
            overflow: auto;
            border: 1px solid #ebeef5;
            border-radius: 4px;
            padding: 8px;
        }
    }
</style>