export default {
    setIsLoggedIn(state, isLoggedIn) {
        state.isLoggedIn = isLoggedIn;
    },
    setCurrentUser(state, user) {
        state.user = user;
    },
    toggleLoading(state) {
        state.loading = !state.loading;
    }
}