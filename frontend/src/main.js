import { createApp } from 'vue'

//ElementPlus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/display.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import lyIntall from './lycustom.js'
import router from './router'
import store from './store'

import App from './App.vue'
const app = createApp(App);

// 自定义指令
import directivePlugin from '@/utils/directive.js'

import Particles from "@tsparticles/vue3";
import { loadSlim } from "@tsparticles/slim";

app.use(Particles, {
    init: async engine => {
        await loadSlim(engine);
    },
});

app.use(ElementPlus);
app.use(lyIntall);
app.use(store)
app.use(router);
app.use(directivePlugin)

app.mount('#app')
