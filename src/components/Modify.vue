<template>
	<div class="modify">
		<b-card no-body>
			<b-tabs pills card vertical justified >
				<b-tab lazy title="修改个人信息">
					<b-card-body>
						<modify-personal-information/>
					</b-card-body>
				</b-tab>
				<b-tab lazy title="修改密码">
					<b-card-body>
						<modify-password/>
					</b-card-body>
				</b-tab>
			</b-tabs>
		</b-card>
	</div>
</template>

<script>
import ModifyPersonalInformation from "@/components/Modify/ModifyPersonalInformation";
import ModifyPassword from "@/components/Modify/ModifyPassword";

export default {
	name: "Modify",
	components: {
		ModifyPersonalInformation,
		ModifyPassword
	}
}
</script>

<style scoped>

</style>
