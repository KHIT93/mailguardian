<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex">
            <div class="card min-w-full table-wrapper">
                <mg-bar-chart :chart-data="chart" :height="200" />
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Number of messages</th>
                            <th>Clean</th>
                            <th>Spam</th>
                            <th>Infected</th>
                            <th>Volume</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in dates" :key="item.date">
                            <td>{{ item.date }}</td>
                            <td>{{ item.id__count }}</td>
                            <td>{{ clean_count(item) }} ({{ clean_pct(item) }}%)</td>
                            <td>{{ item.is_spam_count }} ({{ spam_pct(item) }}%)</td>
                            <td>{{ item.infected_count }} ({{ infected_pct(item) }}%)</td>
                            <td>{{ item.size__sum | byte_display }}</td>
                        </tr>
                        <tr class="font-extrabold border-t-2 text-base">
                            <td>Total ({{ dates.length }} days)</td>
                            <td>{{ messageTotalCount }}</td>
                            <td>{{ messageTotalClean }}</td>
                            <td>{{ messageTotalSpam }}</td>
                            <td>{{ messageTotalInfected }}</td>
                            <td>{{ messageTotalSize | byte_display }}</td>
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
import BarChart from '../../components/BarChart.vue';
export default {
    components: {
        'mg-bar-chart': BarChart
    },
    data: () => {
        return {
            dates: [],
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
        messageTotalCount() {
            let total = 0;
            this.dates.forEach(item => {
                total += item.id__count;
            });
            return total;
        },
        messageTotalClean() {
            let clean = 0;
            this.dates.forEach(item => {
                clean += this.clean_count(item);
            })
            return clean;
        },
        messageTotalSpam() {
            let total = 0;
            this.dates.forEach(item => {
                total += item.is_spam_count;
            });
            return total;
        },
        messageTotalInfected() {
            let total = 0;
            this.dates.forEach(item => {
                total += item.infected_count;
            });
            return total;
        },
        messageTotalSize() {
            let total = 0;
            this.dates.forEach(item => {
                total += item.size__sum;
            });
            return total;
        },
        ...mapGetters(['filters'])
    },
    methods: {
        get() {
            this.setLoading(true);
            (new Form(this.activeFilters)).post('/api/reports/messages-by-date/').then(data => {
                this.dates = data;
                this.chart = {
                    labels: this.dates.map(item => item.date),
                    datasets: [
                        {
                            label: 'Clean',
                            backgroundColor: '#3490DC',
                            data: this.dates.map(item => this.clean_count(item))
                        },
                        {
                            label: 'Spam',
                            backgroundColor: '#F9ACAA',
                            data: this.dates.map(item => item.is_spam_count)
                        },
                        {
                            label: 'Infected',
                            backgroundColor: '#E3342F',
                            data: this.dates.map(item => item.infected_count)
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
        clean_count(item) {
            let count = 0;
            count = item.id__count;
            count -= item.is_spam_count;
            count -= item.infected_count;
            
            return count;
        },
        clean_pct(item) {
            return Math.round((this.clean_count(item) / item.id__count) * 100);
        },
        spam_pct(item) {
            return Math.round((item.is_spam_count / item.id__count) * 100);
        },
        infected_pct(item) {
            return Math.round((item.infected_count / item.id__count) * 100);
        },
        ...mapMutations(['toggleLoading', 'setLoading'])
    }
}
</script>