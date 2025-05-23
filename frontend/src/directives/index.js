import { dragDirective } from './customDirectives';

/**
 * 导出指令方法：v-xxx
 * @methods dragDirective 用户权限指令，用法：v-drag
 */
export function directive(app) {
	// 拖拽自定义
	dragDirective(app);
}