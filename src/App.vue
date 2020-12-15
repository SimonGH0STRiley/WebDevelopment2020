<template>
	<div id="app">
		<b-container>
			<b-row>
				<b-col cols="12">
					<top-nav-bar :username="currentUsername"/>
				</b-col>
			</b-row>
			<b-row><br/></b-row>
			<b-row align-v="stretch">
				<b-col cols="2">
					<side-nav-bar :currentPanel="currentPanel" :isAdmin="isAdmin" @PanelSelected="switchPanel" style="height: 100%"/>
				</b-col>
				<b-col cols="10" class="main-panel">
					<router-view></router-view>
				</b-col>
			</b-row>
		</b-container>
	</div>
</template>

<script>
import TopNavBar from "@/components/TopNavBar";
import SideNavBar from "@/components/SideNavBar";
import router from "@/router";

export default {
	data() {
		let userJson = localStorage.getItem('user');
		let userObject = userJson && JSON.parse(userJson);
		return {
			currentUser: userObject,
			isLogin: Boolean(userObject),
			isAdmin: Boolean(userObject && userObject.is_superuser),
			currentUsername: userObject && userObject.username,
			currentPanel: 'explore',
		}
	},
	components: {
		TopNavBar,
		SideNavBar
	},
	// computed: {
	// 	currentUser() {
	// 		const userJson = localStorage.getItem("user");
	// 		return userJson && JSON.parse(userJson)
	// 	},
	// 	isLogin() {
	// 		return Boolean(this.currentUser);
	// 	},
	// 	currentUsername(){
	// 		const user = this.currentUser;
	// 		return user && user.username
	// 	},
	// 	isAdmin() {
	// 		let user = this.currentUser;
	// 		return Boolean(user && user.is_superuser)
	// 	}
	// },
	methods: {
		switchPanel(selectedPanel) {
			this.currentPanel = selectedPanel;
		}
	},
	beforeUpdate() {
		let userJson = localStorage.getItem('user');
		let userObject = userJson && JSON.parse(userJson);
		this.currentUser = userObject;
		this.isLogin = Boolean(userObject);
		this.isAdmin = Boolean(userObject && userObject.is_superuser);
		this.currentUsername = userObject && userObject.username;
	}
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
