<template>
	<div class="admin-chart">
		<div class="filter">
			<b-row class="time-filter">
				<b-input-group size="sm">
					<b-input-group-prepend is-text>
						<b-icon icon="calendar2-week"></b-icon>
					</b-input-group-prepend>
					<b-datepicker v-model="startDate" placeholder="请选择起始日期"></b-datepicker>
          <b-input-group-append>
            <b-button size="sm" @click="startDate = null">
              <b-icon icon="trash"></b-icon>
            </b-button>
          </b-input-group-append>
					<b-input-group-prepend is-text>
						<b-icon icon="calendar2-week-fill"></b-icon>
					</b-input-group-prepend>
					<b-datepicker v-model="endDate" placeholder="请选择截止日期"></b-datepicker>
          <b-input-group-append>
            <b-button size="sm" @click="endDate = null">
              <b-icon icon="trash"></b-icon>
            </b-button>
          </b-input-group-append>
				</b-input-group>
			</b-row>
			<br/>
			<b-row class="city-filter">
				<b-input-group size="sm">
					<b-input-group-prepend is-text>
						<b-icon icon="geo-alt-fill"></b-icon>
					</b-input-group-prepend>
					<b-form-input v-model="cityFilter" type="search" placeholder="输入筛选城市"></b-form-input>
					<b-input-group-append is-text>市</b-input-group-append>
				</b-input-group>
			</b-row>
		</div>
		<highcharts :options="chartOptions"></highcharts>
	</div>
</template>

<script>
import {Chart} from "highcharts-vue";
import statService from "@/services/statService";

function filterData(data, filter) {
  let tempData = [];
  data.forEach(typeSummary => {
    let goodData = typeSummary.data.filter(filter);
    if (goodData.length > 0)
      tempData.push({name: typeSummary.name, data: goodData});
  })
  return tempData;
}

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
        yAxis: {title: {text: "收入"}},
        xAxis: {
				  type: "datetime",
          tickInterval: 24 * 3600 * 1000, // One day
          // dateTimeLabelFormats: {day: '%Y-%m-%d'}
        },
        tooltip: {
				  dateTimeLabelFormats: {day: '%Y-%m-%d'}
        },
				series: this.shownData
			},
			rawData: []
		}
	},
	beforeCreate() {
			statService.getStats().then(stats => {
        this.rawData = stats.map((curr) => {
          return {
            type: curr['task_type'],
            date: new Date(curr['date']).getTime(),
            raw_date: curr['date'],
            income: curr['income'],
            city: curr['city']
          }
        });
				this.$forceUpdate()
			})
	},
  computed: {
	  shownData() {
	    let tempData = this.rawData;
	    if (this.startDate) {
	      const startDate = new Date(this.startDate).getTime();
        tempData = filterData(tempData, d => d.date >= startDate);
      }
      if (this.endDate) {
        const endDate = new Date(this.endDate).getTime();
	      tempData = filterData(tempData, d => d.date <= endDate);
      }
      if (this.cityFilter) {
        tempData = filterData(tempData, d => d.city === this.cityFilter)
      }
      // Finalize
      let summary = {}
      tempData.forEach(d => {
        let typeSummary = summary[d.type] || {};
        let dateSummary = typeSummary[d.date] || 0;
        dateSummary += d.income;
        typeSummary[d.date] = dateSummary;
        summary[d.type] = typeSummary;
      })
      let result = [];
      Object.getOwnPropertyNames(summary).forEach(type => {
          let data = Object.entries(summary[type]);
          data = data.map(v => {
            console.log(v[0])
            v[0] = Number(v[0])
            return v;
          })
          result.push({name: type, data: data});
      });
	    return result;

    }
  },
  beforeUpdate() {
	  this.chartOptions.series = this.shownData
  }
}
</script>

<style scoped>

</style>
