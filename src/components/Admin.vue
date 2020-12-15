<template>
  <div>
    <b-form-group>
      <b-row>
      <b-col cols="4">
        <b-input-group size="sm">
          <b-input-group-prepend is-text>Start</b-input-group-prepend>
          <b-datepicker v-model="startDate"></b-datepicker>
        </b-input-group>
      </b-col>
      <b-col cols="4">
        <b-input-group size="sm">
          <b-input-group-prepend is-text>End</b-input-group-prepend>
          <b-datepicker v-model="endDate"></b-datepicker>
        </b-input-group>
      </b-col>
        </b-row>
      <b-input-group size="sm">
                <b-input-group-prepend is-text>
                  <b-icon icon="search"></b-icon>
                </b-input-group-prepend>
                <b-form-input v-model="cityFilter" type="search" placeholder="输入进行筛选条目"></b-form-input>
      </b-input-group>
    </b-form-group>
    <b-table></b-table>
    <highcharts :options="chartOptions"></highcharts>
  </div>
</template>

<script>
import { Chart } from "highcharts-vue";
export default {
  name: "Admin",
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
      }
    }
  }
}
</script>

<style scoped>

</style>