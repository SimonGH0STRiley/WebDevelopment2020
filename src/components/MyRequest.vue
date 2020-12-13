<template>
	<div class="edit-user">
		<b-card border-variant="success" no-body>
			<b-tabs card justified>
				<b-tab lazy title="我发出的响应">
					<b-card-body>
						<request-for-requester></request-for-requester>
					</b-card-body>
				</b-tab>
			</b-tabs>
		</b-card>
	</div>
</template>

<script>
import RequestForRequester from "@/components/MyRequest/RequestForRequester";

export default {
	name: "MyRequest",
	components : {
		RequestForRequester
	}
}
</script>

<style scoped>

</style>
