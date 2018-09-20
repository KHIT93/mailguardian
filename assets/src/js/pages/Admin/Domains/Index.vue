<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card p-2">
            <h2 class="font-normal text-center mb-2">Domain management</h2>
            <p>Here you can manage the domains that have been created on the system</p>
            <div class="card table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Domain</th>
                            <th class="hidden md:table-cell">Relay type</th>
                            <th>Destination</th>
                            <th class="hidden md:table-cell">Allowed email accounts</th>
                            <th class="hidden md:table-cell">Created</th>
                            <th class="hidden md:table-cell">Changed</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="count == 0">
                            <td colspan="6">There are currently no domains to display</td>
                        </tr>
                        <tr v-for="item in domains" :key="item.id" v-else @click="edit(item.id)">
                            <td>{{ item.name }}</td>
                            <td class="hidden md:table-cell">{{ item.relay_type }}</td>
                            <td>{{ item.destination }}</td>
                            <td class="hidden md:table-cell" v-if="item.allowed_accounts == -1">Unlimited</td>
                            <td class="hidden md:table-cell" v-else>{{ item.allowed_accounts }}</td>
                            <td class="hidden md:table-cell">{{ moment(item.created_timestamp).fromNow() }}</td>
                            <td class="hidden md:table-cell">{{ moment(item.updated_timestamp).fromNow() }}</td>
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
                <router-link to="/admin/domains/add" class="btn btn-blue shadow">
                    Add Domain
                </router-link>
            </div>
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
            domains: [],
            count: 0,
            search: null,
            current: 1,
            page_count: 1,
            next_link: '',
            previous_link: ''
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
            axios.get('/api/domains/'+qs).then(response => {
                this.domains = response.data.results;
                this.count = response.data.count;
                this.current = response.data.current;
                this.page_count = response.data.page_count;
                this.next_link = response.data.next;
                this.previous_link = response.data.previous;
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
            });
        },
        moment(str) {
            return window.moment(str);
        },
        next() {
            let page = this.next_link.split("?page=")[1];
            this.get(this.search, page);
        },
        previous() {
            let page = this.previous_link.split("?page=")[1];
            this.get(this.search, page);
        },
        edit(id) {
            router.push('/admin/domains/'+id);
        },
        ...mapMutations(['setLoading'])
    }
}
</script>