<template>
    <div class="lytabledialog">
        <LyDialog v-model="dialogVisible" :title="loadingTitle" :width="width" :before-close="handleClose"
            :fullscreen="fullscreen">
            <slot name="search"></slot>
            <el-table ref="table" border :data="tableData" :size="size" :height="height" v-loading="loadingSave">
                <el-table-column type="index" width="60" label="序号" v-if="tableIndex">
                    <template #default="scope">
                        <span v-text="getIndex(scope.$index)"></span>
                    </template>
                </el-table-column>
                <slot></slot>
            </el-table>
            <Pagination :small="true" v-bind:child-msg="pageparm" @callFather="callFather"></Pagination>
        </LyDialog>
    </div>
</template>

<script>
import Pagination from "@/components/Pagination.vue";
import LyDialog from "@/components/dialog/dialog.vue";
export default {
    emits: ['refreshData', 'closed'],
    name: "dialogTableList",
    components: { LyDialog, Pagination },
    props: {
        apiObj: { type: Function, default: null },
        params: { type: Object, default: () => { } },//网络请求的额外参数
        successCode: { type: Number, default: 2000 },//网络请求完成代码
        size: { type: String, default: "default" },
        fullscreen: { type: Boolean, default: false },
        tableIndex: { type: Boolean, default: false },
        limit: { type: Number, default: 10 },//每页条数
        height: { type: [Number,String], default: 500 },//表格高度
        width: { type: String, default: '50%' },//dialog宽度
    },
    data() {
        return {
            dialogVisible: false,
            loadingSave: false,
            loadingTitle: '',
            tableData: [],
            formInline: {
                page: 1,
                limit: this.limit,
            },
            pageparm: {
                page: 1,
                limit: this.limit,
                total: 0
            },
            formData: {},
        }
    },
    methods: {
        // 表格序列号
        getIndex($index) {
            // (当前页 - 1) * 当前显示数据条数 + 当前行数据的索引 + 1
            return (this.pageparm.page - 1) * this.pageparm.limit + $index + 1
        },
        callFather(parm) {
            this.formInline.page = parm.page
            this.formInline.limit = parm.limit
            this.getData()
        },
        handleClose() {
            this.$emit('closed')
        },
        handleOpen(params, flag) {
            this.loadingTitle = flag
            this.dialogVisible = true
            this.formData = Object.assign(this.formData, params)
            this.getData()
        },
        //获取表格数据
        getData() {
            this.loadingSave = true;
            var reqData = {
                page: this.formInline.page,
                limit: this.formInline.limit,
            }
            Object.assign(reqData, this.params, this.formData)
            //存在时间日期范围处理
            if (reqData.timerange) {
                reqData.beginAt = dateFormats(reqData.timerange[0], 'yyyy-MM-dd hh:mm:ss');
                reqData.endAt = dateFormats(reqData.timerange[1], 'yyyy-MM-dd hh:mm:ss');
                delete reqData.timerange
            }
            if (!!this.apiObj && this.apiObj != {}) {
                this.apiObj(reqData).then(res => {
                    this.loadingSave = false;
                    if (res.code == this.successCode) {
                        this.tableData = res.data.data
                        this.pageparm.page = res.data.page;
                        this.pageparm.limit = res.data.limit;
                        this.pageparm.total = res.data.total;
                    } else {
                        this.$message.warning(res.msg)
                    }
                })
            }
        },
        refresh(params){
            this.formData = Object.assign(this.formData, params)
            this.getData()
        }
    }
}
</script>
<style scoped>
.lytabledialog:deep(.el-dialog) .el-dialog__body {
    padding: 10px 20px 20px 20px;
}
</style>