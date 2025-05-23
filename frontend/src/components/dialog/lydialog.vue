<!--
 * @Descripttion: 自定义弹窗组件
 * @Program: django-vue-lyadmin
 * @version: 1.0
 * @Author: lybbn
 * @Date: 2024年08月07日
 * @EditDate: 2024年08月07日
-->
<template>
	<div class="lydialog-wrapper" v-if="!hidden">
		<div :class="['dialog-wrap', {'radius': borderRadius}, {'willclose': willclose}, {'goup': buttonReverse}]" :style="{'width': width + 'px'}">
			<div :class="['box-header', {'hidden': !showHeaderBg}]" v-if="showHeader">
				<div class="title">{{title}}</div>
                <div class="btn-close" v-if="showCloseBtn" @click="closeDialog">
					<el-icon class="icon"><Close /></el-icon>
				</div>
			</div>
			<div class="box-body" :style="{'height': height + 'px'}">
				<slot></slot>
			</div>
			<div :class="['box-footer', {'hidden': !showFooterBg}, {'reverse': buttonReverse}]" v-if="!hideFooter">
				<button class="btn btn-primary" @click="$emit('confirm')" v-if="showConfrim">{{confirmText}}</button>
				<button class="btn btn-gray" @click="$emit('cancel')" v-if="showCancel">{{cancelText}}</button>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
        emits: ['confirm','cancel'],
		props: {
			hidden: true,
			title: String,
			width: {
				type: Number,
				default: 880
			},
			height: {
				type: Number,
				default: 500
			},
			showHeader: {
				type: Boolean,
				default: true
			},
			showHeaderBg: {
				type: Boolean,
				default: true
			},
			hideFooter: {
				type: Boolean,
				default: true
			},
			showFooterBg: {
				type: Boolean,
				default: true
			},
			showConfrim: {
				type: Boolean,
				default: true
			},
			showCancel: {
				type: Boolean,
				default: true
			},
			confirmText: {
				type: String,
				default: '确定'
			},
			cancelText: {
				type: String,
				default: '取消'
			},
			buttonReverse: {
				type: Boolean,
				default: false
			},
			borderRadius: false,
			showCloseBtn: {
				type: Boolean,
				default: true
			}
		},
		data() {
			return {
				willclose: false
			}
		},
		methods: {
			closeDialog() {
				this.willclose = true;
				setTimeout(() => {
					this.willclose = false;
					this.$emit('close');
				}, 100);
			}
		}
	}
</script>

<style lang="scss">
	.lydialog-wrapper {
		z-index: 9999;
		background-color: var(--el-overlay-color-lighter);
		position: fixed;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
		display: flex;
        align-items: center;
		justify-content: center;

		.dialog-wrap {
			background-color: #fff;
			border-radius: 2px;
			overflow: hidden;
			animation: dialog-open .3s forwards;
			
			&.radius {
				border-radius: 5px;
			}

			@keyframes dialog-open {
				from {
					transform: translateY(-5%);
				}

				to {
					transform: translateY(0);
				}
			}

			&.willclose {
				animation: dialog-close .2s forwards;
			}

			@keyframes dialog-close {
				to {
					opacity: .1;
					transform: translateY(-20%);
				}
			}

			&.goup {
				margin-top: -20%;
			}

			.box-header {
				padding: 14px 20px;
				background-color: #f5f5f5;
				display: flex;
                align-items: center;
				justify-content: space-between;

				&.hidden {
					background-color: var(--ly-bg-color);
				}

				.title {
					font-size: 18px;
					font-weight: 400;
					color: #424242;
				}

				.btn-close {
                    display: flex;
                    align-items: center;
                    padding: 3px;
					text-align: center;
					color: #757575;
					cursor: pointer;
					transition: all .2s;
					border-radius: 50%;

					&:hover {
						background-color: var(--el-color-error);

						.icon {
							color: #FFFFFF;
                            animation: rotate 0.3s linear forwards;
						}
					}

					.icon {
						color: #757575;
						font-size: 17px;
						font-weight: bold;
					}

                    @keyframes rotate {
                        from {
                            transform: rotate(0deg);
                        }
                        to {
                            transform: rotate(180deg);
                        }
                    }
				}
			}

			.box-body {
				width: 100%;
				display: flex;
			}

			.box-footer {
				display: flex;
                align-items: center;
				justify-content: center;
				height: 80px;
				border-top: 1px solid var(--ly-border-color);
				background-color: var(--ly-bg-color-grey);

				&.hidden {
					border-top: none;
					background-color: var(--ly-bg-color);
				}

				&.reverse {
					margin-bottom: 20px;
					flex-direction: row-reverse;
				}

				.btn {
					width: 160px;
					height: 40px;
					margin: 0 7px;
					line-height: 40px;
					text-align: center;
					cursor: pointer;
					color: #FFFFFF;

					&.btn-primary {
						background-color: var(--el-color-primary);

						&:hover {
							opacity: .8;
						}
					}

					&.btn-gray {
						background-color: var(--ly-bg-color-gray);

						&:hover {
							background-color: #757575;
						}
					}
				}
			}
		}
	}
</style>