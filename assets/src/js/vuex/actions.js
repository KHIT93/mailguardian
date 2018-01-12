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
                    console.log('You are not logged in. You should automatically be redirected to the login page');
                    commit('setIsLoggedIn', false);
                    commit('setCurrentUser', {});
                }
                else if(response.status == 200) {
                    console.log('You are logged in. You are allowed to proceed');
                    commit('setIsLoggedIn', true);
                    commit('setCurrentUser', response.data);
                }
                commit('toggleLoading');
            }).catch(error => {
                console.log('You are not logged in. You should automatically be redirected to the login page');
                commit('toggleLoading');
                reject();
            })
        })
    }
}