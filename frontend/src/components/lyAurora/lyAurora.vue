<template>
	<div class="ly-aurora" aria-hidden="true">
		<span class="ly-aurora-blob b1"></span>
		<span class="ly-aurora-blob b2"></span>
		<span class="ly-aurora-blob b3"></span>
	</div>
</template>

<script setup>
// 极光光斑背景（纯 CSS 装饰层，可整组件移除，不影响任何功能）
// 强度受 --ly-aurora-opacity 控制（暗色模式自动减弱），prefers-reduced-motion 时静止
</script>

<style lang="scss" scoped>
.ly-aurora {
	position: fixed;
	inset: 0;
	/* -1：垫在所有内容之下（body 提供页面底色，#app 无背景不遮挡），避免光斑蒙在表格/卡片上 */
	z-index: -1;
	overflow: hidden;
	pointer-events: none;
}
.ly-aurora-blob {
	position: absolute;
	border-radius: 50%;
	filter: blur(128px);
	opacity: calc(var(--ly-aurora-opacity) * 0.42);
	will-change: transform;

	&.b1 {
		width: clamp(520px, 44vw, 760px);
		height: clamp(520px, 44vw, 760px);
		left: -180px;
		top: -220px;
		background: radial-gradient(circle, var(--ly-color-primary) 0%, transparent 76%);
		animation: ly-drift1 52s ease-in-out infinite alternate;
	}
	&.b2 {
		width: clamp(440px, 38vw, 680px);
		height: clamp(440px, 38vw, 680px);
		right: -180px;
		top: 10%;
		background: radial-gradient(circle, var(--ly-blue-400) 0%, transparent 76%);
		animation: ly-drift2 64s ease-in-out infinite alternate;
	}
	&.b3 {
		width: clamp(420px, 34vw, 560px);
		height: clamp(420px, 34vw, 560px);
		left: 36%;
		bottom: -260px;
		background: radial-gradient(circle, var(--ly-blue-300) 0%, transparent 78%);
		opacity: calc(var(--ly-aurora-opacity) * 0.32);
		animation: ly-drift3 58s ease-in-out infinite alternate;
	}
}
@keyframes ly-drift1 {
	to { transform: translate(64px, 42px) scale(1.05); }
}
@keyframes ly-drift2 {
	to { transform: translate(-48px, 36px) scale(0.96); }
}
@keyframes ly-drift3 {
	to { transform: translate(34px, -44px) scale(1.04); }
}
@media (prefers-reduced-motion: reduce) {
	.ly-aurora-blob { animation: none; }
}
</style>
