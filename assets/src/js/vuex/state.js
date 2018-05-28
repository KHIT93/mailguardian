let Cookies = require('js-cookie');

export default {
    isLoggedIn: false,
    user: {},
    loading: false,
    notifications: [],
    csrftoken: Cookies.get('csrftoken'),
    report: {
        filters: {
            from_address: null,
            from_domain: null,
            to_address: null,
            to_domain: null,
            subject: null,
            client_ip: null,
            mailscanner_hostname: null,
            date: null,
            whitelisted: null,
            blacklisted: null,
            is_spam: null,
            is_rbl_listed: null,
            quarantined: null,
            infected: null
        },
        filter_options: {
            from_address: {
                operators: [
                    { label: 'equals', value: '=' },
                    { label: 'does not equal', value: '<>' },
                    { label: 'contains', value: 'icontains' }
                ],
                field_type: 'text'
            },
            from_domain: {
                operators: [
                    { label: 'equals', value: '=' },
                    { label: 'does not equal', value: '<>' },
                    { label: 'contains', value: 'icontains' }
                ],
                field_type: 'text'
            },
            to_address: {
                operators: [
                    { label: 'equals', value: '=' },
                    { label: 'does not equal', value: '<>' },
                    { label: 'contains', value: 'icontains' }
                ],
                field_type: 'text'
            },
            to_domain: {
                operators: [
                    { label: 'equals', value: '=' },
                    { label: 'does not equal', value: '<>' },
                    { label: 'contains', value: 'icontains' }
                ],
                field_type: 'text'
            },
            subject: {
                operators: [
                    { label: 'equals', value: '=' },
                    { label: 'does not equal', value: '<>' },
                    { label: 'contains', value: 'icontains' }
                ],
                field_type: 'text'
            },
            client_ip: {
                operators: [
                    { label: 'equals', value: '=' },
                    { label: 'does not equal', value: '<>' }
                ],
                field_type: 'text'
            },
            mailscanner_hostname: {
                operators: [
                    { label: 'equals', value: '=' },
                    { label: 'does not equal', value: '<>' }
                ],
                field_type: 'text'
            },
            date: {
                operators: [
                    { label: 'equals', value: '=' },
                    { label: 'does not equal', value: '<>' },
                    { label: 'greater than', value: 'gt' },
                    { label: 'greater than or equals', value: 'gte' },
                    { label: 'less than', value: 'lt'},
                    { label: 'less than or equals', value: 'lte'}
                ],
                field_type: 'date'
            },
            whitelisted: {
                operators: [
                    { label: 'yes', value: 1},
                    { label: 'no', value: 0}
                ],
                field_type: 'boolean'
            },
            blacklisted: {
                operators: [
                    { label: 'yes', value: 1},
                    { label: 'no', value: 0}
                ],
                field_type: 'boolean'
            },
            is_spam: {
                operators: [
                    { label: 'yes', value: 1},
                    { label: 'no', value: 0}
                ],
                field_type: 'boolean'
            },
            is_rbl_listed: {
                operators: [
                    { label: 'yes', value: 1},
                    { label: 'no', value: 0}
                ],
                field_type: 'boolean'
            },
            quarantined: {
                operators: [
                    { label: 'yes', value: 1},
                    { label: 'no', value: 0}
                ],
                field_type: 'boolean'
            },
            infected: {
                operators: [
                    { label: 'yes', value: 1},
                    { label: 'no', value: 0}
                ],
                field_type: 'boolean'
            }
        }
    },
    wizard: {
        payload: null
    }
}