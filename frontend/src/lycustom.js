// 统一导入el-icon图标
import config from "./config"
import api from "@/api/api"
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import directives from '@/utils/directive.js';
import lyTable from "@/components/lyTable/index.vue";
import lyImage from '@/components/image/lyImage.vue';
import lyImg from '@/components/image/lyImg.vue';

export default {
    install(app) {
        app.config.globalProperties.$CONFIG = config;
        app.config.globalProperties.$API = api;
        // 注册全局elementplus icon组件
        for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
            app.component(key, component)
        }
        app.use(directives)
        app.component("ly-table", lyTable);
        app.component("ly-image", lyImage);
        app.component("ly-img", lyImg);
    }
}
