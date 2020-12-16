<template>
	<div class="admin-chart">
		<div class="filter">
			<b-row class="time-filter">
				<b-input-group size="sm">
					<b-input-group-prepend is-text>
						<b-icon icon="calendar2-week"></b-icon>
					</b-input-group-prepend>
					<b-datepicker v-model="startDate"></b-datepicker>
					<b-input-group-append is-text>
						<b-icon icon="calendar2-week-fill"></b-icon>
					</b-input-group-append>
					<b-datepicker v-model="endDate"></b-datepicker>
				</b-input-group>
			</b-row>
			<br/>
			<b-row class="city-filter">
				<b-input-group size="sm">
					<b-input-group-prepend is-text>
						<b-icon icon="geo-alt-fill"></b-icon>
					</b-input-group-prepend>
					<b-form-input v-model="cityFilter" type="search" placeholder="输入进行筛选条目"></b-form-input>
					<b-input-group-append is-text>市</b-input-group-append>
				</b-input-group>
			</b-row>
		</div>
		<highcharts :options="chartOptions"></highcharts>
	</div>
</template>

<script>
import { Chart } from "highcharts-vue";
import statService from "@/services/statService";

export default {
	name: "AdminChart",
	components: {highcharts: Chart},
	data() {
		return {
			startDate: null,
			endDate: null,
			cityFilter: null,
			chartOptions: {
				title: {text: null},
				series: [
					{
						name:"a",
						data:[1,2,3,4,3,2,1]
					},
					{
						name:"b",
						data:[6,5,1,2,3,4,5]
					}
				]
			},
			rawData: null
		}
	},
	beforeCreate() {
			statService.getStats().then(stats => {
				stats = []
				let middle = stats.reduce((m, curr) => {
					let curr_data = m[curr['task_type']] || []
					curr_data.push([curr['date'], curr['income']])
					m[curr['task_type']] = curr_data
					return m
				}, {})
				let result = []
				for (let k in Object.getOwnPropertyNames(middle)) {
					result.push({name: k, data: middle[k]})
				}
				this.rawData = result
			})
	}
}
</script>

<style scoped>

</style>
