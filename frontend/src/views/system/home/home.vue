<template>
    <div class="dashboard-container">
        <!-- 欢迎横幅 -->
        <div class="welcome-banner">
            <div>
                <h2><span class="grad-text">{{ greeting }}</span>，{{ userState.userInfo.name || '管理员' }}，今天也保持高效！</h2>
                <p>系统运行平稳 · 欢迎使用 {{ userState.sysConfig.systitle || config.APP_NAME }} · 距离上次备份已过去 2 小时</p>
            </div>
            <div class="welcome-date">
                <el-icon><Sunny /></el-icon>
                <div>{{ todayStr }}<br><span class="sub">{{ weekStr }}</span></div>
            </div>
        </div>

        <!-- 顶部信息卡片 -->
        <el-row :gutter="15">
            <el-col :xs="24" :sm="12" :md="6">
                <el-card shadow="hover" class="info-card">
                    <div class="card-content">
                        <div class="card-icon ic-blue">
                            <el-icon><User /></el-icon>
                        </div>
                        <div class="card-text">
                            <div class="card-value">12,345</div>
                            <div class="card-title">用户总数</div>
                            <span class="trend up"><el-icon><Top /></el-icon>较上周 +12.4%</span>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
                <el-card shadow="hover" class="info-card">
                    <div class="card-content">
                        <div class="card-icon ic-royal">
                            <el-icon><ShoppingCart /></el-icon>
                        </div>
                        <div class="card-text">
                            <div class="card-value">2,543</div>
                            <div class="card-title">订单总数</div>
                            <span class="trend up"><el-icon><Top /></el-icon>较昨日 +8.2%</span>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
                <el-card shadow="hover" class="info-card">
                    <div class="card-content">
                        <div class="card-icon ic-cyan">
                            <el-icon><PriceTag /></el-icon>
                        </div>
                        <div class="card-text">
                            <div class="card-value">876</div>
                            <div class="card-title">商品总数</div>
                            <span class="trend down"><el-icon><Bottom /></el-icon>较上月 -2.1%</span>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :md="6">
                <el-card shadow="hover" class="info-card">
                    <div class="card-content">
                        <div class="card-icon ic-ink">
                            <el-icon><Money /></el-icon>
                        </div>
                        <div class="card-text">
                            <div class="card-value">¥345,678</div>
                            <div class="card-title">总收入</div>
                            <span class="trend mut">本月稳健</span>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>

        <!-- 图表区域 -->
        <el-row :gutter="15">
            <el-col :xs="24" :sm="24" :md="16">
                <el-card shadow="hover" class="chart-card">
                    <template #header>
                        <div class="card-header">
                            <div class="card-header-title">
                                <span>访问量统计</span>
                                <span class="card-header-sub">站点访问与注册趋势</span>
                            </div>
                            <el-radio-group v-model="chartType" size="small">
                                <el-radio-button label="本周" value="week"></el-radio-button>
                                <el-radio-button label="本月" value="month"></el-radio-button>
                                <el-radio-button label="本年" value="year"></el-radio-button>
                            </el-radio-group>
                        </div>
                    </template>
                    <div id="visit-chart" style="height: 300px;"></div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="24" :md="8">
                <el-card shadow="hover" class="chart-card">
                    <template #header>
                        <div class="card-header">
                            <div class="card-header-title">
                                <span>销售占比</span>
                                <span class="card-header-sub">品类分布</span>
                            </div>
                        </div>
                    </template>
                    <div id="sale-chart" style="height: 300px;"></div>
                </el-card>
            </el-col>
        </el-row>

        <!-- 快捷操作和消息 -->
        <el-row :gutter="15">
            <el-col :xs="24" :sm="12">
                <el-card shadow="hover" class="quick-actions">
                    <template #header>
                        <div class="card-header">
                            <div class="card-header-title">
                                <span>快捷操作</span>
                                <span class="card-header-sub">一键直达高频功能</span>
                            </div>
                        </div>
                    </template>
                    <el-row :gutter="10">
                        <el-col :xs="8" :sm="6" v-for="(action,index) in quickActions" :key="action.icon">
                            <el-button class="quick-action-btn" :icon="action.icon" @click="handleQuickAction(action)" v-if="index<12">
                            {{ action.name }}
                            </el-button>
                        </el-col>
                    </el-row>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12">
                <el-card shadow="hover">
                    <template #header>
                        <div class="card-header">
                            <div class="card-header-title">
                                <span>最新消息</span>
                                <span class="card-header-sub">系统通知与提醒</span>
                            </div>
                        </div>
                    </template>
                    <el-scrollbar height="300px">
                        <div v-for="(message, index) in messages" :key="index" class="message-item">
                            <div class="message-title">{{ message.title }}</div>
                            <div class="message-time">{{ message.time }}</div>
                            <div class="message-content">{{ message.content }}</div>
                        </div>
                    </el-scrollbar>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
    import { ref, onMounted,nextTick,computed } from 'vue'
    import * as echarts from 'echarts'
    import {useUserState} from "@/store/userState";
    import { useRouter } from 'vue-router'
    import config from '@/config'

    const router = useRouter()
    const userState = useUserState()

    // 图表类型
    const chartType = ref('week')

    // 问候语与日期
    const greeting = computed(() => {
        const h = new Date().getHours()
        if (h < 6) return '凌晨好'
        if (h < 9) return '早上好'
        if (h < 12) return '上午好'
        if (h < 14) return '中午好'
        if (h < 18) return '下午好'
        return '晚上好'
    })
    const todayStr = computed(() => {
        const d = new Date()
        return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
    })
    const weekStr = computed(() => {
        return '星期' + ['日','一','二','三','四','五','六'][new Date().getDay()]
    })

    // 快捷操作
    // const quickActions = ref([
    //     { name: '新增用户', icon: 'User', action: 'addUser' },
    // ])
    let quickActions = computed(() => {
        let tmparr = []
        userState.permissions.menus.forEach(item=>{
            if(item.type == 1){
                tmparr.push({
                    name:item.name,
                    icon:item.icon,
                    action:item.web_path
                })
            }
        })
        return tmparr
    })

    // 消息列表
    const messages = ref([
        { title: '系统升级通知', time: '2025-05-15 10:30', content: '系统将于今晚凌晨2点进行升级维护，预计耗时2小时。' },
        { title: '新订单提醒', time: '2025-05-15 09:15', content: '您有5笔新订单待处理，请及时处理。' },
        { title: '库存预警', time: '2025-05-14 16:45', content: '商品"A001"库存不足，当前库存10件，请及时补货。' },
        { title: '会员活动', time: '2025-05-14 14:20', content: '新会员注册活动已上线，注册即送100积分。' },
        { title: '系统公告', time: '2025-05-13 11:10', content: '系统新增了数据导出功能，欢迎使用。' },
        { title: '消息通知', time: '2025-05-12 11:00', content: '有一个用户下载了您的应用。' },
    ])

    // 处理快捷操作
    const handleQuickAction = (action) => {
        router.push({path:action.action})
    }

    // 初始化图表
    let visitChart = null
    let saleChart = null

    // 读取当前主题的语义变量（暗色模式自适应）
    const cssVar = (name, fallback) => {
        const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim()
        return v || fallback
    }
    const chartTheme = () => ({
        axisLabel: cssVar('--ly-text-3', '#9AA3BC'),
        splitLine: document.documentElement.classList.contains('dark') ? 'rgba(255,255,255,.08)' : 'rgba(27,35,64,.06)',
        centerText: cssVar('--ly-text-1', '#1B2340'),
        donutBorder: document.documentElement.classList.contains('dark') ? 'rgba(30,37,58,.8)' : 'rgba(255,255,255,.8)'
    })

    const initCharts = () => {
        const t = chartTheme()
        // 访问量图表（品牌蓝渐变面积线）
        visitChart = echarts.init(document.getElementById('visit-chart'))
        visitChart.setOption({
            tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(255,255,255,.94)',
                borderColor: 'rgba(58,123,255,.2)',
                textStyle: { color: '#1B2340', fontSize: 12 }
            },
            legend: {
                data: ['访问量', '注册量'],
                textStyle: { color: t.axisLabel }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                axisLine: { lineStyle: { color: t.splitLine } },
                axisLabel: { color: t.axisLabel, fontSize: 11 },
                axisTick: { show: false }
            },
            yAxis: {
                type: 'value',
                splitNumber: 4,
                splitLine: { lineStyle: { color: t.splitLine } },
                axisLabel: { color: t.axisLabel, fontSize: 11 }
            },
            series: [
                {
                    name: '访问量',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    lineStyle: {
                        width: 3,
                        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                            { offset: 0, color: '#2E66E8' },
                            { offset: 1, color: '#3A7BFF' }
                        ])
                    },
                    itemStyle: { color: '#2E66E8', borderColor: '#fff', borderWidth: 2 },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: 'rgba(58,123,255,.30)' },
                            { offset: 1, color: 'rgba(108,155,255,0)' }
                        ])
                    },
                    data: [120, 132, 101, 134, 90, 230, 210]
                },
                {
                    name: '注册量',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 6,
                    lineStyle: {
                        width: 2.5,
                        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                            { offset: 0, color: '#22D2EE' },
                            { offset: 1, color: '#5CE0F5' }
                        ])
                    },
                    itemStyle: { color: '#22D2EE', borderColor: '#fff', borderWidth: 2 },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: 'rgba(34,210,238,.20)' },
                            { offset: 1, color: 'rgba(92,224,245,0)' }
                        ])
                    },
                    data: [20, 32, 21, 34, 20, 50, 40]
                }
            ]
        })

        // 销售占比图表（品牌蓝族渐变环图）
        saleChart = echarts.init(document.getElementById('sale-chart'))
        saleChart.setOption({
            tooltip: {
                trigger: 'item',
                backgroundColor: 'rgba(255,255,255,.94)',
                borderColor: 'rgba(58,123,255,.2)',
                textStyle: { color: '#1B2340', fontSize: 12 }
            },
            legend: {
                top: '5%',
                left: 'center',
                textStyle: { color: t.axisLabel }
            },
            series: [
            {
                name: '销售占比',
                type: 'pie',
                radius: ['48%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 8,
                    borderColor: t.donutBorder,
                    borderWidth: 3
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '18',
                        fontWeight: 'bold',
                        color: t.centerText
                    }
                },
                labelLine: {
                    show: false
                },
                data: [
                    { value: 1048, name: '电子产品', itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [{ offset: 0, color: '#2E66E8' }, { offset: 1, color: '#3A7BFF' }]) } },
                    { value: 735, name: '服装', itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [{ offset: 0, color: '#234FB8' }, { offset: 1, color: '#2E66E8' }]) } },
                    { value: 580, name: '食品', itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [{ offset: 0, color: '#22D2EE' }, { offset: 1, color: '#5CE0F5' }]) } },
                    { value: 484, name: '家居', itemStyle: { color: '#6C9BFF' } },
                    { value: 300, name: '其他', itemStyle: { color: '#DCE7FF' } }
                ]
            }
            ]
        })

        // 窗口大小变化时重新调整图表大小
        window.addEventListener('resize', () => {
            visitChart && visitChart.resize()
            saleChart && saleChart.resize()
        })

        // 暗色模式切换时刷新图表配色
        document.addEventListener('change', refreshChartTheme)
    }

    // 切换暗色模式后重建图表配色（html class 变化监听）
    let darkObserver = null
    const refreshChartTheme = () => {
        // 延迟一帧等 html.dark class 与变量生效
        requestAnimationFrame(() => {
            const t = chartTheme()
            if (visitChart) {
                const opt = visitChart.getOption()
                opt.legend[0].textStyle.color = t.axisLabel
                opt.xAxis[0].axisLine.lineStyle.color = t.splitLine
                opt.xAxis[0].axisLabel.color = t.axisLabel
                opt.yAxis[0].splitLine.lineStyle.color = t.splitLine
                opt.yAxis[0].axisLabel.color = t.axisLabel
                visitChart.setOption(opt)
            }
            if (saleChart) {
                const opt = saleChart.getOption()
                opt.legend[0].textStyle.color = t.axisLabel
                opt.series[0].itemStyle.borderColor = t.donutBorder
                opt.series[0].emphasis.label.color = t.centerText
                saleChart.setOption(opt)
            }
        })
    }

    onMounted(() => {
        setTimeout(() => {
            nextTick(()=>{
                initCharts()
            })
        },300)

        darkObserver = new MutationObserver(refreshChartTheme)
        darkObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
    })

    import { onBeforeUnmount } from 'vue'
    onBeforeUnmount(() => {
        darkObserver && darkObserver.disconnect()
    })

