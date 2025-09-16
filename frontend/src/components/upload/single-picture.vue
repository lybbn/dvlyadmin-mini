<template>
	<div class="ly-upload" :class="{'ly-upload-round':round}" :style="style">
		<div v-if="file && file.status != 'success'" class="ly-upload__uploading">
			<div class="ly-upload__progress">
				<el-progress :percentage="file.percentage" :text-inside="true" :stroke-width="16"/>
			</div>
			<ly-image class="image" :src="file.tempFile" fit="cover"></ly-image>
		</div>
		<div v-if="file && file.status=='success'" class="ly-upload__img">
			<ly-image class="image" :src="file.url" :preview-src-list="[file.url]" fit="cover" hide-on-click-modal preview-teleported>
				<template #placeholder>
					<div class="ly-upload__img-slot">
						Loading...
					</div>
				</template>
			</ly-image>
			<div class="ly-upload__img-actions" v-if="!disabled">
				<span class="del" @click="handleRemove()"><el-icon><Delete /></el-icon></span>
			</div>
		</div>
		<el-upload v-if="!file" class="uploader" ref="uploader"
			:auto-upload="cropper?false:autoUpload"
			:disabled="disabled"
			:show-file-list="showFileList"
			:action="action"
			:name="name"
			:data="data"
			:accept="accept"
			:limit="1"
			:http-request="request"
			:on-change="change"
			:before-upload="before"
			:on-success="success"
			:on-error="error"
			:on-exceed="handleExceed">
			<slot>
				<div class="el-upload--picture-card" :style="style">
					<div class="file-empty">
						<el-icon><component :is="icon" /></el-icon>
						<h4 v-if="title">{{title}}</h4>
					</div>
				</div>
			</slot>
		</el-upload>
		<span style="display:none!important"><el-input v-model="value"></el-input></span>
		<el-dialog :bodyPadding="0" title="剪裁" draggable v-model="cropperDialogVisible" width="780px" @closed="cropperClosed" destroy-on-close>
			<lyCropper :src="cropperFile.tempCropperFile" :compress="compress" :aspectRatio="aspectRatio" ref="cropper"></lyCropper>
			<template #footer>
				<el-button @click="cropperDialogVisible=false" >取 消</el-button>
				<el-button type="primary" @click="cropperSave">确 定</el-button>
			</template>
		</el-dialog>
	</div>
</template>

