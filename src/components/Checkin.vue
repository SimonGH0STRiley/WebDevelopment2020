<template>
	<div class="checkin">
		<b-card border-variant="success" no-body>
			<b-tabs card justified>
				<b-tab lazy title="登录">
					<b-card-body>
						<login/>
					</b-card-body>
				</b-tab>
				<b-tab lazy title="注册">
					<b-card-body>
						<register/>
					</b-card-body>
				</b-tab>
			</b-tabs>
		</b-card>
	</div>
</template>

<script>
import Login from "@/components/Checkin/Login";
import Register from '@/components/Checkin/Register';

export default {
	name: "Checkin",
	data() {
		return {}
	},
	components: {
		Login,
		Register
	},
	methods: {
	}
}
</script>

<style scoped>

</style>
