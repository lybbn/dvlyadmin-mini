// 统一导入el-icon图标
import config from "./config"
import api from "@/api/api"
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { directive } from './directives';

export default {
    install(app) {
        app.config.globalProperties.$CONFIG = config;
        app.config.globalProperties.$API = api;
        // 注册全局elementplus icon组件
        for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
            app.component(key, component)
        }
        directive(app)
    }
}
