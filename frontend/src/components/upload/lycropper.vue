<!--
 * @Author：lybbn
 * @Version：2.0
 * @QQ:1042594286
 * @EditDate: 2025-06-15
 * @Descripttion: Vue 3 响应式图像裁剪组件
-->
<template>
	<div class="ly-cropper-container">
		<div class="ly-cropper">
		<div class="ly-cropper__img-container">
			<img :src="src" ref="imgRef" class="cropper-image" :alt="altText" />
		</div>
		<div class="ly-cropper__controls">
			<div class="ly-cropper__dimensions">
			<h4 class="section-title">裁剪尺寸</h4>
			<div class="dimension-controls">
				<div class="dimension-input">
				<el-input-number 
					v-model="cropWidth" 
					:min="minDimension" 
					:max="maxDimension" 
					controls-position="right" 
					size="small" 
					label="宽度"
					@change="handleDimensionChange"
				/>
				</div>
				<div class="dimension-input">
				<el-input-number 
					v-model="cropHeight" 
					:min="minDimension" 
					:max="maxDimension" 
					controls-position="right" 
					size="small" 
					label="高度"
					@change="handleDimensionChange"
				/>
				</div>
				<div class="aspect-ratio-controls" v-if="showAspectRatioOptions">
				<el-button-group>
					<el-button 
					v-for="ratio in presetRatios" 
					:key="ratio.value" 
					size="small" 
					@click="setAspectRatio(ratio.value)"
					:type="currentRatio === ratio.value ? 'primary' : ''"
					>
					{{ ratio.label }}
					</el-button>
				</el-button-group>
				</div>
			</div>
			</div>
			
			<div class="ly-cropper__preview">
			<h4 class="section-title">裁剪预览</h4>
			<div class="ly-cropper__preview__img" ref="previewRef"></div>
			</div>
		</div>
		</div>
		
		<!-- <div class="ly-cropper__actions">
		<el-button size="medium" @click="handleCancel">取消</el-button>
		<el-button type="primary" size="medium" @click="handleConfirm">确认</el-button>
		</div> -->
	</div>
</template>

<script setup>
	import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
	import Cropper from 'cropperjs'
	import 'cropperjs/dist/cropper.css'

	const props = defineProps({
	src: {
		type: String, 
		required: true,
		validator: value => {
		return /\.(jpe?g|png|gif|bmp|webp)$/i.test(value)
		}
	},
	compress: {
		type: Number, 
		default: 0.8,
		validator: value => value > 0 && value <= 1
	},
	aspectRatio: {
		type: Number,
		default: NaN
	},
	altText: {
		type: String,
		default: 'Image to crop'
	},
	minDimension: {
		type: Number,
		default: 10
	},
	maxDimension: {
		type: Number,
		default: 5000
	},
	showAspectRatioOptions: {
		type: Boolean,
		default: true
	}
	})

	const emit = defineEmits(['confirm', 'cancel'])

	const imgRef = ref(null)
	const previewRef = ref(null)
	const crop = ref(null)
	const cropWidth = ref(0)
	const cropHeight = ref(0)
	const currentRatio = ref(props.aspectRatio)
	const isMobile = ref(false)

	const presetRatios = [
	{ label: '1:1', value: 1 },
	{ label: '4:3', value: 4/3 },
	{ label: '16:9', value: 16/9 },
	{ label: '自由', value: NaN }
	]

	const cropperOptions = computed(() => ({
		viewMode: 2,
		dragMode: 'move',
		responsive: true,
		restore: false,
		checkOrientation: true,
		autoCropArea: 0.8,
		movable: true,
		scalable: true,
		zoomable: true,
		rotatable: true,
		aspectRatio: props.aspectRatio,
		preview: previewRef.value,
		crop: setCropSize,
		ready: initCropSize
	}))

	const checkMobile = () => {
		isMobile.value = window.innerWidth < 768
	}

	const initCropper = () => {
		if (imgRef.value) {
			crop.value = new Cropper(imgRef.value, cropperOptions.value)
		}
	}

	const initCropSize = () => {
		if (crop.value) {
			const canvasData = crop.value.getCanvasData()
			cropWidth.value = Math.round(canvasData.width)
			cropHeight.value = Math.round(canvasData.height)
		}
	}

	const setCropSize = (e) => {
		const { width, height } = e.detail
		cropWidth.value = Math.round(width)
		cropHeight.value = Math.round(height)
	}

	const handleDimensionChange = () => {
		if (crop.value) {
			crop.value.setData({
			width: cropWidth.value,
			height: cropHeight.value
			})
		}
	}

	const setAspectRatio = (ratio) => {
		currentRatio.value = ratio
		if (crop.value) {
			crop.value.setAspectRatio(ratio)
		}
	}

	const getCropData = (cb, type = 'image/jpeg') => {
		if (crop.value) {
			cb(crop.value.getCroppedCanvas().toDataURL(type, props.compress))
		}
	}

	const getCropBlob = (cb, type = 'image/jpeg') => {
		if (crop.value) {
			crop.value.getCroppedCanvas().toBlob(
			blob => cb(blob), 
			type, 
			props.compress
			)
		}
	}

	const getCropFile = (cb, fileName = 'cropped-image.jpg', type = 'image/jpeg') => {
		getCropBlob(blob => {
			cb(new File([blob], fileName, { type }))
		}, type)
	}

	const handleConfirm = () => {
		getCropBlob(blob => {
			emit('confirm', blob)
		})
	}

	const handleCancel = () => {
		emit('cancel')
	}

	const rotate = (degrees = 90) => {
		if (crop.value) {
			crop.value.rotate(degrees)
		}
	}

	const reset = () => {
		if (crop.value) {
			crop.value.reset()
		}
	}

	watch(() => props.aspectRatio, (val) => {
		currentRatio.value = val
		if (crop.value) {
			crop.value.setAspectRatio(val)
		}
	})

	watch(() => props.src, (newVal) => {
		if (crop.value) {
			crop.value.replace(newVal)
		}
	})

	onMounted(() => {
		checkMobile()
		window.addEventListener('resize', checkMobile)
		initCropper()
	})

	onBeforeUnmount(() => {
		if (crop.value) {
			crop.value.destroy()
		}
		window.removeEventListener('resize', checkMobile)
	})

	// 暴露方法给父组件
	defineExpose({
		getCropData,
		getCropBlob,
		getCropFile,
		rotate,
		reset
	})
