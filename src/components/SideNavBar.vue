<template>
	<div class="side-nav-bar" >
		<b-card style="height: 100%" border-variant="primary" no-body>
			<b-card-header header-bg-variant="primary" header-text-variant="white">
				<b-icon icon="menu-button-wide-fill"></b-icon>控制台
			</b-card-header>
			<b-list-group flush>
				<b-list-group-item :to="{name: 'explore'}" class="text-left" :active="selectedPanel === 'explore'" @click="changePanel('explore')">
					<b-icon icon="globe"></b-icon>探索
				</b-list-group-item>
				<b-list-group-item :to="{name: 'task'}" class="d-flex justify-content-between align-items-center" :active="selectedPanel === 'task'" @click="changePanel('task')">
					<div><b-icon icon="clipboard-data"></b-icon>我的发布</div>
					<b-badge variant="warning" pill>2</b-badge>
				</b-list-group-item>
				<b-list-group-item :to="{name: 'request'}" class="d-flex justify-content-between align-items-center" :active="selectedPanel === 'request'" @click="changePanel('request')">
					<div><b-icon icon="clipboard-check"></b-icon>我的响应</div>
					<b-badge variant="warning" pill>99+</b-badge>
				</b-list-group-item>
				<b-list-group-item :to="{name: 'edit'}" class="text-left" :active="selectedPanel === 'edit'" @click="changePanel('edit')">
					<b-icon icon="pen"></b-icon>编辑个人档案
				</b-list-group-item>
				<b-list-group-item v-if="isAdmin" :to="{name: 'admin'}" class="text-left" :active="selectedPanel === 'admin'" @click="changePanel('admin')">
					<b-icon icon="graph-up"></b-icon>管理员报表
				</b-list-group-item>
			</b-list-group>
		</b-card>
	</div>
</template>

<script>
export default {
	name: "SideNavBar",
	props: ['currentPanel', 'isAdmin'],
	data() {
		return {
			selectedPanel: this.currentPanel
		}
	},
	methods: {
		changePanel(panel) {
			this.selectedPanel = panel;
			this.$emit('PanelSelected', this.selectedPanel)
		}
	}
}
</script>

<style scoped>

</style>
