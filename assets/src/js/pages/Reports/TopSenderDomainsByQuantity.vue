<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex">
            <div class="card min-w-full table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Sending domain</th>
                            <th>Number of messages</th>
                            <th>Volume</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in data" :key="item.date">
                            <td>{{ item.from_domain }}</td>
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
        ...mapGetters(['filters'])
    },
    methods: {
        get() {
            this.setLoading(true);
            (new Form(this.activeFilters)).post('/api/reports/top-sender-domains-by-quantity/').then(data => {
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