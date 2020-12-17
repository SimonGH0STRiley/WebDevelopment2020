<template>
	<div class="new-task">
		<b-form @submit.prevent="submitForm">
			<div class="task-name-group">
				<b-row class="task-name-group" :class="{'form-group--error': $v.taskName.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="kanban-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-input class="form-input" placeholder="请输入召集令名称" v-model.trim="$v.taskName.$model"/>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.taskName.$error && !$v.taskName.required">必须输入召集令名称</b-col></b-row>
				<br/>
			</div>
			<div class="task-type-group">
				<b-row class="task-name-group" :class="{'form-group--error': $v.taskType.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="filter-circle-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-select class="form-input" v-model.trim="$v.taskType.$model">
							<template #first><b-form-select-option :value="''" disabled>请选择召集令类型</b-form-select-option></template>
							<b-form-select-option value="技术交流">技术交流</b-form-select-option>
							<b-form-select-option value="学业探讨">学业探讨</b-form-select-option>
							<b-form-select-option value="社会实践">社会实践</b-form-select-option>
							<b-form-select-option value="公益志愿">公益志愿</b-form-select-option>
							<b-form-select-option value="实习工作">实习工作</b-form-select-option>
							<b-form-select-option value="外出游玩">外出游玩</b-form-select-option>
							<b-form-select-option value="其他类型">其他类型</b-form-select-option>
						</b-form-select>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.taskName.$error && !$v.taskName.required">必须选择召集令类型</b-col></b-row>
				<br/>
			</div>
			<div class="required-population-group">
				<b-row class="required-population-group" :class="{'form-group--error': $v.requiredPopulation.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="person-lines-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-spinbutton class="form-input" placeholder="请选择召集人数" warp v-model.trim="$v.requiredPopulation.$model" min="1" max="100"></b-form-spinbutton>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.requiredPopulation.$error && !$v.requiredPopulation.required">必须选择召集人数</b-col></b-row>
				<br/>
			</div>
			<div class="deadline-group">
				<b-row class="deadline-group" :class="{'form-group--error': $v.deadline.endDate.$error}">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="alarm-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-datepicker placeholder="请选择截止日期" :state="!$v.deadline.endDate.$error ? null : false"
						                   :min="today" :start-weekday="1"
						                   today-button reset-button close-button
						                   v-bind="labels['zh_Date']" v-model.trim="$v.deadline.endDate.$model"></b-form-datepicker>
						<b-form-timepicker placeholder="请选择截止时间"
						                   show-seconds :hour12="false" now-button reset-button :locale="'de'"
						                   v-bind="labels['zh_Time']" v-model.trim="deadline.endTime"></b-form-timepicker>
					</b-input-group>
				</b-row>
				<b-row><b-col offset="1" class="error" v-if="$v.deadline.endDate.$error && !$v.deadline.endDate.required">必须选择召集令截止日期</b-col></b-row>
				<br/>
			</div>
			<div class="photo-group">
				<b-row class="photo-group">
					<b-input-group>
						<b-input-group-prepend is-text>
							<b-icon class="form-label" icon="image-fill"></b-icon>
						</b-input-group-prepend>
						<b-form-file placeholder="上传召集令描述图片（可选）" drop-placeholder="拖拽图片到这里" browse-text="浏览本地图片"
						             accept="image/*" v-model="photo">
							<template slot="file-name" slot-scope="{ names }">
								<b-badge pill variant="info">{{ names[0] }}</b-badge>
							</template>
						</b-form-file>
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
			<div class="new-task-button">
				<b-row>
					<b-col offset="3" cols="2">
						<b-button variant="success" type="submit" :disabled="newTaskStatus === 'PENDING'">
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
import { maxLength, required, numeric } from "vuelidate/lib/validators";
import taskService from "@/services/taskService";

export default {
	name: "NewTask",
	data() {
		const now = new Date();
		const today = now.getFullYear()  + '-' + (now.getMonth() + 1) + '-' + now.getDate();
		const present = now.toTimeString().slice(0,8);
		return {
			newTaskStatus: null,
			taskName: '',
			taskType: '',
			requiredPopulation: null,
			deadline: {
				endDate: today,
				endTime: present,
			},
			photo: null,
			description: '',
			today: today,
			present: present,
			labels: {
				zh_Date: {
					weekdayHeaderFormat: 'narrow',
					labelPrevDecade: '过去十年',
					labelPrevYear: '上一年',
					labelPrevMonth: '上个月',
					labelCurrentMonth: '当前月份',
					labelNextMonth: '下个月',
					labelNextYear: '明年',
					labelNextDecade: '未来十年',
					labelToday: '今天',
					labelSelected: '选定日期',
					labelNoDateSelected: '未选择日期',
					labelCalendar: '日历',
					labelNav: '日历导航',
					labelHelp: '使用光标键浏览日期',
					labelTodayButton: '选择今天',
					labelResetButton: '重置',
					labelCloseButton: '关闭'
				},
				zh_Time: {
					labelHours: '小时',
					labelMinutes: '分钟',
					labelSeconds: '秒',
					labelAmpm: '上午下午',
					labelAm: '上午',
					labelPm: '下午',
					labelIncrement: '增加',
					labelDecrement: '减少',
					labelSelected: '选定时间',
					labelNoTimeSelected: '没有选择时间',
					labelNowButton: '现在时间',
					labelResetButton: '重置',
					labelCloseButton: '关闭'
				}
			}
		};
	},
	
	validations: {
		// TODO: 防止SQL注入攻击
		taskName: {
			required,
			maxLength: maxLength(20),
		},
		taskType: {
			required,
		},
		requiredPopulation: {
			required,
			numeric,
		},
		deadline: {
			endDate: {
				required
			},
		},
		endTime: {
		},
		description: {
			maxLength: maxLength(500),
		}
	},
	
	methods: {
		submitForm() {
			console.log('submit!')
			this.$v.$touch()
			if (this.$v.$invalid) {
				this.newTaskStatus = 'ERROR'
			} else {
				this.newTaskStatus = 'PENDING'
				let form = new FormData()
				form.append('name', this.taskName);
				form.append('type', this.taskType);
				form.append('request_population', this.requiredPopulation);
				form.append('end_time', this.deadline.endDate + 'T' + this.deadline.endTime);
				if (this.photo) {
					form.append('photo', this.photo);
				}
				form.append('description', this.description);
				taskService.createTask(form)
				.then(task => {
					alert('啪的一下 很快嗷！');
					this.$emit('NewedTask', task);
				})
				.catch(err => {
					alert('这是技术性调整 不要害怕');
					this.newTaskStatus = null;
				})
			}
		},
		resetForm() {
			this.newTaskStatus = null;
			this.taskName = '';
			this.taskType = '';
			this.requiredPopulation = null;
			this.deadline.endDate = this.today;
			this.deadline.endTime = this.present;
			this.photo = null;
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
