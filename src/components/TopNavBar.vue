<template>
	<div class="side-bar">
		<b-navbar toggleable="lg" type="dark" variant="primary">
			<b-navbar-brand href="#">召集令</b-navbar-brand>
			
			<b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
			
			<b-collapse id="nav-collapse" is-nav>
				<b-navbar-nav>
					<b-nav-item href="#">Link</b-nav-item>
				</b-navbar-nav>
				
				<!-- Right aligned nav items -->
				<b-navbar-nav class="ml-auto">
					
					<b-nav-item-dropdown :text="username" right>
						<template #button-content>
							<b-icon icon="person"/>
						</template>
						<b-dropdown-item href="#">登出</b-dropdown-item>
						<b-dropdown-item href="#">查看个人信息</b-dropdown-item>
						<b-dropdown-item href="#">修改个人信息</b-dropdown-item>

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
