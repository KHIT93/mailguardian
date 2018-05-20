import Vue from 'vue';
import VueRouter from 'vue-router';
import routes from './routes';
Vue.use(VueRouter);
// let getters = mapGetters(['user']);
// let actions = mapActions(['checkSession']);
// let mutations = mapMutations(['notify']);
const router = new VueRouter({
    routes
});
router.beforeEach(async (to, from, next) => {
    let result = {};
    window.axios.post('/api/current-user/').then(response => {
        console.log()
        result = response;
        if (to.matched.some(record => record.meta.requiresAuth)) {
            if (result.status == 403 && to.path != '/login') {
                next({
                    path: '/login'
                });
            }
            else if(to.matched.some(record => record.meta.requiresDomainAdmin)) {
                if (result.status == 403 && !result.data.user.is_domain_admin) {
                    next(from);
                }
            }
            else if(to.matched.some(record => record.meta.requiresAdmin)) {
                if (result.status == 403 && !result.data.user.is_staff) {
                    next(from);
                }
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
    
});
export default router;