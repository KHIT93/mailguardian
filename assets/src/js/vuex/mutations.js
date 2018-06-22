import uuidv1 from 'uuid/v1';
export default {
    setIsLoggedIn(state, isLoggedIn) {
        state.isLoggedIn = isLoggedIn;
    },
    setCurrentUser(state, user) {
        state.user = user;
    },
    toggleLoading(state) {
        state.loading = !state.loading;
    },
    setFilter(state, { field, operator, value}) {
        state.report.filters[field] = { operator: operator, value: value };
    },
    removeFilter(state, filter) {
        state.report.filters[filter] = null;
    },
    resetFilters(state) {
        state.report.filters = {
            from_address: null,
            from_domain: null,
            to_address: null,
            to_domain: null,
            subject: null,
            client_ip: null,
            mailscanner_hostname: null,
            timestamp: null,
            whitelisted: null,
            blacklisted: null,
            is_spam: null,
            is_rbl_listed: null,
            quarantined: null,
            infected: null
        };
    },
    notify(state, notification) {
        return state.notifications.push(notification);
    },
    purgeNotification(state, notification = null) {
        if (notification) {
            //Find notification in array and remove it
            state.notifications.splice(state.notifications.indexOf(notification), 1);
        }
        else {
            state.notifications.filter(n => n.persistent == false).shift();
        }
    },
    setWizardPayload(state, payload = null) {
        state.wizard.payload = payload;
    },
    setSettings(state, payload = null) {
        payload.forEach((setting) => {
            state.settings[setting.key] = setting.value;
        });
    }
}