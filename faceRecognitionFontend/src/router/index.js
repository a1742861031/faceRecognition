import Vue from 'vue'
import Router from 'vue-router'
import Authentication from '../components/Authentication.vue'
import  AddUser from'../components/AddUser.vue'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path:'/',
      redirect:'/Auth',
      name:'ึ๗าณ'
    },
    {
      
      path: '/Auth',
      name: 'Authentication',
      component: Authentication
    },
    {
      
      path: '/adduser',
      name: 'AddUser',
      component: AddUser
    },
  ]
})
