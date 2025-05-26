<template>
	<div v-if="navMenus.length <= 0" style="padding:20px;">
		<el-alert title="无菜单" center type="info" :closable="false"></el-alert>
	</div>
	<template v-for="navMenu in navMenus" :key="navMenu.path">
		<el-menu-item v-if="!hasChildren(navMenu)" :index="navMenu.path" :data-id="navMenu.path" @contextmenu="handleRightClick($event, navMenu.path)">
			<!-- <a v-if="navMenu.meta && navMenu.meta.type == 'link'" :href="navMenu.path" target="_blank"
				@click.stop='() => { }'></a> -->
			<!-- <SvgIcon v-if="navMenu.meta?.icon" :icon-class="navMenu.meta?.icon"></SvgIcon> -->
			<SvgIcon v-if="navMenu.meta?.icon" :icon-class="navMenu.meta?.icon"></SvgIcon>
			<template #title>
				<span>{{ navMenu.meta.title }}</span>
			</template>
		</el-menu-item>
		<el-sub-menu v-else :index="navMenu.path" :data-id="navMenu.path" @contextmenu="handleRightClick($event, navMenu.path)">
			<template #title>
				<SvgIcon v-if="navMenu.meta?.icon" :icon-class="navMenu.meta?.icon" style="font-size:20px !important;"></SvgIcon>
				<span>{{ navMenu.meta.title }}</span>
			</template>
			<NavMenu :navMenus="navMenu.children"></NavMenu>
		</el-sub-menu>
	</template>
</template>

<script setup>
	import { computed } from 'vue'
	import SvgIcon from '@/components/icons/SvgIcon.vue'
	const props = defineProps({
		navMenus: {
			type: Array,
			default: []
		},
	})

	const emits = defineEmits(['contextmenuClick'])

	// function hasChildren(item) {
	// 	return item.children && !item.children.every(item => item.meta.hidden)
	// }

	const hasChildren = computed(() => {
		return (item) => item.children && !item.children.every(item => item.meta.hidden)
	})

	function handleRightClick(e,path){
		emits('contextmenuClick',e,path)
	}
</script>
<style scoped>
</style>
