<template>
	<div v-if="usercolumn.length > 0" class="setting-column" v-loading="isSave">
		<div class="setting-column__title">
			<span class="move_b"></span>
			<span class="show_b">显示</span>
			<span class="name_b">名称</span>
			<span class="width_b">宽度</span>
			<!-- <span class="sortable_b">排序</span> -->
			<span class="fixed_b">固定</span>
		</div>
		<div class="setting-column__list" ref="list">
			<ul>
				<li v-for="item in usercolumn" :key="item.prop">
					<span class="move_b">
						<el-tag class="move" style="cursor: move;">
							<el-icon style="width: 1em; height: 1em;cursor: move;">
								<DCaret />
							</el-icon>
						</el-tag>
					</span>
					<span class="show_b">
						<el-switch v-model="item.hide" :active-value="false" :inactive-value="true"></el-switch>
					</span>
					<span class="name_b" :title="item.prop">{{ item.label }}</span>
					<span class="width_b">
						<el-input v-model="item.width" placeholder="auto" size="small"></el-input>
					</span>
					<!-- <span class="sortable_b">
						<el-switch v-model="item.sortable"></el-switch>
					</span> -->
					<span class="fixed_b">
						<el-switch v-model="item.fixed"></el-switch>
					</span>
				</li>
			</ul>
		</div>
		<div class="setting-column__bottom">
			<el-button @click="backDefaul" :disabled="isSave">重置</el-button>
			<el-button @click="save" type="primary">保存</el-button>
		</div>
	</div>
	<el-empty v-else description="暂无可配置的列" :image-size="80"></el-empty>
</template>

<script setup>
	import { ref, reactive, watchEffect, onMounted } from 'vue'
	import Sortable from 'sortablejs'
	import { DCaret } from '@element-plus/icons-vue'

	// Props
	const props = defineProps({
		column: {
			type: Array,
			default: () => []
		}
	})

	// Emits
	const emit = defineEmits(['userChange', 'back', 'save'])

	// Data
	const isSave = ref(false)
	const usercolumn = ref(JSON.parse(JSON.stringify(props.column || [])))

	// Watcher for usercolumn changes
	watchEffect(() => {
		emit('userChange', usercolumn.value)
	})

	// Mounted
	onMounted(() => {
		if (usercolumn.value.length > 0) {
			rowDrop()
		}
	})

	// Methods
	function rowDrop() {
		const tbody = list.value.querySelector('ul')
		Sortable.create(tbody, {
			handle: '.move',
			animation: 300,
			ghostClass: 'ghost',
			onEnd({ newIndex, oldIndex }) {
				const tableData = usercolumn.value
				const currRow = tableData.splice(oldIndex, 1)[0]
				tableData.splice(newIndex, 0, currRow)
			}
		})
	}

	function backDefaul() {
		emit('back', usercolumn.value)
	}

	function save() {
		emit('save', usercolumn.value)
	}

	const list = ref(null)

	defineExpose({
      	isSave,
		usercolumn
    })
</script>

<style scoped>
	.setting-column {
	}

	.setting-column__title {
		border-bottom: 1px solid #eb eef5;
		padding-bottom: 15px;
	}
	.setting-column__title span {
		font-weight: bold;
		color: #909399;
		font-size: 12px;
		display: inline-block;
	}
	.setting-column__title span.move_b {
		width: 40px;
		margin-right: 15px;
	}
	.setting-column__title span.show_b {
		width: 60px;
	}
	.setting-column__title span.name_b {
		width: 190px;
	}
	.setting-column__title span.width_b {
		width: 60px;
		margin-right: 15px;
	}
	.setting-column__title span.sortable_b {
		width: 60px;
	}
	.setting-column__title span.fixed_b {
		width: 60px;
	}

	.setting-column__list {
		max-height: 314px;
		overflow: auto;
	}
	.setting-column__list li {
		list-style: none;
		margin: 10px 0;
		display: flex;
		align-items: center;
	}
	.setting-column__list li > span {
		display: inline-block;
		font-size: 12px;
	}
	.setting-column__list li span.move_b {
		width: 40px;
		margin-right: 15px;
	}
	.setting-column__list li span.show_b {
		width: 60px;
	}
	.setting-column__list li span.name_b {
		width: 190px;
		white-space: nowrap;
		text-overflow: ellipsis;
		overflow: hidden;
		cursor: default;
	}
	.setting-column__list li span.width_b {
		width: 60px;
		margin-right: 15px;
	}
	.setting-column__list li span.sortable_b {
		width: 60px;
	}
	.setting-column__list li span.fixed_b {
		width: 60px;
	}
	.setting-column__list li.ghost {
		opacity: 0.3;
	}

	.setting-column__bottom {
		border-top: 1px solid #eb eef5;
		padding-top: 15px;
		text-align: right;
	}

	.dark .setting-column__title {
		border-color: var(--el-border-color-light);
	}
	.dark .setting-column__bottom {
		border-color: var(--el-border-color-light);
	}
</style>