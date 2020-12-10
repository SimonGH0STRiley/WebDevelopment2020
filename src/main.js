import Vue from 'vue';
import App from '@/App.vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import store from '@/store';
import router from '@/router';
import VueRouter from "vue-router";
import VueResource from 'vue-resource'
import Vuelidate from "vuelidate/src";
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
// Install VueRouter
Vue.use(VueRouter)
// Install VueResource
Vue.use(VueResource)
// Install Vuelidate
Vue.use(Vuelidate)


const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
