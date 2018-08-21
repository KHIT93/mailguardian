<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex">
            <div class="card min-w-full table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Number of messages</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in dates" :key="item.date">
                            <td>{{ item.timestamp }}</td>
                            <td>{{ item.id__count }}</td>
                        </tr>
                        <tr>
                        <tr class="font-extrabold border-t-2 text-base">
                            <td>Total</td>
                            <td>{{ messageTotalCount }}</td>
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
export default {
    data: () => {
        return {
            dates: [],
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
        ...mapGetters(['filters'])
    },
    methods: {
        get() {
            this.setLoading(true);
            (new Form(this.activeFilters)).post('/api/reports/messages-per-hour/').then(data => {
                this.dates = data;
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