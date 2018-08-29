<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex">
            <div class="card min-w-full table-wrapper">
                <mg-pie-chart :chart-data="chart" :height="200" />
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Sender</th>
                            <th>Number of messages</th>
                            <th>Summarized size</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in data" :key="item.date">
                            <td>{{ item.from_address }}</td>
                            <td>{{ item.id__count }}</td>
                            <td>{{ item.size__sum | byte_display }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
<script>
import { mapMutations, mapGetters } from 'vuex';
import Form from '../../classes/Form';
import PieChart from '../../components/PieChart.vue';
export default {
    components: {
        'mg-pie-chart': PieChart
    },
    data: () => {
        return {
            data: [],
            chart: {
                labels: [],
                datasets: []
            }
        }
    },
    created() {
        this.get();
    },
    computed: {
        activeFilters() {
            return Object.keys(this.filters).filter(key => !!this.filters[key]).reduce((obj, key) => {
                obj[key] = this.filters[key];
                return obj;
            }, {})
        },
        ...mapGetters(['filters'])
    },
    methods: {
        get() {
            this.setLoading(true);
            (new Form(this.activeFilters)).post('/api/reports/top-senders-by-volume/').then(data => {
                this.data = data;
                this.chart = {
                    labels: this.data.map(item => item.from_address),
                    datasets: [
                        {
                            backgroundColor: [
                                '#F7b7b7',
                                '#CFDF49',
                                '#88d8f2',
                                '#07AF7B',
                                '#B9E3F9',
                                '#FFF3AD',
                                '#EF606A',
                                '#EC8833',
                                '#FFF100',
                                '#87C9A5'
                            ],
                            data: this.data.map(item => item.size__sum)
                        }
                    ]
                }
                this.toggleLoading();
            }).catch(error => {
                //Handle error
                console.log(error);
                this.toggleLoading();
            });
        },
        ...mapMutations(['toggleLoading', 'setLoading'])
    }
}
</script>