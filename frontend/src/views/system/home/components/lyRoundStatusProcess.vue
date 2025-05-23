<template>
    <el-row :gutter="10">
        <el-col :xs="xs" :sm="sm" :md="md" :lg="lg" :xl="xl" v-if="!dataStatus.is_windows" align="center">
            <el-popover
                placement="bottom"
                :width="400"
                trigger="hover">
                <div class="space-inner">
                    <div class="lycard">
                        <div class="space-header">
                            <div class="space-header-title">负载状态</div>
                        </div>
                        <div class="space-main">
                            <div class="space-main-up">
                                <div class="space-main-up-cpu">
                                    <span>最近1分钟平均负载：{{dataStatus.load_average.one}}</span>
                                    <span>最近5分钟平均负载：{{dataStatus.load_average.five}}</span>
                                    <span>最近15分钟平均负载：{{dataStatus.load_average.fifteen}}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <template #reference>
                    <el-progress type="circle" :percentage="dataStatus.load_average.percent" :stroke-width="6" :color="colors" :width="100">
                        <template #default="{ percentage }">
                            <span class="percentage-value">{{ percentage }}%</span>
                            <span class="percentage-label">负载</span>
                        </template>
                    </el-progress>
                </template>
            </el-popover>
            <div class="status-bottom-tips">
                {{ loadStatus(dataStatus.load_average.percent) }}
            </div>
        </el-col>
        <el-col :xs="xs" :sm="sm" :md="md" :lg="lg" :xl="xl" align="center">
            <el-popover
                placement="bottom"
                :width="400"
                trigger="hover">
                <div class="space-inner">
                    <div class="lycard">
                        <div class="space-header">
                            <div class="space-header-title">CPU使用率</div>
                        </div>
                        <div class="space-main">
                            <div class="space-main-up">
                                <div class="space-main-up-cpu">
                                    <span>CPU型号：{{dataStatus.cpu[3]}}</span>
                                    <span>物理CPU：{{dataStatus.cpu[5]}}颗</span>
                                    <span>物理核心：{{dataStatus.cpu[5]*dataStatus.cpu[4]}}个</span>
                                    <span>逻辑核心：{{dataStatus.cpu[1]}}个</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <template #reference>
                    <el-progress type="circle" :percentage="dataStatus.cpu[0]" :stroke-width="6" :color="colors" :width="100">
                        <template #default="{ percentage }">
                            <span class="percentage-value">{{ percentage }}%</span>
                            <span class="percentage-label">CPU</span>
                        </template>
                    </el-progress>
                </template>
            </el-popover>
            <div class="status-bottom-tips">
                {{ dataStatus.cpu[1] }} 核心
            </div>
        </el-col>
        <el-col :xs="xs" :sm="sm" :md="md" :lg="lg" :xl="xl" align="center">
            <el-popover
                placement="bottom"
                :width="400"
                trigger="hover">
                <div class="space-inner">
                    <div class="lycard">
                        <div class="space-header">
                            <div class="space-header-title">内存使用率</div>
                        </div>
                        <div class="space-main">
                            <div class="space-main-up">
                                <div class="space-main-up-cpu">
                                    <span>总共内存：{{dataStatus.mem.total}}GB</span>
                                    <span>已用内存：{{dataStatus.mem.used}}GB</span>
                                    <span>剩余内存：{{dataStatus.mem.free}}GB</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <template #reference>
                    <el-progress type="circle" :percentage="dataStatus.mem.percent" :stroke-width="6" :color="colors" :width="100">
                        <template #default="{ percentage }">
                            <span class="percentage-value">{{ percentage }}%</span>
                            <span class="percentage-label">内存</span>
                        </template>
                    </el-progress>
                </template>
            </el-popover>
            <div class="status-bottom-tips">
                {{ dataStatus.mem.used }} GB / {{ dataStatus.mem.total }}  GB
            </div>
        </el-col>
        <el-col :xs="xs" :sm="sm" :md="md" :lg="lg" :xl="xl" v-for="(item,index) in dataStatus.disk" align="center">
            <el-popover
                placement="bottom"
                :width="400"
                trigger="hover">
                <div class="space-inner">
                    <div class="lycard">
                        <div class="space-header">
                            <div class="space-header-title">硬盘使用率： {{item.path}}</div>
                        </div>
                        <div class="space-main">
                            <div class="space-main-up">
                                <div class="space-main-up-cpu">
                                    <span>总共大小：{{item.size[0]}}</span>
                                    <span>已用大小：{{item.size[1]}}</span>
                                    <span>剩余大小：{{item.size[2]}}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <template #reference>
                    <el-progress type="circle" :percentage="parseFloat(item.size[3])" :stroke-width="6" :color="colors" :width="100">
                        <template #default="{ percentage }">
                            <span class="percentage-value">{{ percentage }}%</span>
                            <span class="percentage-label">{{item.path}}</span>
                        </template>
                    </el-progress>
                </template>
            </el-popover>
            <div class="status-bottom-tips">
                {{ item.size[1] }} / {{ item.size[0] }}
            </div>
        </el-col>
    </el-row>
