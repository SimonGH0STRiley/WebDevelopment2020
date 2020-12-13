<template>
	<div class="side-bar">
		<b-navbar toggleable="lg" type="dark" variant="info">
			<b-navbar-brand href="#">召集令</b-navbar-brand>
			
			<b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
			
			<b-collapse id="nav-collapse" is-nav>
				<!-- Right aligned nav items -->
				<b-navbar-nav class="ml-auto">
					<b-nav-item-dropdown right>
						<template #button-content><b-icon icon="person"></b-icon>{{username}}</template>
						<b-dropdown-item href="#"><b-icon icon="box-arrow-right"/> Log out</b-dropdown-item>
					</b-nav-item-dropdown>
				</b-navbar-nav>
			</b-collapse>
		</b-navbar>
	</div>
</template>

<script>
export default {
	name: "TopNavBar",
	data() {
		
		return {
			username: 'SimonGHOSTRiley'
		}
	}
}
</script>

<style scoped>

</style>
