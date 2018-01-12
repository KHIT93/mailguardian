let Cookies = require('js-cookie');

export default {
    isLoggedIn: false,
    user: {},
    loading: false,
    report: {
        filters: {
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
        }
    }
}