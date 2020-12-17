<template>
	<div class="task-for-tasker">
		<b-container>
			<b-row class="filter&new">
				<b-col cols="10" class="filter">
					<b-form-group>
						<b-input-group size="sm">
							<b-input-group-prepend is-text>
								<b-icon icon="search"></b-icon>
							</b-input-group-prepend>
							<b-form-input v-model="filter" type="search" placeholder="输入进行筛选条目"></b-form-input>
							<b-input-group-append>
								<b-dropdown size="sm" no-caret>
									<template #button-content>
										<b-icon icon="filter-circle"></b-icon>
									</template>
									<b-col>
										<b-form-radio-group v-model="filterOn[0]">
											<b-form-radio value="Task">召集令名称</b-form-radio>
											<b-form-radio value="TaskType">召集令类型</b-form-radio>
											<b-form-radio value="EndDate">结束时间</b-form-radio>
											<b-form-radio value="RecruitProgress">招募进度</b-form-radio>
											<b-form-radio value="TaskStatus">召集令状态</b-form-radio>
										</b-form-radio-group>
									</b-col>
								</b-dropdown>
							</b-input-group-append>
						</b-input-group>
					</b-form-group>
				</b-col>
				<b-col cols="2" class="new-task">
					<b-button size='sm' variant="outline-primary" @click="onNewTask($event.target)">
						<b-icon icon="clipboard-plus"></b-icon>新建召集令
					</b-button>
				</b-col>
			</b-row>
			<b-row class="task-table">
				<b-col>
					<b-table
						:fields="fields" :items="items"
						:current-page="currentPage" :per-page="perPage"
						:filter="filter" :filter-included-fields="filterOn"
						:sort-compare="sortCompare" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc"
						@filtered="onFiltered"
						:tbody-tr-class="renderColourByStatus"
						show-empty small stacked="md" sticky-header="" head-variant="light" label bordered outlined hover>
						
						<template #cell(Task)="row">
							<div :id="'task-' + row.index">{{row.value}}</div>
							<b-popover :target="'task-' + row.index" triggers="hover" placement="bottomright">
								召集令类型：{{row.item.TaskType}}
								<br/>
								召集令描述：{{row.item.TaskDescription}}
								<br/>
								<div v-if="row.item.TaskPhotoUrl">
									召集令图片：<br/>
									<b-img :src="row.item.TaskPhotoUrl" style="max-width: 200px"></b-img>
								</div>
							</b-popover>
						</template>
						
						<template #cell(TaskerName)="row">
							<div :id="'tasker-name-' + row.index">{{row.value}}</div>
							<b-popover :target="'tasker-name-' + row.index" triggers="hover" placement="bottom">
								发令用户实名：{{row.item.TaskerRealName}}
								<br/>
								发令用户等级：{{row.item.TaskerLevel}}
								<br/>
								发令用户城市：{{row.item.TaskerCity}}
								<br/>
								发令用户电话：{{row.item.TaskerPhone}}
								<br/>
								发令用户描述：{{row.item.TaskerDescription}}
							</b-popover>
						</template>
						
						<template #cell(RecruitProgress)="row">
							<b-progress :max="row.item.RequiredPopulation" height="1.5rem">
								<b-progress-bar :value="row.item.RecruitedPopulation" :variant="renderColourByProgress(row.item)" striped animated>
									<span><strong>{{ row.item.RecruitedPopulation }}/{{ row.item.RequiredPopulation }}</strong></span>
								</b-progress-bar>
							</b-progress>
						</template>
						
						<template #cell(TaskStatus)="row">
							<div :id="'task-status-' + row.index">{{row.value}}</div>
							<b-popover :target="'task-status-' + row.index" triggers="hover" placement="bottomleft" v-if="row.value === '待响应' && row.item.TaskerName !== currentUsername">
								<b-button pill size='sm' variant="success" @click="onNewRequest(row.item, $event.target)">申请</b-button>
							</b-popover>
						</template>
					</b-table>
				</b-col>
			</b-row>
			<b-row class="page-nav">
				<b-col cols="6">
					<b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage" align="fill" size="sm" class="my-0"></b-pagination>
				</b-col>
				<b-col cols="6">
					<b-form-group label="每页显示条目数" label-size="sm" label-cols-sm="8" label-for="perPageSelect" label-align="right">
						<b-form-select v-model="perPage" id="perPageSelect" size="sm" :options="pageOptions"></b-form-select>
					</b-form-group>
				</b-col>
			</b-row>
			<b-modal :id="newTaskModal.id" :title="'新建召集令'" @hide="resetNewTaskModal"
			         size="lg" centered
			         header-bg-variant="dark" header-text-variant="light"
			         body-bg-variant="light" body-text-variant="dark"
			         footer-bg-variant="warning" footer-text-variant="dark"
			         ok-only ok-title="关闭" ok-variant="secondary">
				<b-container >
					<new-task v-model="newTaskModal.content" v-bind="$attrs" v-on="$listeners" @NewedTask="onNewedTask"/>
				</b-container>
			</b-modal>
			<b-modal :id="newRequestModal.id" :title="'响应召集令' + newRequestModal.title" @hide="resetNewRequestModal"
			         size="lg" centered
			         header-bg-variant="dark" header-text-variant="light"
			         body-bg-variant="light" body-text-variant="dark"
			         footer-bg-variant="warning" footer-text-variant="dark"
					 ok-only ok-title="关闭" ok-variant="secondary">
				<b-container>
					<new-request :content="newRequestModal.content" v-bind="$attrs" v-on="$listeners" @NewedRequest="onNewedRequest"/>
				</b-container>
			</b-modal>
		</b-container>
	</div>
</template>

