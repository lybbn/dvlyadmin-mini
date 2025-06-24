<!--
 * @Descripttion: 文件导入
 * @version: 1.0
 * @Author: lybbn
 * @Program: dvlyadmin-mini
 * @Edit Date: 2025-06-21
-->

<template>
    <slot :open="open">
        <el-button type="primary" @click="open" icon="Upload" title="导入"></el-button>
    </slot>
    <el-dialog 
        v-model="dialog" 
        title="导入" 
        :width="550" 
        :close-on-click-modal="false" 
        append-to-body 
        destroy-on-close
        >
        <el-progress 
            v-if="loading" 
            :text-inside="true" 
            :stroke-width="20" 
            :percentage="percentage" 
            style="margin-bottom: 15px;"
        />
        <div v-loading="loading">
            <el-upload 
            ref="uploader"
            drag
            :accept="accept"
            :max-size="maxSize"
            :limit="1"
            :data="data"
            :show-file-list="false"
            :http-request="request"
            :before-upload="before"
            :on-progress="progress"
            :on-success="success"
            :on-error="error"
            >
            <slot name="uploader">
                <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
                <div class="el-upload__text">
                将文件拖到此处或 <em>点击选择文件上传</em>
                </div>
            </slot>
            <template #tip>
                <div class="el-upload__tip">
                    <template v-if="tip">{{ tip }}</template>
                    <template v-else>请上传小于或等于 {{ maxSize }}M 的 {{ accept }} 格式文件</template>
                    <p v-if="templateUrl" style="margin-top: 7px;">
                        <el-link :href="templateUrl" target="_blank" type="primary" :underline="false">
                        下载导入模板
                        </el-link>
                    </p>
                    <p v-if="!isEmpty(apiTemplateObj)" style="margin-top: 7px;">
                        <el-button type="primary" link>
                        下载导入模板
                        </el-button>
                    </p>
                </div>
            </template>
            </el-upload>
            <el-form 
                v-if="$slots.form" 
                inline 
                label-width="100px" 
                label-position="left" 
                style="margin-top: 18px;"
                >
                <slot name="form" :formData="formData"></slot>
            </el-form>
        </div>
    </el-dialog>
</template>

<script setup>
    import { ref } from 'vue'
    import { ElMessage, ElNotification } from 'element-plus'
    import { UploadFilled } from '@element-plus/icons-vue'
    import { isEmpty } from '@/utils/util'

    const props = defineProps({
        apiObj: { type: Object, default: () => ({}) },
        apiTemplateObj: { type: Object, default: () => ({}) },
        data: { type: Object, default: () => ({}) },
        accept: { type: String, default: ".xls, .xlsx" },
        maxSize: { type: Number, default: 10 },
        tip: { type: String, default: "" },
        templateUrl: { type: String, default: "" }
    })

    const emit = defineEmits(['success'])

    const dialog = ref(false)
    const loading = ref(false)
    const percentage = ref(0)
    const formData = ref({})
    const uploader = ref(null)

    const open = () => {
        dialog.value = true
        formData.value = {}
    }

    const close = () => {
        dialog.value = false
    }

    const before = (file) => {
        const maxSize = file.size / 1024 / 1024 < props.maxSize
        if (!maxSize) {
            ElMessage.warning(`上传文件大小不能超过 ${props.maxSize}MB!`)
            return false
        }
        loading.value = true
        return true
    }

    const progress = (e) => {
        percentage.value = e.percent
    }

    const success = (res, file) => {
        uploader.value.handleRemove(file)
        uploader.value.clearFiles()
        loading.value = false
        percentage.value = 0
        emit('success', res, close)
    }

    const error = (err) => {
        loading.value = false
        percentage.value = 0
        ElNotification.error({
            title: '上传文件未成功',
            message: err.message || err
        })
    }

    const request = (param) => {
        const requestData = {
            ...param.data,
            ...formData.value
        }
        
        const data = new FormData()
        data.append(param.filename, param.file)
        
        for (const key in requestData) {
            data.append(key, requestData[key])
        }
        
        props.apiObj.post(data, {
            onUploadProgress: e => {
            const complete = parseInt(((e.loaded / e.total) * 100) | 0, 10)
            param.onProgress({ percent: complete })
            }
        }).then(res => {
            param.onSuccess(res)
        })
        .catch(err => {
            param.onError(err)
        })
    }
</script>

<style scoped>
    .el-upload__tip {
        font-size: 12px;
        color: var(--el-text-color-secondary);
        margin-top: 7px;
    }
</style>