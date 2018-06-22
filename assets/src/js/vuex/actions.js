import router from '../routing/router';
export default {
    async login({commit, state}) {
        commit('toggleLoading');
        //AJAX call for logging in
        commit('toggleLoading');
    },
    async logout({commit, state}) {
        commit('toggleLoading');
        //AJAX call for logging out
        commit('toggleLoading');
    },
    async getCurrentUser({commit, state}) {
        commit('toggleLoading');
        //AJAX call to fetch the current user
        if(state.isLoggedIn) {
            axios.post('/api/current-user/').then(response => {
                commit('setCurrentUser',response.data);
                commit('toggleLoading');
            }).catch(error => {
                console.log(error);
                commit('toggleLoading');
            })
        }
    },
    checkSession({commit, state}) {
        return new Promise((resolve, reject) => {
            commit('toggleLoading');
            axios.post('/api/current-user/').then(response => {
                if(response.status == 403) {
                    commit('setIsLoggedIn', false);
                    commit('setCurrentUser', {});
                    //router.push('/login');
                }
                else if(response.status == 200) {
                    commit('setIsLoggedIn', true);
                    commit('setCurrentUser', response.data);
                }
                commit('toggleLoading');
                resolve();
            }).catch(error => {
                commit('toggleLoading');
                reject();
            })
        })
    },
    getSettings({commit, state}) {
        axios.get('/api/settings/').then(response => {
            response.data.results.forEach(setting => commit('setSetting', setting));
        });
    }
}