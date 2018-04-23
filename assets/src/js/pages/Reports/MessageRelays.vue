<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex">
            <div class="bg-white border sm:rounded shadow min-w-full table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Sender</th>
                            <th>Number of messages</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in senders" :key="item.date">
                            <td>{{ item.client_ip }}</td>
                            <td>{{ item.id__count }}</td>
                        </tr>
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
            senders: [],
        }
    },
    mounted() {
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
            this.senders.forEach(item => {
                total += item.id__count;
            });
            return total;
        },
        ...mapGetters(['filters'])
    },
    methods: {
        get() {
            this.toggleLoading();
            (new Form(this.activeFilters)).post('/api/reports/top-mail-relays/').then(data => {
                this.senders = data;
                this.toggleLoading();
            }).catch(error => {
                //Handle error
                console.log(error);
                this.toggleLoading();
            });
        },
        ...mapMutations(['toggleLoading'])
    }
}
</script>