</script>

<style lang="scss" scoped>
	.ly-cropper-container {
		display: flex;
		flex-direction: column;
		height: 100%;
		max-width: 100%;
		overflow-y: auto;
	}

	.ly-cropper {
		display: flex;
		flex-direction: column;
		flex-grow: 1;
		gap: 20px;
		height: calc(100% - 60px);
		margin-bottom:10px;
		
		@media (min-width: 768px) {
			flex-direction: row;
		}
	}

	.ly-cropper__img-container {
		flex: 1;
		min-height: 300px;
		max-height: 70vh;
		background: #f5f7fa;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		
		.cropper-image {
			max-width: 100%;
			max-height: 100%;
			display: block;
		}
	}

	.ly-cropper__controls {
		display: flex;
		flex-direction: column;
		width: 100%;
		padding: 0 10px;
		
		@media (min-width: 768px) {
			width: 300px;
			padding: 0;
		}
	}

	.section-title {
		font-weight: normal;
		font-size: 14px;
		color: #606266;
		margin: 0 0 12px 0;
	}

	.dimension-controls {
		display: flex;
		flex-direction: column;
		gap: 12px;
		margin-bottom: 20px;
	}

	.dimension-input {
		width: 100%;
		
		:deep(.el-input-number) {
			width: 100%;
			
			.el-input__inner {
			text-align: left;
			}
		}
	}

	.aspect-ratio-controls {
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
		
		button {
			flex: 1;
			min-width: 60px;
		}
	}

	.ly-cropper__preview {
		margin-top: 20px;
		
		&__img {
			width: 100%;
			height: 200px;
			border: 1px solid #ebeef5;
			border-radius: 4px;
			overflow: hidden;
			background-color: #f5f7fa;
			background-image: linear-gradient(45deg, #ddd 25%, transparent 25%, transparent 75%, #ddd 75%, #ddd),
							linear-gradient(45deg, #ddd 25%, transparent 25%, transparent 75%, #ddd 75%, #ddd);
			background-size: 20px 20px;
			background-position: 0 0, 10px 10px;
		}
	}

	.ly-cropper__actions {
		display: flex;
		justify-content: flex-end;
		gap: 12px;
		padding: 16px 0 0;
		border-top: 1px solid #ebeef5;
		margin-top: auto;
	}

	@media (max-width: 767px) {
		.ly-cropper {
			height: auto;
		}
		
		.ly-cropper__img-container {
			min-height: 200px;
		}
		
		.ly-cropper__preview__img {
			height: 150px;
		}
	}
</style>