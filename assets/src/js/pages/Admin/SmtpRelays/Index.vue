<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-6 pb-8">
        <div class="card p-2">
            <h2 class="font-normal text-center mb-2">Relay management</h2>
            <p>Here you can manage the hosts, which are allowed to send mail through your deployed node(s)</p>
            <div class="w-full py-2">
                <form @submit.prevent="get_search">
                    <div class="flex text-sm items-center">
                        <input type="text" name="search" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" v-model="search" placeholder="Type something here..."/>
                        <button type="submit" class="btn btn-blue shadow">
                            Search
                        </button>
                    </div>
                </form>
            </div>
            <div class="card card-no-shadow card-no-border table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>IP Address</th>
                            <th>Hostname</th>
                            <th>Active</th>
                            <th>Comment</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="count == 0">
                            <td colspan="6">There are currently no SMTP relays to display</td>
                        </tr>
                        <tr v-for="item in smtp_relays" :key="item.id" v-else @click="edit(item.id)">
                            <td>{{ item.ip_address }}</td>
                            <td>{{ item.hostname }}</td>
                            <td>
                                <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                    <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green-500': item.active, 'bg-red-500': !item.active }" >
                                        {{ item.active | yesno }}
                                    </span>
                                </div>
                            </td>
                            <td>{{ item.comment }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="inline-flex pt-2 rounded" v-if="page_count > 1">
                <button @click="previous" class="btn rounded-none rounded-l" :class="{'select-none cursor-not-allowed btn-gray-lightest' : current == 1, 'btn-gray-400' : current != 1}">
                    Prev
                </button>
                <button @click="next" class="btn rounded-none rounded-r" :class="{'select-none cursor-not-allowed btn-gray-lightest' : current == page_count, 'btn-gray-400' : current != page_count}">
                    Next
                </button>
            </div>
            <div class="mt-4 mb-2">
                <router-link to="/admin/smtp-relays/add" class="btn btn-blue shadow">
                    Add Relay
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
            smtp_relays: [],
            count: 0,
            search: null,
            current: 1,
            page_count: 1,
            next_link: '',
            prev_link: '',
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
            axios.get('/api/smtp-relays/'+qs).then(response => {
                this.smtp_relays = response.data.results;
                this.count = response.data.count;
                this.current = response.data.current;
                this.page_count = response.data.page_count;
                this.next_link = response.data.next;
                this.prev_link = response.data.previous;
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
            });
        },
        moment(str) {
            return window.moment(str);
        },
        next() {
            page = this.next_link.split("?page=")[1];
            this.get(this.search, page);
        },
        previous() {
            page = this.prev_link.split("?page=")[1];
            this.get(this.search, page);
        },
        async get_search() {
            await this.get(this.search);
            this.search = null;
        },
        edit(id) {
            router.push('/admin/smtp-relays/'+id);
        },
        ...mapMutations(['setLoading'])
    }
}
</script>