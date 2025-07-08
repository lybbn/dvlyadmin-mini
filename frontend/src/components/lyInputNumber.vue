<!--
 * @Descripttion: elementplus el-input-number解决传入string类型报错问题
 * @version: 1.0
 * @program: django-vue-lyadmin
 * @Author: lybbn
 * @Date: 2024.01.05
-->
<template>
    <el-input-number v-model="inputValue" @change="handleChange" :min="min" :max="max" :step="step" :precision="precision"
        :controls="controls" :controls-position="controlsPosition" :placeholder="placeholder"
        :class="textAlign ? 'lyinputnumber_textalign_left' : ''" :disabled="disabled"></el-input-number>
</template>
  
<script setup>
import { ref, computed } from 'vue';

const emits = defineEmits(['update:modelValue', 'change'])

const props = defineProps({
    modelValue: {
        type: [Number, String],
    },
    min: {
        type: Number,
    },
    max: {
        type: Number,
    },
    step: {
        type: Number,
    },
    precision: {
        type: Number,
    },
    controls: {
        type: Boolean,
        default: false
    },
    controlsPosition: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: ''
    },
    textAlign: {
        type: String,
        default: 'left',//文字位置 left 靠左（默认）、''居中
    },
    disabled: {
        type: Boolean,
        default: false
    },

});

const inputValue = computed({
    get() {
        if (typeof props.modelValue === 'string') {
            return parseFloat(props.modelValue);
        }
        return props.modelValue;
    },
    set(newValue) {
        emits('update:modelValue', newValue)
    },
})


function handleChange(e) {
    emits('change', e)
}

</script>
<style scoped>
.lyinputnumber_textalign_left:deep(.el-input__inner) {
    text-align: left;
}
</style>