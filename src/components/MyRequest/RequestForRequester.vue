<template>
	<div class="request-for-requester">
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
											<b-form-radio value="TaskerName">发令用户昵称</b-form-radio>
											<b-form-radio value="RequestDate">接令时间</b-form-radio>
											<b-form-radio value="RequestStatus">当前状态</b-form-radio>
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
						
						<template #cell(RequestStatus)="row">
							<div :id="'request-status-' + row.index">{{row.value}}</div>
							<b-popover :target="'request-status-' + row.index" triggers="hover" placement="bottomleft" v-if="row.value === '待处理'">
								<b-button pill size='sm' variant="success" @click="onEdit(row.item, $event.target)">修改</b-button>
								<b-button pill size="sm" variant="secondary" @click="onCancel(row.item)">取消</b-button>
							</b-popover>
							<b-popover :target="'request-status-' + row.index" triggers="hover" placement="bottomleft" v-if="row.value === '已撤回' || row.value === '已拒绝'">
								<b-button pill size='sm' variant="danger" @click="onDelete(row.item)">删除</b-button>
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
			<b-modal :id="editRequestModal.id" :title="editRequestModal.title" @hide="resetEditRequestModal"
			         size="lg" centered
			         header-bg-variant="dark" header-text-variant="light"
			         body-bg-variant="light" body-text-variant="dark"
			         footer-bg-variant="warning" footer-text-variant="dark"
			         ok-only ok-title="取消" ok-variant="secondary">
				<b-container>
					<edit-request :content="editRequestModal.content" v-bind="$attrs" v-on="$listeners" @EditedRequest="onEdited"/>
				</b-container>
			</b-modal>
		</b-container>
	</div>
</template>

<script>
import EditRequest from "@/components/MyRequest/EditRequest";
import requestService from "@/services/requestService";

export default {
	name: "RequesterForRequester",
	data() {
		return {
			fields: [
				{ key: 'Task', label: '召集令名称'},
				{ key: 'TaskType', label: '召集令类型', sortable: true},
				{ key: 'TaskerName', label: '发令用户昵称', sortable: true,
					sortByFormatted: (value, key, item) => {
						return item.TaskerLevel;
					}
				},
				{ key: 'RequestDate', label: '接令时间', sortable: true, sortByFormatted: true,
					formatter: (value) => {
						console.log(value)
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
				{ key: 'RequestStatus', label: '召集令状态', sortable: true, sortByFormatted: true, filterByFormatted: true,
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
			filterOn: ['TaskerName'],
			currentPage: 1,
			perPage: 5,
			pageOptions: [5, 10, 15, { value: 100, text: "全部显示" }],
			editRequestModal: {
				id: 'edit-request-modal',
				title: '',
				content: {}
			}
		}
	},
	components: {
		EditRequest
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
			if (key !== 'TaskDate') {
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
		onEdit(item, button) {
			this.editRequestModal.title = item.Task;
			this.editRequestModal.content.name = item.Task;
			this.editRequestModal.content.id = item.RequestID;
			this.editRequestModal.content.description = item.RequestDescription;
			this.$root.$emit('bv::show::modal', this.editRequestModal.id, button);
		},
		onEdited() {
			this.$root.$emit('bv::hide::modal', this.editRequestModal.id);
			this.$forceUpdate();
		},
		onCancel(item) {
			requestService.cancelRequest(item.RequestID)
				.then(taskRequest => {
					alert('取消了!');
					item.RequestStatus = 3;
				})
				.catch((err => {
					console.log(err.response.data)
					alert('这是技术性调整 不要害怕');
				}))
		},
		onDelete(item) {
			requestService.deleteRequest(item.RequestID)
				.then(taskRequest => {
					alert('删除了!');
					this.items.splice(this.items.indexOf(item), 1);
				})
				.catch((err => {
					
					alert('这是技术性调整 不要害怕');
				}))
		},
		resetEditRequestModal() {
			this.editRequestModal.title = '';
			this.editRequestModal.content = {};
		}
	},
	beforeCreate() {
		requestService.getRequests({creator: "request"}).then(result => {
			this.items = result.map(currentRequest => {
				return {
					Task: currentRequest.task.name,
					TaskType: currentRequest.task.type,
					TaskPhotoUrl: currentRequest.task.photo,
					TaskDescription: currentRequest.task.description,
					RecruitedPopulation: currentRequest.task.recruited_population,
					RequiredPopulation: currentRequest.task.request_population,
					TaskerName: currentRequest.task.creator.username,
					TaskerRealName: currentRequest.task.creator.first_name + currentRequest.creator.last_name,
					TaskerLevel: currentRequest.task.creator.level,
					TaskerPhone: currentRequest.task.creator.phone,
					TaskerCity: currentRequest.task.creator.city,
					TaskerDescription: currentRequest.task.creator.description,
					RequestID: currentRequest.id,
					RequestDate: currentRequest.edit_time,
					RequestStatus: currentRequest.status,
					RequestDescription: currentRequest.info,
				}
			});
		})
	}
}

</script>

<style scoped>

</style>
