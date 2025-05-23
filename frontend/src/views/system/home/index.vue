<template>
    <div class="home-container" :class="isFullScreen?'lybbn-fullbg':''" ref="lybbnHome">
        <el-card shadow="never" header="" class="lybbn-bottom-10">
            <el-skeleton :rows="1" animated style="width: 100%;" :loading="is_first_loading"></el-skeleton>
            <div class="lycard-sysinfo" v-if="!is_first_loading">
                <div class="lycard-left">
                    <span :class="iconClass" class="lyiconfont">系统：</span>
                    <el-popover
                        placement="bottom"
                        :width="450"
                        trigger="hover">
                        <span>{{systemInfo.monitor.system}}</span>
                        <template #reference>
                            <span>{{systemInfo.monitor.system_simple}}</span>
                        </template>
                    </el-popover>
                    <span style="margin-left: 20px">持续运行: {{systemInfo.monitor.time}}</span>
                </div>
                <div class="lycard-center">

                </div>
                <div class="lycard-right">
                    <el-icon class="set-full-screen" @click="maxFullScreen" v-if="!isFullScreen"><FullScreen /></el-icon>
                    <el-icon class="set-full-screen" @click="handleExitFullScreen" v-if="isFullScreen"><Minus /></el-icon>
                </div>
            </div>
        </el-card>
        <el-row :gutter="10" class="lybbn-bottom-10">
            <!-- <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16"> -->
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">  
                <el-card shadow="never" header="概览" class="lycard-basic">
                    <el-skeleton :rows="1" animated style="width: 100%;" :loading="is_first_loading"></el-skeleton>
                    <el-row v-if="!is_first_loading">
                        <el-col :span="6" align="center">
                            <span>网站</span>
                            <div class="count">
                                <span @click="goPage('/websites')">{{ userState.sysConfig.siteNums }}</span>
                            </div>
                        </el-col>
                        <el-col :span="6" align="center">
                            <span>数据库</span>
                            <div class="count">
                                <span @click="goPage('/databases')">{{ userState.sysConfig.dbNums }}</span>
                            </div>
                        </el-col>
                        <el-col :span="6" align="center">
                            <span>已装应用</span>
                            <div class="count">
                                <span @click="goPage('/appstore')">{{ userState.sysConfig.softNums }}</span>
                            </div>
                        </el-col>
                        <el-col :span="6" align="center">
                            <span>安全风险</span>
                            <div class="count">
                                <!-- <span @click="goPage('/websites')">{{ systemInfo.unsafeNum }}</span> -->
                                <span style="font-size: 16px;color: #909399;">暂未开通</span>
                            </div>
                        </el-col>
                    </el-row>
                </el-card>
                <el-card shadow="never" header="状态" class="lybbn-bottom-10">
                    <el-skeleton :rows="3" animated style="width: 100%;" :loading="is_first_loading"></el-skeleton>
                    <lyRoundStatusProcess :dataStatus="systemInfo.monitor" v-if="!is_first_loading"></lyRoundStatusProcess>
                </el-card>
                <el-card shadow="never" header="监控" class="lybbn-bottom-10">
                    <template #header>
                        <div class="monitor-card-header">
                            <span>监控</span>
                            <div class="monitor-card-header-rt">
                                <el-select v-model="networkValue"  placeholder="请选择" @change="networkSelectChange" style="width: 130px;" v-if="monitorActiveTab=='network'">
                                    <el-option
                                        v-for="(value,key) in systemInfo.monitor.network_stat"
                                        :key="key"
                                        :label="key == 'ALL' ? '所有' : key"
                                        :value="key"
                                    />
                                </el-select>
                                <el-select v-model="diskiostatValue"  placeholder="请选择" @change="iostatSelectChange" style="width: 130px;" v-if="monitorActiveTab=='diskio'">
                                    <el-option
                                        v-for="(value,key) in systemInfo.monitor.diskio_stat"
                                        :key="key"
                                        :label="key == 'ALL' ? '所有' : key"
                                        :value="key"
                                    />
                                </el-select>
                                <el-radio-group v-model="monitorActiveTab" @change="handleMonitorChange" style="margin-left: 5px">
                                    <el-radio-button value="network">网络</el-radio-button>
                                    <el-radio-button value="diskio">磁盘IO</el-radio-button>
                                </el-radio-group>
                            </div>
                        </div>
                    </template>
                    <el-skeleton :rows="4" animated style="width: 100%;" :loading="is_first_loading"></el-skeleton>
                    <div v-if="!is_first_loading">
                        <div class="lymonitor-info" v-if="monitorActiveTab=='network'">
                            <div><p><span class="lyico-up"></span>上行</p><a>{{systemInfo.monitor.network_stat[networkValue].up+'KB'}}</a></div>
                            <div><p><span class="lyico-down"></span>下行</p><a>{{systemInfo.monitor.network_stat[networkValue].down+'KB'}}</a></div>
                            <div><p>总发送</p><a>{{formatUnitSize(systemInfo.monitor.network_stat[networkValue].upTotal)}}</a></div>
                            <div><p>总接收</p><a>{{formatUnitSize(systemInfo.monitor.network_stat[networkValue].downTotal)}}</a></div>
                        </div>
                        <div class="lymonitor-info" v-if="monitorActiveTab=='diskio'">
                            <div><p><span class="lyico-read"></span>读取</p><a>{{formatUnitSize(systemInfo.monitor.diskio_stat[diskiostatValue].read_bytes)}}</a></div>
                            <div><p><span class="lyico-write"></span>写入</p><a>{{formatUnitSize(systemInfo.monitor.diskio_stat[diskiostatValue].write_bytes)}}</a></div>
                            <div><p>读写/秒</p><a>{{systemInfo.monitor.diskio_stat[diskiostatValue].read_count + systemInfo.monitor.diskio_stat[diskiostatValue].write_count + '次'}}</a></div>
                            <div><p>IO延迟</p><a :style="{'color': ioDelayTime > 100 && ioDelayTime < 1000 ? '#e6a23c' : ioDelayTime >= 1000 ? 'red' : '#67c23a'}">{{ ioDelayTime + 'ms'}}</a></div>
                        </div>
                        <div v-show="monitorActiveTab=='network'" style="width: 100%;">
                            <lyLineEchart ref="networkEcharts" v-model="systemInfo.monitor.network_stat[networkValue]"></lyLineEchart>
                        </div>
                        <div v-show="monitorActiveTab=='diskio'" style="width: 100%;">
                            <lyLineEchartIostat ref="diskioEcharts" v-model="systemInfo.monitor.diskio_stat[diskiostatValue]" :is_windows="systemInfo.monitor.is_windows"></lyLineEchartIostat>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <!-- <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
                <el-card shadow="never" header="系统信息" class="lybbn-bottom-10">
                </el-card>
                <el-card shadow="never" header="推荐应用" class="lybbn-bottom-10">
                    
                </el-card>
            </el-col> -->
        </el-row>
        
    </div>
