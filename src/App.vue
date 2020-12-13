<template>
	<div id="app">
		<b-container>
			<b-row>
				<b-col cols="12">
					<top-nav-bar/>
				</b-col>
			</b-row>
			<b-row><br/></b-row>
			<b-row align-v="stretch">
				<b-col cols="2">
					<side-nav-bar :currentPanel="currentPanel" @PanelSelected="switchPanel" style="height: 100%"/>
				</b-col>
				<b-col cols="10" class="main-panel">
					<explore v-if="currentPanel === 'explore'"/>
					<my-task v-if="currentPanel === 'task'"/>
					<my-request v-if="currentPanel === 'request'"/>
					<edit-user v-if="currentPanel === 'edit'"/>
				</b-col>
			</b-row>
		</b-container>
<!--		<h1>Django VueJs Template</h1>-->
<!--		<div id="nav">-->
<!--			<router-link :to="{ name: 'home' }">Vue</router-link> |-->
<!--			<router-link :to="{ name: 'messages' }">Django Rest</router-link>-->
<!--		</div>-->
<!--		<router-view/>-->
	</div>
</template>

<script>
import TopNavBar from "@/components/TopNavBar";
import SideNavBar from "@/components/SideNavBar";
import Checkin from "@/components/Checkin";
import Explore from "@/components/Explore";
import MyTask from "@/components/MyTask";
import MyRequest from "@/components/MyRequest";
import EditUser from "@/components/EditUser";

export default {
	data() {
		return {
			currentPanel: 'explore',
			currentUser: {
				currentUserName: '',
				currentToken: '',
				isAdmin: false,
				currentUserObject: {}
			}
		}
	},
	components: {
		TopNavBar,
		SideNavBar,
		Checkin,
		Explore,
		MyTask,
		MyRequest,
		EditUser
	},
	methods: {
		switchPanel(selectedPanel) {
			this.currentPanel = selectedPanel;
		}
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
