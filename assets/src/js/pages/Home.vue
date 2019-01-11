<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div>
            <mg-notification v-for="message in dashboard_notifications" :key="message.id" :notification="{ title: message.title, message: message.body, type: 'info' }"/>
        </div>
        <div class="">
            <!-- <div class="flex flex-row-reverse p-2 bg-grey-lightest">
                <div class="mt-2">
                    <button @click="get(interval)" type="button" class="bg-blue hover:bg-blue-dark no-underline text-white font-semibold py-2 px-4 border border-blue hover:border-bleu-dark text-sm rounded">Refresh</button>
                    <button @click="get('last_hour')" type="button" class="bg-white hover:bg-blue no-underline text-blue-dark font-semibold hover:text-white py-2 px-4 border border-blue hover:border-transparent text-sm rounded">Last hour</button>
                    <button @click="get('today')" type="button" class="bg-white hover:bg-blue no-underline text-blue-dark font-semibold hover:text-white py-2 px-4 border border-blue hover:border-transparent text-sm rounded">Today</button>
                    <button @click="get('last_day')" type="button" class="bg-white hover:bg-blue no-underline text-blue-dark font-semibold hover:text-white py-2 px-4 border border-blue hover:border-transparent text-sm rounded">Last day</button>
                </div>
            </div> -->
            <!-- <div class="pt-2 border-b bg-grey-lightest"></div> -->
            <div class="sm:flex sm:justify-between">
                <div class="sm:w-1/3 text-center text-grey-darker card sm:mr-1 py-3">
                    <div class="p-2">
                        <div class="mb-2">
                            <span class="text-5xl">{{ daily_total }}</span>
                        </div>
                        <div class="uppercase">
                            Total emails handled
                        </div>
                    </div>
                </div>
                <div class="sm:w-1/3 text-center text-grey-darker card sm:mx-1 py-3 my-2 sm:my-0">
                    <div class="p-2">
                        <div class="mb-2">
                            <span class="text-5xl">{{ daily_spam }}</span>
                        </div>
                        <div class="uppercase">
                            Spam emails handled
                        </div>
                    </div>
                </div>
                <div class="sm:w-1/3 text-center text-grey-darker card sm:ml-1 py-3">
                    <div class="p-2">
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
            <mg-dashboard-chart class="mt-2 card" :chart-data="chart" :height="chartheight" v-show="chart.labels.length > 0"></mg-dashboard-chart>
        </div>
    </div>
</mg-page>
</template>

<script>
    import Modal from '../components/Modal.vue';
    import AppNotification from '../components/Notification.vue';
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
                interval: 'daily',
                dashboard_notifications: []
            }
        },
        created() {
            this.setLoading(true);
            this.get(this.interval);
            this.getNotifications();
        },
        methods: {
            get(interval = 'daily') {
                this.interval = interval;
                axios.post('/api/dashboard/', {'interval' : interval}).then(response => {
                    this.daily_total = response.data.daily_total;
                    this.daily_spam = response.data.daily_spam;
                    this.daily_virus = response.data.daily_virus;
                    this.chartdata = response.data.chart_data;
                    this.chart = {
                        labels: (this.chartdata.length) ? this.chartdata.map(m => moment(m[0]).format('HH:mm')) : [],
                        datasets: [
                            {
                                label: 'Messages',
                                backgroundColor: '#3490DC',
                                lineTension: 0,
                                radius: 0,
                                data: (this.chartdata.length) ? this.chartdata.map(m => m[1]) : []
                            },
                            {
                                label: 'Viruses',
                                backgroundColor: '#E3342F',
                                lineTension: 0,
                                radius: 0,
                                data: (this.chartdata.length) ? this.chartdata.map(m => m[3]) : []
                            },
                            {
                                label: 'Spam',
                                backgroundColor: '#F9ACAA',
                                lineTension: 0,
                                radius: 0,
                                data: (this.chartdata.length) ? this.chartdata.map(m => m[2]) : []
                            }
                        ]
                    }
                    this.setLoading(false);
                }).catch(error => {
                    this.setLoading(false);
                });
            },
            getNotifications() {
                this.setLoading(true);
                axios.get('/api/notifications/dashboard/').then(response => {
                    this.dashboard_notifications = response.data;
                }).catch(error => {
                    this.setLoading(false);
                });
            },
            ...mapMutations(['setLoading', 'toggleLoading'])
        },
        components: {
            'mg-modal': Modal,
            'mg-dashboard-chart': DashboardChart,
            'mg-notification': AppNotification
        },
    }
</script>
