<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex">
            <div class="card min-w-full table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Sender</th>
                            <th>Summarized size</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in data" :key="item.date">
                            <td>{{ item.from_address }}</td>
                            <td>{{ item.size__count | byte_display }}</td>
                        </tr>
                        <tr>
                        <tr class="font-extrabold border-t-2 text-base">
                            <td>Total</td>
                            <td>{{ messageTotalCount | byte_display }}</td>
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
            data: [],
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
            this.data.forEach(item => {
                total += item.size__count;
            });
            return total;
        },
        ...mapGetters(['filters'])
    },
    methods: {
        get() {
            this.setLoading(true);
            (new Form(this.activeFilters)).post('/api/reports/top-senders-by-volume/').then(data => {
                this.data = data;
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