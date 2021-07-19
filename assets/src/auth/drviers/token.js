export default {

    request: function (req, token) {
        this.drivers.http.setHeaders.call(this, req, {
            Authorization: 'Token ' + token
        });
    },

    response: function (res) {
        let response_data = this.drivers.http.httpData.call(this, res)
        if (response_data) {
            return response_data.key
        }
    }
};