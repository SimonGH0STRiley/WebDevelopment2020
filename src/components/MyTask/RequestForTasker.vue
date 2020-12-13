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
								{{JSON.stringify(row.item, null, 2)}}
							</b-popover>
						</template>
						
						<template #cell(RequestDate)="row">
							<div :id="'request-date-' + row.index">{{row.value}}</div>
							<b-popover :target="'request-date-' + row.index" triggers="hover" placement="bottom">
								{{JSON.stringify(row.item, null, 2)}}
							</b-popover>
						</template>
						
						<template #cell(RequesterName)="row">
							<div :id="'requester-name-' + row.index">{{row.value}}</div>
							<b-popover :target="'requester-name-' + row.index" triggers="hover" placement="bottom">
								{{JSON.stringify(row.item, null, 2)}}
							</b-popover>
						</template>
						
						<template #cell(RequestStatus)="row">
							<div :id="'request-status-' + row.index">{{row.value}}</div>
							<b-popover :target="'request-status-' + row.index" triggers="hover" placement="bottomleft" v-if="row.value === '待处理'">
								<b-button pill size='sm' variant="success" @click="onAgree(row.item)">同意</b-button>
								<b-button pill size="sm" variant="danger" @click="onReject(row.item)">拒绝</b-button>
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
			items: [
				{ Task: 'Mission 100', TaskType: '其他类型', RequestDate: '2020-01-01', RequesterName: 'GHOST', RequesterLevel: 6, RequestStatus: 0},
				{ Task: 'Mission 101', TaskType: '其他类型', RequestDate: '2020-01-02', RequesterName: 'GHOST', RequesterLevel: 6, RequestStatus: 1},
				{ Task: 'Mission 200', TaskType: '其他类型', RequestDate: '2020-01-03', RequesterName: 'GHOST', RequesterLevel: 6, RequestStatus: 2},
				{ Task: 'Mission 201', TaskType: '其他类型', RequestDate: '2020-01-04', RequesterName: 'John Price', RequesterLevel: 1, RequestStatus: 3},
				{ Task: 'Mission 202', TaskType: '其他类型', RequestDate: '2020-01-05', RequesterName: 'John Price', RequesterLevel: 1, RequestStatus: 0},
				{ Task: 'Mission 203', TaskType: '其他类型', RequestDate: '2020-01-06', RequesterName: 'John Price', RequesterLevel: 1, RequestStatus: 1},
				{ Task: 'Mission 300', TaskType: '其他类型', RequestDate: '2020-01-07', RequesterName: 'Roach', RequesterLevel: 6, RequestStatus: 2},
				{ Task: 'Mission 301', TaskType: '其他类型', RequestDate: '2020-01-08', RequesterName: 'Roach', RequesterLevel: 6, RequestStatus: 3},
				{ Task: 'Mission 400', TaskType: '其他类型', RequestDate: '2020-01-09', RequesterName: 'Gaz', RequesterLevel: 4, RequestStatus: 0},
				{ Task: 'Mission 401', TaskType: '其他类型', RequestDate: '2020-01-10', RequesterName: 'Gaz', RequesterLevel: 4, RequestStatus: 1},
				{ Task: 'Mission 402', TaskType: '其他类型', RequestDate: '2020-01-11', RequesterName: 'Gaz', RequesterLevel: 4, RequestStatus: 2},
				{ Task: 'Mission 403', TaskType: '其他类型', RequestDate: '2020-01-12', RequesterName: 'Yuri', RequesterLevel: 8, RequestStatus: 3},
				{ Task: 'Mission 404', TaskType: '其他类型', RequestDate: '2020-01-13', RequesterName: 'Yuri', RequesterLevel: 8, RequestStatus: 0},
			],
			sortBy: 'RequestDate',
			sortDesc: true,
			filter: null,
			filterOn: ['RequesterName'],
			totalRows: 1,
			currentPage: 1,
			perPage: 5,
			pageOptions: [5, 10, 15, { value: 100, text: "全部显示" }],
		}
	},
	mounted() {
		// Set the initial number of items
		this.totalRows = this.items.length
	},
	computed: {
		sortOptions() {
			// Create an options list from our fields
			return this.fields
				.filter(f => f.sortable)
				.map(f => {
					return { text: f.label, value: f.key }
				})
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
		onAgree(item) {
			item.RequestStatus = 1;
			// TODO: Do agree
		},
		onReject(item) {
			item.RequestStatus = 2;
			// TODO: Do reject
		}
	}
}

</script>

<style scoped>

</style>
