<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="card p-2 table-wrapper">
            <table class="table text-sm cursor-pointer break-words">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Module</th>
                        <th>Record ID</th>
                        <th>Action</th>
                        <th>By</th>
                        <th>IP Address</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="entry in log" :key="entry.id" @click="detail(entry.id)">
                        <td>{{ entry.timestamp | ago }}</td>
                        <td>{{ entry.content_type_name }}</td>
                        <td>{{ entry.object_pk }}</td>
                        <td>{{ entry.action_name }}</td>
                        <td>{{ entry.actor_email }}</td>
                        <td>{{ entry.remote_addr }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</mg-page>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex';
import router from '../../../routing/router';
export default {
    data: () => {
        return {
            log: []
        }
    },
    computed: {
        ...mapGetters(['user'])
    },
    created() {
        this.get()
    },
    methods: {
        get(query = null, page = null) {
            this.setLoading(true);
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
            axios.get('/api/datalog/'+qs).then(response => {
                this.log = response.data.results;
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
            });
        },
        detail(id) {
            router.push('/admin/audit-log/'+id);
        },
        ...mapMutations(['setLoading', 'notify'])
    }
}
</script>