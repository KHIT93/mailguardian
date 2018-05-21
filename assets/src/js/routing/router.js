import Vue from 'vue';
import VueRouter from 'vue-router';
import routes from './routes';
Vue.use(VueRouter);
const router = new VueRouter({
    routes
});
router.beforeEach(async (to, from, next) => {
    let result = {};
    window.axios.post('/api/current-user/').then(response => {
        result = response;
        if (to.matched.some(record => record.meta.requiresAuth)) {
            if (result.status == 403 && to.path != '/login') {
                next({
                    path: '/login'
                });
            }
            else {
                next();
            }
        }
        else if(to.matched.some(record => record.meta.requiresDomainAdmin)) {
            if (result.status == 403 && !result.data.user.is_domain_admin) {
                next(from);
            }
            else {
                next({ path: '/403', replace:false });
            }
        }
        else if(to.matched.some(record => record.meta.requiresAdmin)) {
            if (result.status == 403 && !result.data.user.is_staff) {
                next(from);
            }
            else {
                next({ path: '/403', replace:false });
            }
        }
        else {
            next();
        }
    }).catch(error => {
        if (error.response.status == 403 && to.path != '/login') {
            next({
                path: '/login'
            });
        }
        else {
            next();
        }
    })
    
});
export default router;