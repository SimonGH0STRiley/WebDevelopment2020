<template>
	<div class="side-nav-bar" >
		<b-card style="height: 100%" border-variant="info" no-body>
			<b-card-header header-bg-variant="info" header-text-variant="white">
				<b-icon icon="menu-button-wide-fill"></b-icon> 控制台
			</b-card-header>
			<b-list-group flush>
				<b-list-group-item button :active="currentPanel === 'checkin'"><b-icon icon="key-fill"></b-icon> Checkin</b-list-group-item>
				<b-list-group-item button :active="currentPanel === 'edit'"><b-icon icon="pen-fill"></b-icon> Edit</b-list-group-item>
			</b-list-group>
		</b-card>
	</div>
</template>

<script>
export default {
	name: "SideNavBar",
	data() {
		return {
			currentPanel: 'checkin'
		}
	}
}
</script>

<style scoped>

</style>
