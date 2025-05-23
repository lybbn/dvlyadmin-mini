/**
* 分页组件
*/
<template>
    <div class="lyPagination-page" :class="border?'lyPagination-page-border':''">
        <el-pagination class="page-box" :class="'page-box-'+position" :hide-on-single-page="hideOnSinglePage" @size-change="handleSizeChange" @current-change="handleCurrentChange" background :size="small?'small':'default'" v-model:current-page="childMsg.page" :page-sizes="pageSizes" :page-size="childMsg.limit" :layout="layout" :total="childMsg.total"></el-pagination>
    </div>
</template>
<script setup>
    import {ref, onMounted, reactive, computed} from 'vue'

    const emit = defineEmits(["callFather"])

    const props = defineProps({
        childMsg: { type: Object, default: () => {} },
        pageSizes: { type: Array, default: [10,20,30,40,50,100,200,500] },
        layout: { type: String, default: "total, sizes, prev, pager, next, jumper" },
        small: {type:Boolean, default:false},
        border: {type:Boolean, default:true},
        position:{type:String, default:"center"},
        hideOnSinglePage:{type:Boolean,default:false}
    })

    let pageparm = ref({
        page: props.childMsg.page || 1,
        limit: props.childMsg.limit || 20,
    })

    function handleSizeChange(val) {
        pageparm.value.limit = val
        pageparm.value.page = 1
        emit('callFather', pageparm.value)
    }

    function handleCurrentChange(val) {
        pageparm.value.page = val
        emit('callFather', pageparm.value)
    }

</script>

<style lang="scss" scoped>
    .lyPagination-page{
        display: flex;
        align-items: center;
        background: var(--el-fill-color-blank);
    }
    .lyPagination-page-border{
        border-bottom: 1px solid var(--el-border-color-lighter);
        border-left: 1px solid var(--el-border-color-lighter);
        border-right: 1px solid var(--el-border-color-lighter);
    }
    
    .lyPagination-page-bk{
        display: flex;
        align-items: center;
    }
    .page-box-center {
        margin: 10px auto;
    }
    .page-box-left {
        margin: 10px 0 auto;
    }
    .page-box-right {
        margin: 10px 0 10px auto;
    }
    .page-box {
        text-align: center;
        .el-pagination__editor.el-input{
            width: 70px !important;
            .el-input__inner{
                text-indent: 0 !important;
            }
        }
    }
    // 移动端样式覆盖
    @media (max-width: 992px){
        .lyPagination-page {
            :deep(.el-pagination){
                .el-pagination__total,
                .el-pagination__jump,
                .el-pagination__sizes {display: none!important;}
            }
        }
    }
</style>