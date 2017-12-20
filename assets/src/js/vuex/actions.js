export default {
    login({commit}) {
        state.pending = true;
        //AJAX call for logging in
        state.pending = false;
    },
    logout({commit}) {
        state.pending = true;
        //AJAX call for logging out
        state.isLoggedIn = false;
        state.pending = false;
    },
    getCurrentUser({commit}) {
        state.pending = true;
        //AJAX call to fetch the current user
        state.user
    }
}