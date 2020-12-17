<template>
	<div class="new-request">
		<b-form @submit.prevent="submitForm">
			<div class="task-name-group">
				<b-row class="task-name-group">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="kanban-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" disabled v-model="taskName"/>
					</b-input-group>
				</b-row>
				<br/>
			</div>
			<div class="description-group">
				<b-row class="description-group" :class="{'form-group--error': !$v.description.maxLength}">
					<b-form-textarea placeholder="请在此输入您小于500字的召集令简介（可选）" rows="4" max-rows="8" v-model.trim="description"></b-form-textarea>
				</b-row>
				<b-row><b-col class="error" v-if="!$v.description.maxLength">个人简介请小于500字</b-col></b-row>
				<br/>
			</div>
			<div class="new-request-button">
				<b-row>
					<b-col offset="3" cols="2">
						<b-button variant="success" type="submit" :disabled="newRequestStatus === 'PENDING'">
							<b-icon icon="check-circle-fill"></b-icon>
						</b-button>
					</b-col>
					<b-col offset="2" cols="2">
						<b-button variant="danger" @click="resetForm">
							<b-icon icon="trash-fill"></b-icon>
						</b-button>
					</b-col>
				</b-row>
			</div>
		</b-form>
	</div>
</template>

<script>
import { maxLength, required } from "vuelidate/lib/validators";
import requestService from "@/services/requestService";

export default {
	name: "NewRequest",
	props: ['content'],
	data() {
		return {
			newRequestStatus: null,
			taskName: this.content.name,
			taskID: this.content.id,
			description: ''
		}
	},
	validations: {
		taskName: {
			required,
		},
		description: {
			maxLength: maxLength(500)
		}
	},
	methods: {
		submitForm() {
			console.log('submit!')
			this.$v.$touch()
			if (this.$v.$invalid) {
				this.newRequestStatus = 'ERROR'
			} else {
				this.newRequestStatus = 'PENDING'
				
				requestService.createRequest({task: this.taskID, info: this.description})
				.then(taskRequest => {
					alert("北京申奥成功了！");
					this.$emit('NewedRequest', taskRequest);
				})
				.catch(err => {
					console.log(err.response.data)
					if (err.response.data['non_field_errors'][0] === 'The fields task, creator must make a unique set.') {
						alert('那里不可以哦');
					} else {
						alert('这是技术性调整 不要害怕');
					}
				})
			}
		},
		resetForm() {
			this.newRequestStatus = null;
			this.description = '';
		},
	}
}
</script>

<style scoped>
.form-label {
	width: 25px;
	justify-content: center;
}
.form-group--alert, .form-group--error {
	animation-name: shakeError;
	animation-fill-mode: forwards;
	animation-duration: .6s;
	animation-timing-function: ease-in-out;
}
.form-group--error .form-label, .error {
	color: #f04124;
}
.form-group--error .form-input{
	border-color: #f04124;
}
@keyframes shakeError {
	0% {
		transform: translateX(0); }
	15% {
		transform: translateX(0.375rem); }
	30% {
		transform: translateX(-0.375rem); }
	45% {
		transform: translateX(0.375rem); }
	60% {
		transform: translateX(-0.375rem); }
	75% {
		transform: translateX(0.375rem); }
	90% {
		transform: translateX(-0.375rem); }
	100% {
		transform: translateX(0); } }
</style>
