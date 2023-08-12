export default class Metric {
    constructor(hostname, protocol) {
        this.hostname = hostname
        this.protocol = protocol
        this.active = false
        this.loading = false
        this.timestamp = false
    }

    async get() {
        let res = false
        this.loading = true
        try {
            res = (await useBackendFetch(`${this.protocol}://${this.hostname}/host/metrics/`))
            this.active = true
        }
        catch (error) {
            console.log(error)
            this.active = false
        }
        if (res) {
            this.cpu_usage = res.cpu_load
            this.ram_usage = res.ram_usage
            this.queue = res.queue || 0
        }
        this.loading = false
        this.timestamp = new Date()
    }
}