</template>
<script setup>
    import { ref,onMounted,onBeforeUnmount,nextTick } from 'vue';
    import {triggerFullScreen,exitFullScreen,formatUnitSize} from '@/utils/util'
    import lyRoundStatusProcess from "./components/lyRoundStatusProcess.vue"
    import lyLineEchart from "./components/lyLineEchart.vue"
    import lyLineEchartIostat from "./components/lyLineEchartIostat.vue"
    import { useRouter } from 'vue-router'
    import Api from "@/api/api"
    import {useUserState} from "@/store/userState";

    const userState = useUserState()

    const router = useRouter()
    let isFullScreen = ref(false)
    let loading_data_nums = ref(0)
    let is_first_loading = ref(true)
    let iconClass = ref("")
    let systemInfo = ref({
        monitor:{
            cpu: [0, 0, [0, 0, 0, 0], "", 0, 1],
            disk: [{path: "", size: ["0GB", "0GB", "0GB", 0], inodes: false}],
            is_windows: true,
            load_average: {one: 0, five: 0, fifteen: 0, max: 0, limit: 0, safe:0, percent: 0},
            mem: {percent: 0, total: 0, free: 0, used: 0},
            system: "",
            time: "0天",
            network_stat:{
                "ALL":{down:0,downPackets:0,downTotal:0,up:0,upPackets:0,upTotal:0}
            },
            diskio_stat:{
                "ALL": {read_count: 0, write_count: 0, read_bytes: 0, write_bytes: 0, read_time: 0, write_time: 0}
            }
        },
        unsafeNum:0
    })
    let timer = ref(null)
    let refreshInterval = 3
    let monitorActiveTab = ref("network")
    let networkValue = ref("ALL")
    let diskiostatValue = ref("ALL")
    let networkStatDatas = ref([])
    let diskIoStatDatas = ref([])

    let lybbnHome = ref(null)
    function maxFullScreen(){
        triggerFullScreen(lybbnHome.value)
        isFullScreen.value = true
    }

    function handleExitFullScreen(){
        exitFullScreen()
        isFullScreen.value = false
    }

    function handleFullscreenChange() {
        // 处理全屏状态变化
        isFullScreen.value = !!(document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || document.fullscreenElement); 
    }

    function goPage(path){
        router.push({ path: path });
    }

    let diskioEcharts = ref(null)
    let networkEcharts = ref(null)
    function handleMonitorChange(){
        nextTick(()=>{
            if(monitorActiveTab.value == 'network'){
                networkEcharts.value.handleResize()
            }else{
                diskioEcharts.value.handleResize()
            }
        })
    }

    function networkSelectChange(){

    }

    function iostatSelectChange(){

    }
    
    let ioDelayTime = ref(0)

    //获取监控数据
    function getMonitorData(){
        Api.getSysMonitor().then(res => {
            is_first_loading.value = false
            if(res.code ==2000) {
                systemInfo.value.monitor = res.data
                let tempsystem = res.data.system.split(" ")[0].toLowerCase()
                iconClass.value = 'ico-'+tempsystem
                let iostat = systemInfo.value.monitor.diskio_stat[diskiostatValue.value]
                ioDelayTime.value = iostat.write_time > iostat.read_time ? iostat.write_time : iostat.read_time
            }
        })
        loading_data_nums.value=loading_data_nums.value+1
    }

    function intervalMonitor(){
        timer.value = setInterval(() => {
            getMonitorData()
        },refreshInterval*1000);
    }

    function clearIntervalMonitor(){
        clearInterval(timer.value)
        timer.value = null
    }

    getMonitorData()

    onMounted(()=>{
        intervalMonitor()
        userState.getSystemConfig()
        document.addEventListener('fullscreenchange', handleFullscreenChange)
    })

    onBeforeUnmount(() => {
        clearIntervalMonitor()
        document.removeEventListener('fullscreenchange', handleFullscreenChange)
    });
