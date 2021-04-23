import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import AdminProfile from '../components/function/AdminProfile.vue'
import ManageFace from '../components/function/ManageFace.vue'
Vue.use(Router)
//����·�ɵ�������
 
// ���ElementUI�������е�vue-router��3.0�汾�����ظ���˵���������

// ���ElementUI�������е�vue-router��3.0�汾�����ظ���˵���������
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


// // ��������
// // ʹ�� router.beforeEach ע��һ��ȫ��ǰ���������ж��û��Ƿ��½
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