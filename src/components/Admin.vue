<template>
	<div class="admin">
		<b-card border-variant="success" no-body>
			<b-tabs card justified>
				<b-tab lazy title="管理员报表">
					<b-card-body>
						<admin-chart/>
					</b-card-body>
				</b-tab>
				<b-tab lazy title="管理员工具">
					<b-card-body>
						<admin-edit-password/>
					</b-card-body>
				</b-tab>
			</b-tabs>
		</b-card>
	</div>
</template>

<script>
import AdminChart from "@/components/Admin/AdminChart";
import AdminEditPassword from "@/components/Admin/AdminEditPassword";

export default {
	name: "Admin",
	data() {
		return {}
	},
	components: {
		AdminChart,
		AdminEditPassword
	},
	methods: {
	}
}
</script>

<style scoped>

</style>
