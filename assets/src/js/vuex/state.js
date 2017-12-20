let Cookies = require('js-cookie');

export default {
    isLoggedIn: !!Cookies.get('sessionid'),
    user: {},
    loading: false,
}