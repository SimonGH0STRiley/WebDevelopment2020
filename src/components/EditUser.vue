<template>
	<div class="edit-user">
		<b-card border-variant="success" no-body>
			<b-tabs card justified>
				<b-tab lazy title="修改个人信息">
					<b-card-body>
						<edit-user-information/>
					</b-card-body>
				</b-tab>
				<b-tab lazy title="修改密码">
					<b-card-body>
						<edit-password/>
					</b-card-body>
				</b-tab>
			</b-tabs>
		</b-card>
	</div>
</template>

<script>
import EditUserInformation from "@/components/Edit/EditUserInformation";
import EditPassword from "@/components/Edit/EditPassword";

export default {
	name: "EditUser",
	components: {
		EditUserInformation,
		EditPassword
	}
}
</script>

<style scoped>

</style>
