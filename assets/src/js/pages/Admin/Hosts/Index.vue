<template>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card p-2">
            <h2 class="font-normal text-center mb-2">Host management</h2>
            <p>Here you can manage the hosts that are part of your multi-node deployment</p>
            <div class="card table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Hostname</th>
                            <th>IP Address</th>
                            <th>Use TLS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="count == 0">
                            <td colspan="6">There are currently no hosts to display</td>
                        </tr>
                        <tr v-for="item in hosts" :key="item.id" v-else @click="edit(item.id)">
                            <td>{{ item.hostname }}</td>
                            <td>{{ item.ip_address }}</td>
                            <td>
                                <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                    <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green': item.use_tls, 'bg-red': !item.use_tls }" >
                                        {{ item.use_tls | yesno }}
                                    </span>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="inline-flex pt-2 rounded" v-if="page_count > 1">
                <button @click="previous" class="btn rounded-none rounded-l" :class="{'select-none cursor-not-allowed btn-grey-lightest' : current == 1, 'btn-grey-light' : current != 1}">
                    Prev
                </button>
                <button @click="next" class="btn rounded-none rounded-r" :class="{'select-none cursor-not-allowed btn-grey-lightest' : current == page_count, 'btn-grey-light' : current != page_count}">
                    Next
                </button>
            </div>
            <div class="mt-4 mb-2">
                <router-link to="/admin/hosts/add" class="btn btn-blue shadow">
                    Add Host
                </router-link>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
import router from '../../../routing/router';
export default {
    data: () => {
        return {
            hosts: [],
            count: 0,
            search: null,
            current: 1,
            page_count: 1
        }
    },
    created() {
        this.get();
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
            axios.get('/api/hosts/'+qs).then(response => {
                this.hosts = response.data.results;
                this.count = response.data.count;
                this.current = response.data.current;
                this.page_count = response.data.page_count;
            });
        },
        moment(str) {
            return window.moment(str);
        },
        next() {
            page = this.hosts.next.split("?page=")[1];
            this.get(this.search, page);
        },
        previous() {
            page = this.hosts.previous.split("?page=")[1];
            this.get(this.search, page);
        },
        edit(id) {
            router.push('/admin/hosts/'+id);
        }
    }
}
</script>