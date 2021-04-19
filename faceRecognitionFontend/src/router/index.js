import Vue from 'vue'
import Router from 'vue-router'
import Authentication from '../components/Authentication.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path:'/',
      redirect:'/Auth',
      name:'��ҳ'
    },
    {
      
      path: '/Auth',
      name: 'Authentication',
      component: Authentication
    },
  ]
})
