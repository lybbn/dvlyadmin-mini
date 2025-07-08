<!--
 * @Descripttion: 富文本编辑器
 * @author：lybbn
 * @version：1.0
 * @EditDate：2025-06-24
 * @program：dvlyadmin-mini
-->
<template>
    <div class="editor-wrapper">
        <Toolbar class="editor-toolbar"
        :editor="editorRef"
        :defaultConfig="toolbarConfig"
        :mode="mode"
        />
        <Editor class="editor-content"
        v-model="editorValue"
        :defaultConfig="editorConfig"
        :mode="mode"
        @onCreated="handleCreated"
        />
    </div>
</template>

<script setup>
    import { ref, shallowRef, onBeforeUnmount,watch, readonly } from 'vue'
    import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
    import '@wangeditor/editor/dist/css/style.css'
    import {getToken} from '@/utils/util'
    import sysConfig from "@/config"
    import { ElMessage } from 'element-plus'

    // 编辑器实例，必须用 shallowRef
    const editorRef = shallowRef()

    let jwttoken = getToken()

    // 内容 HTML
    const props = defineProps({
        modelValue: {
            type: String,
            default: ''
        },
        mode: {
            type: String,
            default: 'default' // 或 'simple'
        },
        readOnly:{
            type: Boolean,
            default: false
        }
    })

    const emit = defineEmits(['update:modelValue'])

    const editorValue = ref(props.modelValue)

    // 监听内容变化
    watch(editorValue, (newVal) => {
        emit('update:modelValue', newVal)
    })

    // 监听props变化
    watch(() => props.modelValue, (newVal) => {
        if (newVal !== editorValue.value) {
            editorValue.value = newVal
        }
    })

    // 工具栏配置
    const toolbarConfig = {
        // 可配置工具栏项
        // 参考文档：https://www.wangeditor.com/v5/toolbar-config.html
        excludeKeys: [
            'group-video',
            'emotion',
            'todo',
            'codeBlock',
            'undo',
            'redo',
            'code',
            'blockquote'
        ],
    }

    // 编辑器配置
    const editorConfig = {
        placeholder: '请输入内容...',
        readOnly:props.readOnly,
        lineHeight: '1',
        // 图片上传配置
        MENU_CONF: {
            uploadImage: {
                server: sysConfig.API_URL+'/api/system/sys_image_upload/', // 你的图片上传接口
                fieldName: 'file', // 上传表单的字段名
                maxFileSize: 5 * 1024 * 1024, // 5M
                allowedFileTypes: ['image/*'],
                headers: {
                    Authorization: sysConfig.TOKEN_PREFIX + jwttoken,
                },
                // 自定义上传参数
                meta: {
                },
                // 自定义插入图片
                customInsert(res, insertFn) {
                    // res 即服务端的返回结果
                    // 从 res 中找到 url alt href ，然后插入图片
                    if (res.code === 2000) {
                        let imgpath=''
                        if (res.data.data[0].indexOf("://")>=0){
                            imgpath = res.data.data[0]

                        }else{
                            imgpath = sysConfig.API_URL+res.data.data[0]
                        }
                        insertFn(imgpath, '', '')
                    } else {
                        ElMessage.warning('上传失败: ' + res.msg)
                    }
                }
            },
            // 行高配置
            lineHeight: {
                lineHeightList: [
                    '0.5',
                    '1',
                    '1.5',
                    '2',
                    '2.5'
                ]
            }
        }
    }

    // 组件销毁时，及时销毁编辑器
    onBeforeUnmount(() => {
        const editor = editorRef.value
        if (editor == null) return
        editor.destroy()
    })

    const handleCreated = (editor) => {
        editorRef.value = editor // 记录 editor 实例
    }
</script>

<style scoped>
    .editor-wrapper {
        width:100%;
        border: 1px solid #ddd;
        border-radius: 4px;
        overflow: hidden;
    }

    .editor-toolbar {
        border-bottom: 1px solid #ddd;
    }

    .editor-content {
        min-height: 310px;
        height: 310px;
        overflow-y: auto;
    }
</style>