</template>

<script setup>
    import { ref,onMounted,watch } from 'vue';

    const props = defineProps({
        dataStatus: {
            type: Object,
            default: () => ({
                cpu: [0, 0, [0, 0, 0, 0], "Intel(R) Core(TM) i5-7500 CPU @ 3.40GHz * 1", 0, 1],
                disk: [{path: "", size: ["0GB", "0GB", "0GB", 0], inodes: false}],
                is_windows: true,
                load_average: {one: 0, five: 0, fifteen: 0, max: 0, limit: 0, safe:0, percent: 0},
                mem: {percent: 0, total: 0, free: 0, used: 0},
                system: "Windows 10 Pro (build 16299) x64 (Py3.9.8)",
            })
        },
    });

    const colors = [
        { color: '#5cb87a', percentage: 60 },
        // { color: '#1989fa', percentage: 70 },
        // { color: '#6f7ad3', percentage: 65 },
        { color: '#e6a23c', percentage: 80 },
        { color: '#f56c6c', percentage: 90 },
    ]

    function loadStatus(val) {
        if (val < 30) {
            return "运行流畅"
        }
        if (val < 70) {
            return "运行正常"
        }
        if (val < 80) {
            return "运行缓慢"
        }
        return "运行堵塞"
    }

    let xs=ref(12) 
    let sm=ref(12)
    let md=ref(6)
    let lg=ref(6)
    let xl=ref(6)

    function calcLayout(){
        if(props.dataStatus.is_windows && (props.dataStatus.disk.length==3 || props.dataStatus.disk.length==4)){
            lg.value=4
            xl.value=4
        }else if(!props.dataStatus.is_windows && (props.dataStatus.disk.length==2 || props.dataStatus.disk.length==3)){
            lg.value=4
            xl.value=4
        }else{
            lg.value=6
            xl.value=6
        }
    }

    watch(()=>props.dataStatus,(nval)=>{
        calcLayout()
    },{deep:true})

</script>

<style scoped>
    .percentage-value {
        display: block;
        margin-top: 10px;
        font-size: 23px;
    }
    .percentage-label {
        display: block;
        margin-top: 10px;
        font-size: 14px;
    }
    .status-bottom-tips{
        margin-top: 10px;
    }
    .space-inner{
    }
    .lycard{
        background: var(--el-bg-color);
        /*box-shadow: var(--el-box-shadow-light);*/
        border: 1px solid var(--el-border-color-light);
    }
    .space-header{
        border-bottom: 1px solid var(--el-color-info-light-7);
        font-size: 14px;
        padding: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .space-header-title{
        padding: 8px 0;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        margin-left: 10px;
    }
    .space-main{
        padding: 20px;
    }
    .space-main-up{
        display: flex;
        align-items: center;
        column-gap: 20px;
        /*justify-content: space-around;*/
    }
    .space-main-up-cpu{
        font-size: 12px;
        display: flex;
        flex-direction: column;
        line-height: 20px;
        /*width: 200px;*/
        color: #666666;
    }
    ::v-deep(.el-col) {
        margin-bottom: 11px;
    }
</style>