<template>
	<div class="request-for-tasker">
		<b-container>
			<b-row class="filter">
				<b-col>
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
											<b-form-radio value="RequestDate">响应时间</b-form-radio>
											<b-form-radio value="RequesterName">响应用户昵称</b-form-radio>
											<b-form-radio value="RequestStatus">响应状态</b-form-radio>
										</b-form-radio-group>
									</b-col>
								</b-dropdown>
							</b-input-group-append>
						</b-input-group>
					</b-form-group>
				</b-col>
			</b-row>
			<b-row class="request-table">
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
								召集令进度:
								<br/>
								<div>
									<b-progress :max="row.item.RequiredPopulation" height="1.5rem">
										<b-progress-bar :value="row.item.RecruitedPopulation" :variant="renderColourByProgress(row.item)" striped animated>
											<span><strong>{{ row.item.RecruitedPopulation }}/{{ row.item.RequiredPopulation }}</strong></span>
										</b-progress-bar>
									</b-progress>
								</div>
							</b-popover>
						</template>
						
						<template #cell(RequestDate)="row">
							<div :id="'request-date-' + row.index">{{row.value}}</div>
							<b-popover :target="'request-date-' + row.index" triggers="hover" placement="bottom">
								响应描述：{{row.item.RequestDescription}}
							</b-popover>
						</template>
						
						<template #cell(RequesterName)="row">
							<div :id="'requester-name-' + row.index">{{row.value}}</div>
							<b-popover :target="'requester-name-' + row.index" triggers="hover" placement="bottom">
								响应用户实名：{{row.item.RequesterRealName}}
								<br/>
								响应用户等级：{{row.item.RequesterLevel}}
								<br/>
								响应用户城市：{{row.item.RequesterCity}}
								<br/>
								响应用户电话：{{row.item.RequesterPhone}}
								<br/>
								响应用户描述：{{row.item.RequesterDescription}}
							</b-popover>
						</template>
						
						<template #cell(RequestStatus)="row">
							<div :id="'request-status-' + row.index">{{row.value}}</div>
							<b-popover :target="'request-status-' + row.index" triggers="hover" placement="bottomleft" v-if="row.value === '待处理'">
								<b-button pill size='sm' variant="success" @click="onAgree(row.item)">同意</b-button>
								<b-button pill size="sm" variant="secondary" @click="onReject(row.item)">拒绝</b-button>
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
		</b-container>
	</div>
</template>

<script>
import taskService from "@/services/taskService";
import requestService from "@/services/requestService";

export default {
	name: "RequestForTasker",
	data() {
		return {
			fields: [
				{ key: 'Task', label: '召集令名称'},
				{ key: 'TaskType', label: '召集令类型', sortable: true},
				{ key: 'RequestDate', label: '响应时间', sortable: true, sortByFormatted: true,
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
				{ key: 'RequesterName', label: '响应用户昵称', sortable: true,
					sortByFormatted: (value, key, item) => {
						return item.RequesterLevel;
					}
				},
				{ key: 'RequestStatus', label: '响应状态', sortable: true, sortByFormatted: true, filterByFormatted: true,
					formatter: (value) => {
						if (value === 0) {
							return '待处理';
						} else if (value === 1) {
							return '已同意';
						} else if (value === 2) {
							return '已拒绝';
						} else if (value === 3) {
							return '已撤回';
						}
					}
				}
			],
			items: [],
			sortBy: 'RequestDate',
			sortDesc: true,
			filter: null,
			filterOn: ['RequesterName'],
			currentPage: 1,
			perPage: 5,
			pageOptions: [5, 10, 15, { value: 100, text: "全部显示" }],
		}
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
		getToBeDeal() {
			let toBeDealCounter = 0;
			this.items.forEach(currentRequest => {
				if (currentRequest.RequestStatus === 0)
					toBeDealCounter++;
			})
			return toBeDealCounter;
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
			if (key !== 'RequestDate') {
				return false;
			}
			const a = aRow[key];
			const b = bRow[key];
			return a < b ? -1 : a > b ? 1 : 0;
		},
		renderColourByStatus(item, type) {
			if (!item || type !== 'row') {
				return '';
			} else if (item.RequestStatus === 0) {
				return '';
			} else if (item.RequestStatus === 1) {
				return 'table-success';
			} else if (item.RequestStatus === 2) {
				return 'table-danger';
			} else if (item.RequestStatus === 3) {
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
		onAgree(item) {
			requestService.dealRequest(item.RequestID, "accept")
				.then(taskRequest => {
					alert("你问我资瓷不资瓷，我是资瓷滴！")
					item.RequestStatus = 1;
				})
				.catch(err => {
					console.log(err.response.data)
					alert('这是技术性调整 不要害怕');
				})
		},
		onReject(item) {
			requestService.dealRequest(item.RequestID, "reject")
				.then(taskRequest => {
					alert("你们啊 NAIVE！")
					item.RequestStatus = 2;
				})
				.catch(err => {
					//console.log(err.response.data)
					alert('这是技术性调整 不要害怕');
				})
		}
	},
	beforeCreate() {
		requestService.getRequests({creator: "task"}).then(result => {
			this.items = result.map(currentRequest => {
				return {
					Task: currentRequest.task.name,
					TaskID: currentRequest.task.id,
					TaskType: currentRequest.task.type,
					TaskDescription: currentRequest.task.description,
					RecruitedPopulation: currentRequest.task.recruited_population,
					RequiredPopulation: currentRequest.task.request_population,
					RequestID: currentRequest.id,
					RequestDate: currentRequest.edit_time,
					RequestStatus: currentRequest.status,
					RequestDescription: currentRequest.description,
					RequesterName: currentRequest.creator.username,
					RequesterRealName: currentRequest.creator.first_name + currentRequest.creator.last_name,
					RequesterLevel: currentRequest.creator.level,
					RequesterPhone: currentRequest.creator.phone,
					RequesterCity: currentRequest.creator.city,
					RequesterDescription: currentRequest.creator.description,
				}
			});
		})
	}
}

</script>

<style scoped>

</style>
