import { createApp } from 'vue'

//ElementPlus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/display.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import lyIntall from './lycustom.js'
import store from './store'
import router from './router'
import i18n from './locales/index.js'
import registerSvgIcon from '@/components/icons/index.js'
//引入注册脚本
import 'virtual:svg-icons-register';

import App from './App.vue'
const app = createApp(App);

// 自定义指令
// import directivePlugin from '@/utils/directive.js'

import Particles from "@tsparticles/vue3";
import { loadSlim } from "@tsparticles/slim";

app.use(Particles, {
    init: async engine => {
        await loadSlim(engine);
    },
});

// 注册 SVG 图标组件
registerSvgIcon(app)

app.use(ElementPlus);
app.use(i18n)
app.use(lyIntall);
app.use(store)
app.use(router);
// app.use(directivePlugin)

app.mount('#app')


