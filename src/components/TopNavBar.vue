<template>
	<div class="side-bar">
		<b-navbar toggleable="lg" type="dark" variant="info">
			<b-navbar-brand href="#">召集令</b-navbar-brand>
			<b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
			<b-collapse id="nav-collapse" is-nav>
				<!-- Right aligned nav items -->
				<b-navbar-nav class="ml-auto">
					<b-nav-item-dropdown v-if="username" right>
						<template #button-content><b-icon icon="person"></b-icon>{{ username }}</template>
						<b-dropdown-item @click="checkout"><b-icon icon="box-arrow-right"/>Log out</b-dropdown-item>
					</b-nav-item-dropdown>
				</b-navbar-nav>
			</b-collapse>
		</b-navbar>
	</div>
</template>

<script>
import router from "@/router";

export default {
	name: "TopNavBar",
	props: ['username'],
	methods: {
		checkout() {
			localStorage.removeItem('user');
			router.push('/checkin')
			this.$forceUpdate();
		}
	}
}
</script>

<style scoped>

</style>
