<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card">
            <div class="flex flex-row-reverse p-2 bg-grey-lightest">
                <div class="mt-2">
                    <button @click="get(interval)" type="button" class="bg-blue hover:bg-blue-dark no-underline text-white font-semibold py-2 px-4 border border-blue hover:border-bleu-dark text-sm rounded">Refresh</button>
                    <button @click="get('last_hour')" type="button" class="bg-white hover:bg-blue no-underline text-blue-dark font-semibold hover:text-white py-2 px-4 border border-blue hover:border-transparent text-sm rounded">Last hour</button>
                    <button @click="get('today')" type="button" class="bg-white hover:bg-blue no-underline text-blue-dark font-semibold hover:text-white py-2 px-4 border border-blue hover:border-transparent text-sm rounded">Today</button>
                    <button @click="get('last_day')" type="button" class="bg-white hover:bg-blue no-underline text-blue-dark font-semibold hover:text-white py-2 px-4 border border-blue hover:border-transparent text-sm rounded">Last day</button>
                </div>
            </div>
            <div class="pt-2 border-b bg-grey-lightest"></div>
            <div class="sm:flex sm:justify-between">
                <div class="sm:w-1/3 text-center text-grey-darker py-6">
                    <div class="sm:border-r">
                        <div class="mb-2">
                            <span class="text-5xl">{{ daily_total }}</span>
                        </div>
                        <div class="uppercase">
                            Total emails handled
                        </div>
                    </div>
                </div>
                <div class="sm:w-1/3 text-center text-grey-darker py-6">
                    <div class="sm:border-r">
                        <div class="mb-2">
                            <span class="text-5xl">{{ daily_spam }}</span>
                        </div>
                        <div class="uppercase">
                            Spam emails handled
                        </div>
                    </div>
                </div>
                <div class="sm:w-1/3 text-center text-grey-darker py-6">
                    <div>
                        <div class="mb-2">
                            <span class="text-5xl">{{ daily_virus }}</span>
                        </div>
                        <div class="uppercase">
                            Viruses handled
                        </div>
                    </div>
                </div>
            </div>
            <!-- Chart.js graph here for showing message stats -->
            <mg-dashboard-chart :chart-data="chart" :height="chartheight" v-show="chart.labels.length > 0"></mg-dashboard-chart>
        </div>
    </div>
</template>

<script>
    import Modal from '../components/Modal.vue';
    import DashboardChart from '../components/DashboardChart.vue';
    import { mapMutations } from 'vuex';
    export default {
        data: () => {
            return {
                chartdata: [],
                modal: false,
                daily_total: 0,
                daily_spam: 0,
                daily_virus: 0,
                chart: {
                    labels: [],
                    datasets: []
                },
                chartheight: 150,
                interval: 'last_hour'
            }
        },
        created() {
            this.setLoading(false);
            this.get(this.interval);
        },
        methods: {
            get(interval = 'last_hour') {
                this.interval = interval;
                axios.post('/api/dashboard/', {'interval' : interval}).then(response => {
                    this.daily_total = response.data.daily_total;
                    this.daily_spam = response.data.daily_spam;
                    this.daily_virus = response.data.daily_virus;
                    this.chartdata = response.data.chart_data;
                    this.chart = {
                        labels: (this.chartdata.length) ? this.chartdata.map(m => m[0]) : [],
                        datasets: [
                            {
                                label: 'Messages',
                                backgroundColor: '#3490DC',
                                data: (this.chartdata.length) ? this.chartdata.map(m => m[1]) : []
                            },
                            {
                                label: 'Viruses',
                                backgroundColor: '#E3342F',
                                data: (this.chartdata.length) ? this.chartdata.map(m => m[3]) : []
                            },
                            {
                                label: 'Spam',
                                backgroundColor: '#F9ACAA',
                                data: (this.chartdata.length) ? this.chartdata.map(m => m[2]) : []
                            }
                        ]
                    }
                });
            },
            ...mapMutations(['setLoading', 'toggleLoading'])
        },
        components: {
            'mg-modal': Modal,
            'mg-dashboard-chart': DashboardChart
        },
    }
</script>
