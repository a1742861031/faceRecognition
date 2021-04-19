// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import App from './App'
import axios from 'axios'
import router from './router'
import { Button,NavBar,Popup } from "vant";
import '../static/global.css'

axios.defaults.baseURL = "http://127.0.0.1:5000" // 添加baseUrl
Vue.config.productionTip = false
Vue.prototype.$http = axios
/* eslint-disable no-new */
Vue.use(NavBar)
Vue.use(Button)
Vue.use(Popup)
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
