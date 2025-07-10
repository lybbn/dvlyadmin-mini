<!--
 * @Descripttion: 富文本编辑器
 * @author：lybbn
 * @version：1.0
 * @EditDate：2025-06-24
 * @program：dvlyadmin-mini
-->
<template>
    <div class="editor-wrapper" :id="editor_id">
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
    import { ref, shallowRef, onBeforeUnmount,watch, nextTick } from 'vue'
    import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
    import '@wangeditor/editor/dist/css/style.css'
    import {getToken,generateRandomString} from '@/utils/util'
    import sysConfig from "@/config"
    import { ElMessage } from 'element-plus'

    // 编辑器实例，必须用 shallowRef
    const editorRef = shallowRef()

    let jwttoken = getToken()

    let editor_id = "weditor-"+generateRandomString(15)

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

    const emit = defineEmits(['update:modelValue','fullscreen'])

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
        scroll:true,
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

    let originalParent = ref(null)// 用于保存原始父节点

    const handleCreated = async (editor) => {
        await nextTick() // 等待下一个DOM更新周期
        editorRef.value = editor // 记录 editor 实例
        // 监听全屏
        editor.on('fullScreen', () => { 
            //获取全屏容器（WangEditor 生成的全屏遮罩层）
            const fullscreenEl = document.querySelector(`#${editor_id}.w-e-full-screen-container`);
            // 保存原始父节点（如果尚未记录）
            if (fullscreenEl && !originalParent.value) {
                originalParent.value = fullscreenEl.parentNode;
            }
            // 如果不在 body 下，则移动到 body
            if (fullscreenEl && fullscreenEl.parentNode !== document.body) {
                document.body.appendChild(fullscreenEl);
            }
        })
        editor.on('unFullScreen', () => { 
            //获取全屏容器（WangEditor 生成的全屏遮罩层）
            const fullscreenEl = document.querySelector(`#${editor_id}.editor-wrapper`);
            if (fullscreenEl && originalParent.value) {
                originalParent.value.appendChild(fullscreenEl);
                originalParent.value = null; // 清理引用
            }
        })
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
        height: 301px !important;
        overflow-y: auto;
    }
</style>