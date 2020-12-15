<template>
	<div class="register">
		<b-form @submit.prevent="submitForm">
			<div class="username-group">
				<b-row class="username-group" :class="{'form-group--error': $v.username.$error}">
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
				<b-row class="password-group" :class="{'form-group--error': $v.password.$error}">
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
			<div class="duplicated-password-group">
				<b-row class="duplicated-password-group" :class="{'form-group--error': $v.duplicatedPassword.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="key-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" :type="passwordStatus?'password':'text'" placeholder="请再次输入密码" v-model.trim="$v.duplicatedPassword.$model" auto-complete="off"></b-form-input>
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
			<div class="name-group">
				<b-row class="name-group" :class="{'form-group--error': $v.lastname.$error || $v.firstname.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="file-earmark-person-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" placeholder="请输入您的姓" v-model.trim="$v.lastname.$model"/>
						<b-form-input class="form-input" placeholder="请输入您的名" v-model.trim="$v.firstname.$model"/>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.lastname.$error && !$v.lastname.required">必须输入姓</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.firstname.$error && !$v.firstname.required">必须输入名</b-col></b-row>
				<br/>
			</div>
			<div class="identity-group">
				<b-row class="identity-group" :class="{ 'form-group--error': $v.identityNumber.$error }">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="info-circle-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" placeholder="请输入证件号码" v-model.trim="$v.identityNumber.$model"/>
						<b-input-group-append>
							<b-dropdown :text="identityType" variant="success">
								<b-dropdown-item @click="changeIdentityType('身份证')">身份证</b-dropdown-item>
								<b-dropdown-item @click="changeIdentityType('军官证')">军官证</b-dropdown-item>
								<b-dropdown-item @click="changeIdentityType('护照')">护照</b-dropdown-item>
								<b-dropdown-item @click="changeIdentityType('回乡证')">港澳居民来往内地通行证</b-dropdown-item>
								<b-dropdown-item @click="changeIdentityType('台胞证')">台湾居民来往内地通行证</b-dropdown-item>
							</b-dropdown>
						</b-input-group-append>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.identityNumber.$error && !$v.identityNumber.required">必须输入证件号码</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.identityNumber.$error && !$v.identityNumber.verifyIdNumber">请输入正确的证件号码</b-col></b-row>
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
				<b-row class="city-group" :class="{'form-group--error': $v.city.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="geo-alt-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" placeholder="请输入所在城市名" v-model.trim="$v.city.$model"/>
						<b-input-group-append is-text>市</b-input-group-append>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.city.$error && !$v.city.required">必须输入城市名</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.city.$error && !$v.city.maxLength">城市名的长度请小于10个汉字</b-col></b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.city.$error && !$v.city.cityRule">请输入汉字</b-col></b-row>
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
						<b-button variant="success" type="submit" :disabled="registerStatus === 'PENDING'">
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
import {required, minLength, maxLength, sameAs} from 'vuelidate/lib/validators';
import {passwordRule, identityNumberRule, militaryIDRule, passportRule, HKMCIDRule, TWIDRule, phoneRule, cityRule} from "@/Validator";
import userService from "@/services/userService";

export default {
	name: 'Register',
	data() {
		return {
			registerStatus: null,
			passwordStatus: true,
			username: '',
			password: '',
			duplicatedPassword: '',
			lastname: '',
			firstname: '',
			identityNumber: '',
			identityType: '身份证',
			phoneNumber: '',
			city: '',
			description: '',
			easterEgg: ''
		};
	},
	validations: {
		// TODO: 防止SQL注入攻击
		username: {
			required,
			maxLength: maxLength(150)
		},
		password: {
			required,
			minLength: minLength(6),
			passwordRule
		},
		duplicatedPassword: {
			required,
			sameAsPassword: sameAs('password')
		},
		lastname: {
			required
		},
		firstname: {
			required
		},
		identityNumber: {
			required,
			//or: or(identityNumberRule, militaryIDRule, passportRule, HKMCIDRule, TWIDRule),
			verifyIdNumber: function (value) {
				//console.log(this.identityType)
				const idList = {
					'身份证': identityNumberRule,
					'军官证': militaryIDRule,
					'护照': passportRule,
					'回乡证': HKMCIDRule,
					'台胞证': TWIDRule
				}
				return idList[this.identityType] !== undefined && idList[this.identityType](value)
			}
		},
		phoneNumber: {
			required,
			phoneRule
		},
		city: {
			required,
			maxLength: maxLength(10),
			cityRule
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
				this.registerStatus = 'ERROR'
			} else {
				this.registerStatus = 'PENDING'
				userService.register({
					username: this.username,
					password: this.password,
					lastname: this.lastname,
					firstname: this.firstname,
					identity_number: this.identityNumber,
					identity_type: this.identityType,
					phone: this.phoneNumber,
					city: this.city,
					description: this.description
				})
				.then(userInfo => {
					localStorage.setItem('user', JSON.stringify(userInfo));
					this.$router.push('/explore');
				})
			    .catch(err => {
			    	if (err.response.data["username"]) {
			    		alert('用户名已被注册');
				    } else {
			    		alert('这是技术性调整 不要害怕');
				    }
			    	this.registerStatus = null;
			    })
			}
		},
		resetForm() {
			this.registerStatus = null;
			this.username = '';
			this.password = '';
			this.duplicatedPassword = '';
			this.lastname = '';
			this.firstname = '';
			this.identityNumber = '';
			this.identityType = '身份证';
			this.phoneNumber = '';
			this.city = '';
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
