import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'
import { resolve } from 'path';

const pathResolve = (dir) => {
    return resolve(__dirname, '.', dir);
};

let alias = {
    '@': pathResolve('./src/'),
}

export default defineConfig({
    plugins: [
        vue(),
        VueSetupExtend(),
        createSvgIconsPlugin({
            iconDirs: [resolve(process.cwd(), 'src/assets/lybbn/icons/svg')], // 你的 SVG 目录
            symbolId: 'icon-[name]', // 格式必须和 `iconName` 计算属性匹配
        }),
    ],
    base: '/', // index.html文件所在位置
    root: './', // js导入的资源路径，src
    minify: true, // 是否压缩代码
    server: {
        https: false,//是否开启 HTTPS
        host: true, // host: "0.0.0.0" 设置 host: true 才可以使用 Network 的形式，以 IP 访问项目
        port: 8081,
        hmr: true,
        open: false, //是否自动打开浏览器
        cors: true,  //跨域设置允许
        strictPort: true, //端口被占用时，是否直接退出
        overlay: false,
    },
    build: {
        target: 'esnext', // 允许使用顶级 await
        minify: 'terser', // 是否进行压缩,boolean | 'terser' | 'esbuild',默认使用terser
        manifest: false,
        sourcemap: false,
        outDir: 'dist',
        emptyOutDir: true, // 构建前清空输出目录
        assetsDir: 'static',
        chunkSizeWarningLimit: 2000,
        terserOptions: {
            output: {
                ecma: 2015,
                comments: false,// 移除注释
                ascii_only: true,
            },
            compress: {
                drop_console: true, // 生产环境移除console
                drop_debugger: true,
            },
            mangle: true, // 启用名称混淆
        },
        rollupOptions:{
            output:{
                entryFileNames: `static/[name].[hash].js`,
                chunkFileNames: `static/[name].[hash].js`,
                assetFileNames: `static/[name].[hash].[ext]`,
                manualChunks(id){
                    if (id.includes('node_modules')) {
                        return id.toString().split('node_modules/')[1].split('/')[0].toString();
                    }
                }
            }
        }
    },
    resolve: {
        alias,
    },
    css: {//sass2.0版本以上，消除警告
        preprocessorOptions: {
            scss: {
                api: 'modern-compiler', // or 'modern'
            },
        },
    },
})
