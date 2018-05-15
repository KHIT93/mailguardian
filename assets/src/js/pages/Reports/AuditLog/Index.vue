<template>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="bg-white border sm:rounded shadow p-2 table-wrapper">
            <table class="table text-sm cursor-pointer break-words">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Module</th>
                        <th>Action</th>
                        <th>Message</th>
                        <th>IP Address</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="entry in log" :key="entry.id">
                        <td>{{ entry.timestamp }}</td>
                        <td>{{ entry.module }}</td>
                        <td>{{ entry.action }}</td>
                        <td>{{ entry.message }}</td>
                        <td>{{ entry.ip_address }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex';
export default {
    data: () => {
        return {
            log: []
        }
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        get(query = null, page = null) {
            let qs = '';
            if (query) {
                qs = '?search='+query;
            }
            if (page) {
                qs = '?page='+page;
            }
            if (query && page) {
                qs = '?search='+query+'&page='+page;
            }
            axios.get('/api/audit-log/'+qs).then(response => {
                this.log = response.data.results;
            });
        },
        ...mapMutations(['toggleLoading', 'notify'])
    }
}
</script>