<template>
	<div class="login">
		<b-form @submit.prevent="submitForm">
			<div class="username-group">
				<b-row class="username-group" :class="{ 'form-group--error': $v.username.$error }">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="person-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" placeholder="请输入用户名" v-model.trim="$v.username.$model"/>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.username.$error && !$v.username.required">必须输入用户名</b-col></b-row>
				<br/>
			</div>
			<div class="password-group">
				<b-row class="password-group" :class="{ 'form-group--error': $v.password.$error }">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="key-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" :type="passwordStatus?'password':'text'" placeholder="请输入密码" v-model.trim="$v.password.$model" auto-complete="off"></b-form-input>
						<b-input-group-append>
							<b-button variant="outline-secondary" @mousedown="showPassword" @mouseup="hidePassword">
								<b-icon icon="eye-fill" v-if="!passwordStatus"></b-icon>
								<b-icon icon="eye-slash-fill" v-if="passwordStatus"></b-icon>
							</b-button>
						</b-input-group-append>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.password.$error && !$v.password.required">必须输入密码</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.password.$error && !$v.password.minLength">密码不少于6位</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.password.$error && !$v.password.passwordRule">密码必须包含两个数字，必须包含一个大写和小写字母</b-col></b-row>
				<br/>
			</div>
			<div class="login-button">
				<b-row>
					<b-col offset="3" cols="2">
						<b-button variant="success" type="submit" :disabled="loginStatus==='PENDING'">
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
import {required, minLength} from 'vuelidate/lib/validators';
import {passwordRule} from "@/Validator";
import userApi from '@/services/userService'

export default {
	name: 'Login',
	data() {
		return {
			loginStatus: null,
			passwordStatus: true,
			username: '',
			password: '',
		};
	},
	validations: {
		// TODO: 防止SQL注入攻击
		username: {
			required
		},
		password: {
			required,
		}
	},
	
	methods: {
		submitForm() {
			console.log('submit!')
			this.$v.$touch()
			if (this.$v.$invalid) {
				this.loginStatus = 'ERROR'
			} else {
				// TODO: finish submit logic
				this.loginStatus = 'PENDING'
				userApi.login(this.username, this.password)
        .then(userInfo => {
          console.log(userInfo);
        })
        .catch((err) => {
          this.loginStatus = 'ERROR'
        })
			}
		},
		resetForm() {
			this.loginStatus = null;
			this.username = '';
			this.password = '';
		},
		showPassword() {
			this.passwordStatus = false;
		},
		hidePassword() {
			this.passwordStatus = true;
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