</script>
<style lang="scss" scoped>
    .lybbn-fullbg{
        background-color: #f6f8f9;
    }
    .lybbn-bottom-10{
        margin-bottom: 10px;
    }
    .home-container{
        padding: 10px;
        font-size: 14px;
        .lycard-sysinfo{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            .lycard-left{
                display: flex;
                align-items: center;
                .lyiconfont{
                    display: flex;
                    align-items: center;
                }
            }
            .lycard-right{
                display: flex;
                align-items: center;
                .set-full-screen{
                    font-size: 20px;
                    cursor: pointer;
                }
            }
        }
        .lycard-basic{
            .count{
                margin-top: 10px;
                span {
                    text-align: center;
                    font-size: 25px;
                    color: var(--el-color-primary);
                    font-weight: 500;
                    line-height: 32px;
                    cursor: pointer;
                }
            }
        }
        .monitor-card-header{
            display: flex;
            align-items: center;
            justify-content: space-between;
            .monitor-card-header-rt{
                display: flex;
                align-items: center;
            }
        }
        .lymonitor-info{
            display: flex;
            align-items: center;
            justify-content: space-around;
            .lyico-up {
                width: 12px;
                height: 12px;
                border-radius: 100%;
                background-color: #4c8ff1;
                display: inline-block;
                margin-right: 3px;
            }
            .lyico-down {
                width: 12px;
                height: 12px;
                border-radius: 100%;
                background-color: #1cd798;
                display: inline-block;
                margin-right: 3px;
            }
            .lyico-read {
                width: 12px;
                height: 12px;
                border-radius: 100%;
                background-color: #447D77;
                display: inline-block;
                margin-right: 3px;
            }

            .lyico-write {
                width: 12px;
                height: 12px;
                border-radius: 100%;
                background-color: #9C7A32;
                display: inline-block;
                margin-right: 3px;
            }
        }
    }
</style>