<!--
 * @Descripttion: 弹窗扩展组件
 * @version: 1.0
 * @program: django-vue-lyadmin mini
 * @Author: lybbn
 * @Email：1042594286@qq.com
 * @Date: 2024.01.11
 * @EditDate: 2024.01.11
-->
<template>
  <div class="ly-dialog">
    <el-dialog
      v-model="visible"
      :close-on-click-modal="closeOnClickModal"
      :title="title"
      :width="width"
      :top="top"
      :fullscreen="screeFull"
      :center="center"
      :before-close="beforeClose"
      :append-to-body="appendToBody"
      :destroy-on-close="true"
      :draggable="draggable"
      :show-close="false"
      @closed="closed"
      ref="lyDialogRef"
      >
      <template #header="{ close, titleId, titleClass }">
        <div>
          <slot name="header">
            <div :id="titleId" :class="titleClass" style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;width: 90%;">{{ title }}</div>
          </slot>
          <div class="ly-dialog__headerbtn">
            <button aria-label="fullscreen" type="button" @click="handleFullScreenClick" v-if="showFullScreen">
              <el-icon v-if="screeFull" class="el-dialog__close"><Minus /></el-icon>
              <el-icon v-else class="el-dialog__close"><full-screen /></el-icon>
            </button>
            <button aria-label="close" type="button" @click="close" v-if="showClose">
              <el-icon class="el-dialog__close"><close /></el-icon>
            </button>
          </div>
        </div>
      </template>
      <div v-loading="loading" style="height: 100%;">
        <slot></slot>
      </div>
      <template v-if="$slots.footer" #footer>
        <slot name="footer"></slot>
      </template>
    </el-dialog>
  </div>
</template>
  
<script setup>
    import { ref,watch,onMounted } from 'vue';
    import 'element-plus/es/components/dialog/style/css'
    const emits = defineEmits(['closed','onChangeFullScreen'])

    let lyDialogRef = ref(null)
    let visible = ref(false)
    let screeFull = ref(false)

    const props = defineProps({
      title: {
        type: String,
        default: ''
      },
      modelValue: {
        type: Boolean,
        default: true
      },
      width: {
        type: String,
        default: '50%'
      },
      center: {
        type: Boolean,
        default: false
      },
      top: {
        type: String,
        default: '10vh'
      },
      draggable: {
        type: Boolean,
        default: true
      },
      appendToBody: {
        type: Boolean,
        default: false
      },
      closeOnClickModal: {
        type: Boolean,
        default: false
      },
      fullscreen: {
        type: Boolean,
        default: false
      },
      showFullScreen: {
        type: Boolean,
        default: true
      },
      showClose: {
        type: Boolean,
        default: true
      },
      loading: {
        type: Boolean,
        default: false
      },
      beforeClose:Function// 关闭回调函数
    });
    
    function openDialog() {
      visible.value = true
    }

    function closeDialog() {
      visible.value = false
    }

    function closed() {
      emits('closed')
    }

    function handleFullScreenClick(){
      screeFull.value = !screeFull.value
      emits('onChangeFullScreen',screeFull.value)
    }

    function getRef(){
      return lyDialogRef.value
    }

    onMounted(()=>{
      screeFull.value = props.fullscreen
      visible.value = props.modelValue
      emits('onChangeFullScreen',screeFull.value)
    })

    watch(()=>props.modelValue,(nval)=>{
      visible.value = nval; // modelValue改变是同步子组件visible的值
    },{deep:true})
    watch(()=>props.fullscreen,(nval)=>{
      screeFull.value = nval
    },{deep:true})

    defineExpose({
      getRef
    })

</script>

<style scoped>
  .ly-dialog__headerbtn {
      position: absolute;
      top: var(--el-dialog-padding-primary);
      right: var(--el-dialog-padding-primary);
  }
  .ly-dialog__headerbtn button {
      padding: 0;
      background: transparent;
      border: none;
      outline: none;
      cursor: pointer;
      font-size: var(--el-message-close-size,16px);
      margin-left: 15px;
      color: var(--el-color-info);
  }
  .ly-dialog__headerbtn button:hover .el-dialog__close {
      color: var(--el-color-primary);
  }
  .ly-dialog:deep(.el-dialog) .el-dialog__body {
    padding: 20px;
  }
  .ly-dialog:deep(.el-dialog).is-fullscreen {
      display: flex;
      flex-direction: column;
      top:0px !important;
      left:0px !important;
      padding: 0;
  }
  .ly-dialog:deep(.el-dialog).is-fullscreen .el-dialog__header {
      border-bottom:var(--el-border);
      margin-right:0 !important;
      padding: 16px;
  }
  .ly-dialog:deep(.el-dialog).is-fullscreen .el-dialog__body {
      flex:1;
      overflow: auto;
  }
  .ly-dialog:deep(.el-dialog).is-fullscreen .el-dialog__footer {
      padding-bottom: 10px;
      border-top:var(--el-border);
      padding: 16px;
  }
</style>