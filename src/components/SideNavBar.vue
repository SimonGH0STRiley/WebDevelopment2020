<template>
	<div class="side-nav-bar" >
		<b-card style="height: 100%" border-variant="primary" no-body>
			<b-card-header header-bg-variant="primary" header-text-variant="white">
				<b-icon icon="menu-button-wide-fill"></b-icon>控制台
			</b-card-header>
			<b-list-group flush>
				<b-list-group-item button class="text-left" :active="currentPanel === 'explore'" @click="changePanel('explore')">
					<b-icon icon="globe"></b-icon>探索
				</b-list-group-item>
				<b-list-group-item button class="d-flex justify-content-between align-items-center" :active="currentPanel === 'task'" @click="changePanel('task')">
					<div><b-icon icon="clipboard-data"></b-icon>我的发布</div>
					<b-badge variant="warning" pill>2</b-badge>
				</b-list-group-item>
				<b-list-group-item button class="d-flex justify-content-between align-items-center" :active="currentPanel === 'request'" @click="changePanel('request')">
					<div><b-icon icon="clipboard-check"></b-icon>我的响应</div>
					<b-badge variant="warning" pill>99+</b-badge>
				</b-list-group-item>
				<b-list-group-item button class="text-left" :active="currentPanel === 'edit'" @click="changePanel('edit')">
					<b-icon icon="pen"></b-icon>编辑个人档案
				</b-list-group-item>
			</b-list-group>
		</b-card>
	</div>
</template>

<script>
export default {
	name: "SideNavBar",
	data() {
		return {
			currentPanel: 'task'
		}
	},
	methods: {
		changePanel(panel) {
			this.currentPanel = panel;
		}
	}
}
</script>

<style scoped>

</style>
