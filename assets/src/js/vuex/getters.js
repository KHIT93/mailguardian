let Cookies = require('js-cookie');
export default {
    user(state) {
        return state.user;
    },
    isLoggedIn(state) {
        return state.isLoggedIn;
    },
    loading(state) {
        return state.loading;
    },
    filters(state) {
        return state.report.filters;
    }
}