<script>
import NewTask from "@/components/Explore/NewTask";
import NewRequest from "@/components/Explore/NewRequest";
import taskService from "@/services/taskService";

function formatTask(currentTask) {
  return {
    Task: currentTask.name,
    TaskID: currentTask.id,
    TaskType: currentTask.type,
    StartDate: currentTask.edit_time,
    EndDate: currentTask.end_time,
    TaskStatus: currentTask.status,
    TaskPhotoUrl: currentTask.photo,
    TaskDescription: currentTask.description,
    RequiredPopulation: currentTask.request_population,
    RecruitedPopulation: currentTask.recruited_population,
    TaskerName: currentTask.creator.username,
    TaskerRealName: currentTask.creator.first_name + currentTask.creator.last_name,
    TaskerLevel: currentTask.creator.level,
    TaskerPhone: currentTask.creator.phone,
    TaskerCity: currentTask.creator.city,
    TaskerDescription: currentTask.creator.description,
  };
}

export default {
	name: "TaskForTasker",
	data() {
		const now = new Date();
		return {
			fields: [
				{ key: 'Task', label: '召集令名称'},
				{ key: 'TaskType', label: '召集令类型', sortable: true},
				{ key: 'EndDate', label: '结束时间', sortable: true, sortByFormatted: true,
					formatter: (value) => {
						let date = new Date;
						let timeStamp = Date.parse(value);
						date.setTime(timeStamp);
						return date.toLocaleDateString('zh-CN', {
							year: 'numeric',
							month: 'long',
							day: 'numeric'
						}) + date.toLocaleTimeString('zh-CN');
					}
				},
				{ key: 'TaskerName', label: '发令用户昵称', sortable: true,
					sortByFormatted: (value, key, item) => {
						return item.TaskerLevel;
					}
				},
				{ key: 'RecruitProgress', label: '招募进度', sortable: true,
					sortByFormatted: (value, key, item) => {
						return item.RecruitedPopulation / item.RequiredPopulation;
					}
				},
				{ key: 'TaskStatus', label: '召集令状态', sortable: true, sortByFormatted: true, filterByFormatted: true,
					formatter: (value, key, item) => {
						let EndTime = new Date(item.EndDate);
						if (value === 0 && EndTime > now) {
							return '待响应';
						} else if (value === 0 && EndTime <= now) {
							return '未达成';
						} else if (value === 1) {
							return '已完成';
						} else if (value === 2) {
							return '已取消';
						}
					}
				}
			],
			items: [],
			sortBy: 'EndDate',
			sortDesc: true,
			filter: null,
			filterOn: ['Task'],
			currentPage: 1,
			perPage: 5,
			pageOptions: [5, 10, 15, { value: 100, text: "全部显示" }],
			now: now,
			currentUsername: 'GHOST',
			newTaskModal: {
				id: 'new-task-modal',
				content: {}
			},
			newRequestModal: {
				id: 'new-request-modal',
				title: '',
				content: {}
			}
		}
	},
	components: {
		NewTask,
		NewRequest
	},
	computed: {
		sortOptions() {
			// Create an options list from our fields
			return this.fields
				.filter(f => f.sortable)
				.map(f => {
					return { text: f.label, value: f.key }
				})
		},
    totalRows() {
		  return this.items.length;
    }
	},
	methods: {
		onFiltered(filteredItems) {
			// Trigger pagination to update the number of buttons/pages due to filtering
			this.totalRows = filteredItems.length
			this.currentPage = 1
		},
		sortCompare(aRow, bRow, key) {
			if (key !== 'EndDate') {
				return false;
			}
			const a = aRow[key];
			const b = bRow[key];
			return a < b ? -1 : a > b ? 1 : 0;
		},
		renderColourByStatus(item, type) {
			if (!item || type !== 'row') {
				return '';
			}
			let EndTime = new Date(item.EndDate);
			if (item.TaskStatus === 0 && EndTime > this.now) {
				return '';
			} else if (item.TaskStatus === 0 && EndTime <= this.now) {
				return 'table-danger';
			} else if (item.TaskStatus === 1) {
				return 'table-success';
			} else if (item.TaskStatus === 2) {
				return 'table-secondary';
			}
		},
		renderColourByProgress(item) {
			let ratio = item.RecruitedPopulation / item.RequiredPopulation;
			if (!item) {
				return '';
			} else if (ratio <= 0.25) {
				return 'danger';
			} else if (ratio > 0.25 && ratio <= 0.5) {
				return 'warning';
			} else if (ratio > 0.5 && ratio <= 1) {
				return 'primary';
			} else if (ratio === 1) {
				return 'success';
			}
		},
		onNewTask(button) {
			this.$root.$emit('bv::show::modal', this.newTaskModal.id, button);
		},
		onNewedTask(newTask) {
			this.$root.$emit('bv::hide::modal', this.newTaskModal.id);
			this.items.push(formatTask(newTask));
			// this.$forceUpdate();
		},
		onNewRequest(item, button) {
			this.newRequestModal.title = item.Task;
			this.newRequestModal.content.name = item.Task;
			this.newRequestModal.content.id = item.TaskID
			this.$root.$emit('bv::show::modal', this.newRequestModal.id, button);
		},
		onNewedRequest() {
			this.$root.$emit('bv::hide::modal', this.newRequestModal.id);
			this.$forceUpdate();
		},
		resetNewTaskModal() {
			this.newTaskModal.title = '';
			this.newTaskModal.content = {};
		},
		resetNewRequestModal() {
			this.newRequestModal.title = '';
			this.newRequestModal.content = {};
		}
	},
	beforeCreate() {
		taskService.getTasks().then(result => {
			this.items = result.map(formatTask);
		})
	}
}

</script>

<style scoped>

</style>
