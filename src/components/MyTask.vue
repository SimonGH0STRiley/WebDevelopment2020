<template>
	<div class="edit-user">
		<b-card border-variant="success" no-body>
			<b-tabs card justified>
				<b-tab lazy title="新建召集令">
					<b-card-body>
						<new-task/>
					</b-card-body>
				</b-tab>
				<b-tab lazy title="修改召集令">
					<b-card-body>
						<edit-task/>
					</b-card-body>
				</b-tab>
				<b-tab lazy title="我发出的召集令">
					<b-card-body>
						<task-for-tasker/>
					</b-card-body>
				</b-tab>
				<b-tab lazy title="我收到的响应">
					<b-card-body>
						<request-for-tasker/>
					</b-card-body>
				</b-tab>
			</b-tabs>
		</b-card>
	</div>
</template>

<script>
import NewTask from "@/components/MyTask/NewTask";
import EditTask from "@/components/MyTask/EditTask";
import TaskForTasker from "@/components/MyTask/TaskForTasker";
import RequestForTasker from "@/components/MyTask/RequestForTasker";

export default {
	name: "MyTask",
	components: {
		NewTask,
		EditTask,
		TaskForTasker,
		RequestForTasker
	}
}
</script>

<style scoped>

</style>
