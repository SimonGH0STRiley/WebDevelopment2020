<template>
	<div class="edit-user-information">
		<b-form @submit.prevent="submitForm">
			<div class="username-group">
				<b-row class="username-group">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="person-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" disabled v-model="username"/>
					</b-input-group>
				</b-row>
				<br/>
			</div>
			<div class="name-group">
				<b-row class="name-group">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="file-earmark-person-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" disabled v-model="lastname"/>
						<b-form-input class="form-input" disabled v-model="firstname"/>
					</b-input-group>
				</b-row>
				<br/>
			</div>
			<div class="identity-group">
				<b-row class="identity-group">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="info-circle-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" disabled v-model="identityNumber"/>
						<b-input-group-append>
							<b-dropdown :text="identityType" disabled variant="success"></b-dropdown>
						</b-input-group-append>
					</b-input-group>
				</b-row>
				<br/>
			</div>
			<div class="phone-number-group">
				<b-row class="phone-number-group" :class="{'form-group--error': $v.phoneNumber.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="telephone-fill"></b-icon>
						</b-input-group-prepend>
						<b-input-group-prepend is-text>+86</b-input-group-prepend>
						<b-form-input class="form-input" placeholder="请输入移动电话号码" v-model.trim="$v.phoneNumber.$model"/>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.phoneNumber.$error && !$v.phoneNumber.required">必须输入移动电话号码</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.phoneNumber.$error && !$v.phoneNumber.phoneRule">请输入正确的移动电话号码</b-col></b-row>
				<br/>
			</div>
			<div class="city-group">
				<b-row class="city-group">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="geo-alt-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" disabled v-model="city"/>
						<b-input-group-append is-text>市</b-input-group-append>
					</b-input-group>
				</b-row>
				<br/>
			</div>
			<div class="description-group">
				<b-row class="description-group" :class="{'form-group--error': !$v.description.maxLength}">
					<b-form-textarea placeholder="请在此输入您小于500字的个人简介（可选）" rows="4" max-rows="8" v-model.trim="description"></b-form-textarea>
				</b-row>
				<b-row><b-col class="error" v-if="!$v.description.maxLength">个人简介请小于500字</b-col></b-row>
				<br/>
			</div>
			<div class="easter-egg-group">
				<b-row class="easter-egg-group">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="egg-fried"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" placeholder="Developer secret console" v-model="easterEgg"/>
					</b-input-group>
				</b-row>
				<br/>
			</div>
			<div class="register-button">
				<b-row>
					<b-col offset="3" cols="2">
						<b-button variant="success" type="submit" :disabled="modifyStatus === 'PENDING'">
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
import {required, maxLength} from 'vuelidate/lib/validators';
import {phoneRule} from "@/Validator";

export default {
	name: "EditUserInformation",
	data() {
		return {
			modifyStatus: null,
			username: 'SimonGHOSTRiley',
			lastname: 'Foo',
			firstname: 'Bar',
			identityNumber: '100100200911102333',
			identityType: '身份证',
			phoneNumber: '13312345678',
			city: '伦敦',
			description: 'I am Ghost.',
			easterEgg: 'WhoseYourDaddy'
		};
	},
	validations: {
		phoneNumber: {
			required,
			phoneRule
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
				this.modifyStatus = 'ERROR'
			} else {
				// TODO: finish submit logic
				this.modifyStatus = 'PENDING'
				setTimeout(() => {
					this.modifyStatus = 'OK'
				}, 500)
			}
		},
		resetForm() {
			this.modifyStatus = null;
			this.phoneNumber = '';
			this.description = '';
		},
		showPassword() {
			this.passwordStatus = false;
		},
		hidePassword() {
			this.passwordStatus = true;
		},
		changeIdentityType(type) {
			this.identityType = type;
		}
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
