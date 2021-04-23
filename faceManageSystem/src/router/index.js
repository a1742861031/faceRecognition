import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import AdminProfile from '../components/function/AdminProfile.vue'
import ManageFace from '../components/function/ManageFace.vue'
Vue.use(Router)
//挂载路由导航守卫
 
// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = Router.prototype.push
 
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}



const router = new Router({
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/home', component: Home, redirect: '/profile', children: [
        { path: '/profile', component: AdminProfile },
        { path: '/allface', component: ManageFace },
      ]
    }
  ]
});


// // 导航守卫
// // 使用 router.beforeEach 注册一个全局前置守卫，判断用户是否登陆
// router.beforeEach(async (to, from, next) => {
//   const res = await Vue.prototype.$http.get('sessions');
//   console.log(res);
//   if (to.path === '/login') {
//     next();
//   } else {
//     if (res.data.code != 200) {
//       next('/login');
//     } else {
//       next();
//     }
//   }
// });


export default router;