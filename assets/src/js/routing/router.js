import Vue from 'vue';
import VueRouter from 'vue-router';
import routes from './routes';
Vue.use(VueRouter);
const router = new VueRouter({
    routes
});
router.beforeEach(async (to, from, next) => {
    let result = {};
    let whitelisted = [
        '/password-reset',
        '/setup'
    ];
    if (!whitelisted.some(w => to.path.startsWith(w))) {
        window.axios.post('/api/current-user/').then(response => {
            if (to.matched.some(record => record.meta.requiresAuth)) {
                if (response.status == 403 && to.path != '/login') {
                    next({
                        path: '/login'
                    });
                }
                else {
                    next();
                }
            }
            else if(to.matched.some(record => record.meta.requiresDomainAdmin)) {
                if (response.status == 403 && !response.data.user.is_domain_admin) {
                    next({ path: '/403', replace:false });
                }
                else {
                    next();
                }
            }
            else if(to.matched.some(record => record.meta.requiresAdmin)) {
                if (response.status == 403 && !response.data.user.is_staff) {
                    next({ path: '/403', replace:false });
                }
                else {
                    next();
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
    }
    else {
        next();
    }
    
});
export default router;