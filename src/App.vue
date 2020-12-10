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
				<b-col col="2">
					<side-nav-bar style="height: 100%"/>
				</b-col>
				<b-col cols="10" class="main-panel">
					<checkin/>
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
import Checkin from "@/components/Checkin";
import Modify from "@/components/Modify";
import TopNavBar from "@/components/TopNavBar";
import SideNavBar from "@/components/SideNavBar";

export default {
	components: {
		SideNavBar,
		Checkin,
		Modify,
		TopNavBar
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
