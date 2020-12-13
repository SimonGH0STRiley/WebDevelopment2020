<template>
	<div class="explore">
		<b-card border-variant="success">
			<task-for-explore/>
		</b-card>
	</div>
</template>

<script>
import TaskForExplore from "@/components/Explore/TaskForExplore";
export default {
	name: "Explore",
	data() {
		return {};
	},
	components: {
		TaskForExplore
	}
}
</script>

<style scoped>

</style>