<script>
	import { defineAsyncComponent } from 'vue'
	import { genFileId } from 'element-plus'
	const lyCropper = defineAsyncComponent(() => import('@/components/upload/lycropper.vue'))
	import Api from "@/api/api";
	import config from "@/config"
	import lyDialog from "@/components/dialog/dialog.vue"

	export default {
		emits: ['onSuccess','update:modelValue'],
		props: {
			modelValue: { type: String, default: "" },
			successCode:{ type: Number, default: 2000 },//请求完成代码
			height: {type: Number, default: 148},
			width: {type: Number, default: 148},
			title: { type: String, default: "" },
			icon: { type: String, default: "plus" },
			action: { type: String, default: "" },
			apiObj: { type: Function, default: Api.apiSysImgUpload },//上传请求API对象
			name: { type: String, default: 'file' },
			data: { type: Object, default: () => {} },
			accept: { type: String, default: "image/gif, image/jpeg, image/png" },
			maxSize: { type: Number, default: 10 },
			limit: { type: Number, default: 1 },
			autoUpload: { type: Boolean, default: true },
			showFileList: { type: Boolean, default: false },
			disabled: { type: Boolean, default: false },
			round: { type: Boolean, default: false },
			onSuccess: { type: Function, default: () => { return true } },
			cropper: { type: Boolean, default: false },
			compress: {type: Number, default: 1},
			aspectRatio:  {type: Number, default: NaN}
		},
		components: {
			lyCropper,
			lyDialog
		},
		data() {
			return {
				value: "",
				file: null,
				style: {
					width: this.width + "px",
					height: this.height + "px"
				},
				cropperDialogVisible: false,
				cropperFile: null
			}
		},
		watch:{
			modelValue(val){
				this.value = val
				this.newFile(val)
			},
			value(val){
				this.$emit('update:modelValue', val)
			}
		},
		mounted() {
			this.value = this.modelValue
			this.newFile(this.modelValue)
		},
		methods: {
			newFile(url){
				if(url){
					this.file = {
						status: "success",
						url: url
					}
				}else{
					this.file = null
				}
			},
			cropperSave(){
				this.$refs.cropper.getCropFile(file => {

					file.uid = this.cropperFile.uid
					this.cropperFile.raw = file

					this.file = this.cropperFile
					this.file.tempFile = URL.createObjectURL(this.file.raw)
					this.$refs.uploader.submit()

				}, this.cropperFile.name, this.cropperFile.type)
				this.cropperDialogVisible = false
			},
			cropperClosed(){
				URL.revokeObjectURL(this.cropperFile.tempCropperFile)
				delete this.cropperFile.tempCropperFile
			},
			handleRemove(){
				this.clearFiles()
			},
			clearFiles(){
				URL.revokeObjectURL(this.file.tempFile)
				this.value = ""
				this.file = null
				this.$nextTick(()=>{
					this.$refs.uploader.clearFiles()
				})
			},
			change(file,files){
				if(files.length > 1){
					files.splice(0, 1)
				}
				if(this.cropper && file.status=='ready'){
					const acceptIncludes = ["image/gif", "image/jpeg", "image/png"].includes(file.raw.type)
					if(!acceptIncludes){
						this.$notify.warning({
							title: '上传文件警告',
							message: '选择的文件非图像类文件'
						})
						return false
					}
					this.cropperFile = file
					this.cropperFile.tempCropperFile = URL.createObjectURL(file.raw)
					this.cropperDialogVisible = true
					return false
				}
				this.file = file
				if(file.status=='ready'){
					file.tempFile = URL.createObjectURL(file.raw)
				}
			},
			before(file){
				const acceptIncludes = this.accept.replace(/\s/g,"").split(",").includes(file.type)
				if(!acceptIncludes){
					this.$notify.warning({
						title: '上传文件警告',
						message: '选择的文件非图像类文件'
					})
					this.clearFiles()
					return false
				}
				const maxSize = file.size / 1024 / 1024 < this.maxSize;
				if (!maxSize) {
					this.$message.warning(`上传文件大小不能超过 ${this.maxSize}MB!`);
					this.clearFiles()
					return false
				}
			},
			handleExceed(files){
				const file = files[0]
				file.uid = genFileId()
				this.$refs.uploader.handleStart(file)
			},
			success(res, file){
				//释放内存删除blob
				URL.revokeObjectURL(file.tempFile)
				delete file.tempFile
				if(res){
			        var os = this.onSuccess(res, file)
                    if(os!=undefined && os==false){
						return false
					}
                    let src=''
                    if (res.data.data[0].indexOf("://")>=0){
                        src = res.data.data[0]

                    }else{
                        src = config.API_BASEURL.split('/api')[0]+res.data.data[0]
                    }
                    file.url = src
					this.value = file.url
                }
				this.$emit('onSuccess',this.value)
			},
			error(err){
				this.$nextTick(()=>{
					this.clearFiles()
				})
				this.$notify.error({
					title: '上传文件未成功',
					message: err
				})
			},
			async request(param){
				var vm = this
				var apiObj = vm.apiObj;
                let obj= await apiObj(param)
                if(obj.code == vm.successCode) {
                    param.onSuccess(obj)
                } else {
                    param.onError(obj.msg || "未知错误")
                }
			}
		}
	}
</script>

<style scoped>
	.el-form-item.is-error .ly-upload .el-upload--picture-card {
		border-color: var(--el-color-danger);
	}
	.ly-upload .el-upload--picture-card {
		border-radius: 0;
	}

	.ly-upload .uploader,.ly-upload:deep(.el-upload) {
		width: 100%;
		height: 100%;
	}

	.ly-upload__img {
		width: 100%;
		height: 100%;
		position: relative;
	}
	.ly-upload__img .image {
		width: 100%;
		height: 100%;
	}
	.ly-upload__img-actions {
		position: absolute;
		top:0;
		right: 0;
		display: none;
	}
	.ly-upload__img-actions span {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 25px;
		height:25px;
		cursor: pointer;
		color: #fff;
	}
	.ly-upload__img-actions span i {
		font-size: 12px;
	}
	.ly-upload__img-actions .del {
		background: #F56C6C;
	}
	.ly-upload__img:hover .ly-upload__img-actions {
		display: block;
	}
	.ly-upload__img-slot {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
		font-size: 12px;
		background-color: var(--el-fill-color-lighter);
	}

	.ly-upload__uploading {
		width: 100%;
		height: 100%;
		position: relative;
	}
	.ly-upload__progress {
		position: absolute;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: var(--el-overlay-color-lighter);
		z-index: 1;
		padding:10px;
	}
	.ly-upload__progress .el-progress {
		width: 100%;
	}
	.ly-upload__uploading .image {
		width: 100%;
		height: 100%;
	}

	.ly-upload .file-empty {
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
	}
	.ly-upload .file-empty i {
		font-size: 28px;
	}
	.ly-upload .file-empty h4 {
		font-size: 12px;
		font-weight: normal;
		color: #8c939d;
		margin-top: 8px;
	}

	.ly-upload.ly-upload-round {
		border-radius: 50%;
		overflow: hidden;
	}
	.ly-upload.ly-upload-round .el-upload--picture-card {
		border-radius: 50%;
	}
	.ly-upload.ly-upload-round .ly-upload__img-actions {
		top: auto;
		left: 0;
		right: 0;
		bottom: 0;
	}
	.ly-upload.ly-upload-round .ly-upload__img-actions span {
		width: 100%;
	}
</style>