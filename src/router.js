import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import App from "@/App";
import Checkin from "@/components/Checkin";
import Explore from "@/components/Explore";
import MyTask from "@/components/MyTask";
import MyRequest from "@/components/MyRequest";
import EditUser from "@/components/EditUser";
import Admin from "@/components/Admin";

let router = new Router({
    routes: [
        {
            path: '/checkin',
            name: 'checkin',
            component: Checkin
        },
        {
            path: '/explore',
            name: 'explore',
            component: Explore
        },
        {
            path: '/my-task',
            name: 'task',
            component: MyTask
        },
        {
            path: '/my-request',
            name: 'request',
            component: MyRequest
        },
        {
            path: '/edit-user-profile',
            name: 'edit',
            component: EditUser
        },
        {
            path: '/admin',
            name: 'admin',
            component: Admin
        },
        // 重定向
        {
            path: '/',
            redirect: '/checkin'
        }
    ]
});
router.beforeEach((to, from, next) => {
    let user = localStorage.getItem('user')

    if (to.name !== 'checkin' && !user) {
        next({ name: 'checkin'});
    }
    else if (to.name === 'checkin' && user) {
        next({ name: 'explore'});
    }
    else if (to.name === 'admin' && user && user.is_superuser) {
        next({ name: 'explore'});
    }
    else{
        next();
    }
})

export default router;
