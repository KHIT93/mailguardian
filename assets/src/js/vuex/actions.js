export default {
    login(context) {
        state.pending = true;
        //AJAX call for logging in
        state.pending = false;
    },
    logout(context) {
        state.pending = true;
        //AJAX call for logging out
        state.isLoggedIn = false;
        state.pending = false;
    }
}