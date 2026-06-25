import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'
import viteCompression from 'vite-plugin-compression'
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
        // 构建时生成 gzip 预压缩文件，配合后端直接返回 .gz 文件
        viteCompression({
            algorithm: 'gzip',
            ext: '.gz',
            threshold: 1024, // 大于 1KB 的文件才压缩
            deleteOriginFile: false,
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
        // cssCodeSplit: false,//不分割css
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
                        return 'vendor';
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
