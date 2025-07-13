import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

// 源目录 (Vite 默认输出目录)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const distPath = path.resolve(__dirname, '../../dist');

// 目标目录列表
const targetDirs = [
    path.resolve(__dirname, '../../../backend/frontend/lyadmin'),
];

console.log('开始复制构建文件到backend...');
console.log(`源目录: ${distPath}`);

// 复制到所有目标目录
targetDirs.forEach(target => {
    try {
        fs.ensureDirSync(target); // 确保目录存在
        fs.emptyDirSync(target);  // 清空目录
        fs.copySync(distPath, target);
        console.log(`✓ 成功复制到: ${target}`);
    } catch (err) {
        console.error(`✗ 复制到 ${target} 失败:`, err.message);
    }
});

console.log('打包复制操作完成');