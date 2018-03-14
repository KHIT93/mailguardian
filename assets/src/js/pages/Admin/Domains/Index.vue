<template>
    <mw-admin-layout>
        <h2 class="font-normal text-center mb-2">Domain management</h2>
        <p>Here you can manage the domains that have been created on the system</p>
        <div class="bg-white border sm:rounded shadow">
            <div class="flex shadow">
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        Domain
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        Relay type
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        Destination
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        Allowed email accounts
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r px-2 py-2 font-semibold">
                    <div class="">
                        Created
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 px-2 py-2 font-semibold">
                    <div class="">
                        Changed
                    </div>
                </div>
            </div>
            <div class="flex text-sm break-words items-center p-2" v-if="count == 0">
                <p>There are currently no domains to display</p>
            </div>
            <div class="flex hover:bg-grey-lighter text-sm cursor-pointer break-words" v-for="item in domains" :key="item.id" v-else @click="edit(item.id)">
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
                    <div class="">
                        <p>{{ item.name }}</p>
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r p-2">
                    <div class="">
                        <p>{{ item.relay_type }}</p>
                    </div>
                </div>
                <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
                    <div class="">
                        <p>{{ item.destination }}</p>
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r p-2">
                    <div class="">
                        <p v-if="item.allowed_accounts == -1">Unlimited</p>
                        <p v-else>{{ item.allowed_accounts }}</p>
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r p-2">
                    <div class="">
                        <p>{{ moment(item.created_timestamp).fromNow() }}</p>
                    </div>
                </div>
                <div class="text-grey-darker hidden sm:block sm:w-1/5 p-2">
                    <div class="">
                        <p>{{ moment(item.updated_timestamp).fromNow() }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="inline-flex pt-2 rounded" v-if="page_count > 1">
            <button @click="previous" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded-l" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : current == 1}">
                Prev
            </button>
            <button @click="next" class="bg-grey-light hover:bg-grey text-grey-darkest py-2 px-4 rounded-r" :class="{'select-none cursor-not-allowed bg-grey-lightest hover:bg-grey-lightest' : current == page_count}">
                Next
            </button>
        </div>
        <div class="mt-4 mb-2">
            <router-link to="/admin/domains/add" class="flex-no-shrink bg-blue hover:bg-blue-dark border-blue hover:border-blue-dark text-sm border-4 text-white py-1 px-2 rounded shadow no-underline">
                Add Domain
            </router-link>
        </div>
    </mw-admin-layout>
</template>
<script>
import { mapGetters } from 'vuex';
import router from '../../../routing/router';
import AdminLayout from '../../../components/AdminLayout.vue';
export default {
    data: () => {
        return {
            domains: [],
            count: 0,
            search: null,
            current: 1,
            page_count: 1
        }
    },
    components: {
        'mw-admin-layout': AdminLayout
    },
    mounted() {
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
            axios.get('/api/domains/'+qs).then(response => {
                this.domains = response.data.results;
                this.count = response.data.count;
                this.current = response.data.current;
                this.page_count = response.data.page_count;
            });
        },
        moment(str) {
            return window.moment(str);
        },
        next() {
            page = this.domains.next.split("?page=")[1];
            this.get(this.search, page);
        },
        previous() {
            page = this.domains.previous.split("?page=")[1];
            this.get(this.search, page);
        },
        edit(id) {
            router.push('/admin/domains/'+id);
        }
    }
}
</script>