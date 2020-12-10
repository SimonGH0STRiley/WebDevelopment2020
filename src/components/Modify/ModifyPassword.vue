<template>
	<div class="modify-password">
		<b-form label-width="100px" @submit.prevent="submitForm">
			<div class="old-password-group">
				<b-row class="old-password-group" :class="{'form-group--error': $v.oldPassword.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="key"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" :type="oldPasswordStatus?'password':'text'" placeholder="请输入旧密码" v-model.trim="$v.oldPassword.$model" auto-complete="off"></b-form-input>
						<b-input-group-append>
							<b-button variant="outline-secondary" @mousedown="showOldPassword" @mouseup="hideOldPassword">
								<b-icon icon="eye-fill" v-if="!oldPasswordStatus"></b-icon>
								<b-icon icon="eye-slash-fill" v-if="oldPasswordStatus"></b-icon>
							</b-button>
						</b-input-group-append>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.oldPassword.$error && !$v.oldPassword.required">必须输入旧密码</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.oldPassword.$error && !$v.oldPassword.minLength">旧密码不少于6位</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.oldPassword.$error && !$v.oldPassword.passwordRule">旧密码必须包含两个数字，必须包含一个大写和小写字母</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="isOldPasswordCorrect === -1">旧密码不正确</b-col></b-row>
				<br/>
			</div>
			<div class="password-group">
				<b-row class="password-group" :class="{'form-group--error': $v.password.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="key-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" :type="passwordStatus?'password':'text'" placeholder="请输入新密码" v-model.trim="$v.password.$model" auto-complete="off"></b-form-input>
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
			<div class="duplicated-password-group">
				<b-row class="duplicated-password-group" :class="{'form-group--error': $v.duplicatedPassword.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="key-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" :type="passwordStatus?'password':'text'" placeholder="请再次输入新密码" v-model.trim="$v.duplicatedPassword.$model" auto-complete="off"></b-form-input>
						<b-input-group-append>
							<b-button variant="outline-secondary" @mousedown="showPassword" @mouseup="hidePassword">
								<b-icon icon="eye-fill" v-if="!passwordStatus"></b-icon>
								<b-icon icon="eye-slash-fill" v-if="passwordStatus"></b-icon>
							</b-button>
						</b-input-group-append>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.duplicatedPassword.$error && !$v.duplicatedPassword.required">必须再次输入密码</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.duplicatedPassword.$error && !$v.duplicatedPassword.sameAsPassword">两次输入的密码请保持一致</b-col></b-row>
				<br/>
			</div>
			<div class="login-button">
				<b-row>
					<b-col offset="3" cols="2">
						<b-button variant="info" type="submit" :disabled="modifyStatus==='PENDING'">
							<b-icon icon="cloud-upload-fill"></b-icon>
						</b-button>
					</b-col>
					<b-col offset="2" cols="2">
						<b-button variant="warning" @click="resetForm">
							<b-icon icon="trash-fill"></b-icon>
						</b-button>
					</b-col>
				
				</b-row>
			</div>
		</b-form>
	</div>
</template>

<script>
import {required, minLength, sameAs} from 'vuelidate/lib/validators';
import {passwordRule} from "@/Validator";

export default {
	name: 'ModifyPassword',
	data() {
		return {
			modifyStatus: null,
			oldPasswordStatus: true,
			passwordStatus: true,
			oldPassword: '',
			password: '',
			duplicatedPassword: '',
			isOldPasswordCorrect: 0
			// isOldPasswordCorrect 0->未解析 1->正确 -1->错误
		};
	},
	
	validations: {
		// TODO: 防止SQL注入攻击
		username: {
			required
		},
		oldPassword: {
			required,
			minLength: minLength(6),
			passwordRule
		},
		password: {
			required,
			minLength: minLength(6),
			passwordRule
		},
		duplicatedPassword: {
			required,
			sameAsPassword: sameAs('password')
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
			this.oldPassword = '';
			this.password = '';
			this.duplicatedPassword = '';
		},
		showOldPassword() {
			this.oldPasswordStatus = false;
		},
		hideOldPassword() {
			this.oldPasswordStatus = true;
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
	border-color: #f04124; }

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