</script>

<style scoped>
    .dashboard-container {
        padding: 10px;
    }

    /* 欢迎横幅（玻璃条） */
    .welcome-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 24px;
        margin-bottom: 15px;
        border-radius: var(--ly-card-radius);
        background: var(--ly-glass-bg-soft);
        backdrop-filter: var(--ly-glass-blur);
        -webkit-backdrop-filter: var(--ly-glass-blur);
        border: 1px solid var(--ly-glass-border);
        box-shadow: var(--ly-glass-highlight), var(--ly-shadow-card);
        animation: rise-in var(--ly-duration-normal) both;
    }
    .welcome-banner h2 {font-size: 20px;font-weight: 700;letter-spacing: .3px;color: var(--ly-text-1);}
    .grad-text {
        background: var(--ly-gradient-primary);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .welcome-banner p {margin-top: 6px;font-size: 13px;color: var(--ly-text-2);}
    .welcome-date {display: flex;align-items: center;gap: 12px;font-size: 13px;color: var(--ly-text-2);line-height: 1.5;}
    .welcome-date .el-icon {font-size: 26px;color: var(--ly-color-primary);}
    .welcome-date .sub {font-size: 12px;color: var(--ly-text-3);}
    @keyframes rise-in {from {opacity: 0;transform: translateY(14px);}to {opacity: 1;transform: none;}}

    /* 信息卡片样式 */
    .info-card {
        border-radius: var(--ly-card-radius);
        animation: rise-in var(--ly-duration-normal) both;
    }
    .info-card:nth-child(1) {animation-delay: .05s;}

    .info-card :deep(.el-card__body) {
        padding: 18px 20px;
    }

    .card-content {
        display: flex;
        align-items: center;
    }

    .card-icon {
        width: 48px;
        height: 48px;
        border-radius: var(--ly-radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        color: white;
        font-size: 20px;
        flex-shrink: 0;
        transition: transform var(--ly-duration-normal);
    }
    .info-card:hover .card-icon {transform: scale(1.08) rotate(-4deg);}

    .ic-blue {background: linear-gradient(135deg, #2E66E8, #6C9BFF);box-shadow: 0 6px 14px rgba(46,102,232,.35);}
    .ic-royal {background: linear-gradient(135deg, #33406B, #4A5A96);box-shadow: 0 6px 14px rgba(51,64,107,.32);}
    .ic-cyan {background: linear-gradient(135deg, #22D2EE, #5CE0F5);box-shadow: 0 6px 14px rgba(34,210,238,.32);}
    .ic-ink {background: linear-gradient(135deg, #234FB8, #2E66E8);box-shadow: 0 6px 14px rgba(35,79,184,.32);}

    .card-text {
        flex: 1;
        min-width: 0;
    }

    .card-value {
        font-size: 24px;
        font-weight: 800;
        color: var(--ly-text-1);
        line-height: 1.15;
        letter-spacing: -.4px;
        font-variant-numeric: tabular-nums;
    }

    .card-title {
        font-size: 12.5px;
        color: var(--ly-text-2);
        margin-top: 4px;
    }

    .trend {
        display: inline-flex;
        align-items: center;
        gap: 2px;
        margin-top: 7px;
        font-size: 11.5px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 8px;
    }
    .trend .el-icon {font-size: 11px;}
    .trend.up {color: #0DA678;background: rgba(13,166,120,.1);}
    .trend.down {color: #F04461;background: rgba(240,68,97,.09);}
    .trend.mut {color: var(--ly-text-3);background: rgba(27,35,64,.05);}

    /* 图表卡片样式 */
    .chart-card {
        border-radius: var(--ly-card-radius);
        animation: rise-in var(--ly-duration-normal) .15s both;
    }

    .chart-card :deep(.el-card__body) {
        padding: 0;
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card-header-title {display: flex;flex-direction: column;}
    .card-header-title > span:first-child {font-size: 15px;font-weight: 600;color: var(--ly-text-1);}
    .card-header-sub {font-size: 12px;color: var(--ly-text-3);margin-top: 3px;}

    /* 快捷操作按钮 */
    .quick-action-btn {
        width: 100%;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80px;
        white-space: normal;
        word-break: break-all;
        padding: 5px;
        border-radius: var(--ly-radius-md);
        transition: transform var(--ly-duration-fast), box-shadow var(--ly-duration-fast), border-color var(--ly-duration-fast);
    }
    .quick-action-btn:hover {transform: translateY(-3px);box-shadow: 0 8px 20px rgba(58,123,255,.14);}

    .quick-action-btn :deep(.el-icon) {
        font-size: 20px;
        margin-bottom: 5px;
    }

    /* 消息列表样式 */
    .message-item {
        padding: 10px 0;
        border-bottom: 1px dashed var(--ly-glass-border);
        position: relative;
        padding-left: 14px;
    }
    .message-item::before {
        content: "";
        position: absolute;
        left: 0;
        top: 17px;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--ly-color-primary);
        opacity: .7;
    }

    .message-item:last-child {
        border-bottom: none;
    }

    .message-title {
        font-weight: 600;
        margin-bottom: 5px;
        color: var(--ly-text-1);
    }

    .message-time {
        font-size: 12px;
        color: var(--ly-text-3);
        margin-bottom: 5px;
    }

    .message-content {
        font-size: 13px;
        color: var(--ly-text-2);
        line-height: 1.5;
    }

    /* 响应式调整 */
    @media screen and (max-width: 768px) {
        .card-icon {
            width: 40px;
            height: 40px;
            font-size: 16px;
        }

        .card-value {
            font-size: 18px;
        }

        .welcome-banner {flex-direction: column;align-items: flex-start;gap: 10px;}

        .quick-action-btn {
            height: 70px;
            font-size: 12px;
        }

        .quick-action-btn :deep(.el-icon) {
            font-size: 16px;
        }
    }
</style>
