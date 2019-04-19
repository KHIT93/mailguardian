<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card">
            <h2 class="font-normal text-center mb-2">User management</h2>
            <p>Here you can manage the users that have been created on the system</p>
            <div class="w-full py-2">
                <form @submit.prevent="get_search">
                    <div class="flex text-sm items-center">
                        <input type="text" name="search" class="form-input" v-model="search" placeholder="Type something here..."/>
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
                            <th>Email</th>
                            <th>First name</th>
                            <th>Last name</th>
                            <th>Staff member</th>
                            <th>Domain Administrator</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="count == 0">
                            <td colspan="6">There are currently no users to display</td>
                        </tr>
                        <tr v-for="item in users" :key="item.id" v-else @click="edit(item.id)">
                            <td>{{ item.email }}</td>
                            <td>{{ item.first_name }}</td>
                            <td>{{ item.last_name }}</td>
                            <td>
                                <div class="badge">
                                    <span class="badge-inner" :class="{ 'bg-green-500': item.is_staff, 'bg-gray-500': !item.is_staff }" >
                                        {{ item.is_staff | yesno }}
                                    </span>
                                </div>
                            </td>
                            <td>
                                <div class="badge">
                                    <span class="badge-inner" :class="{ 'bg-green-500': item.is_domain_admin, 'bg-gray-500': !item.is_domain_admin }" >
                                        {{ item.is_domain_admin | yesno }}
                                    </span>
                                </div>
                            </td>
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
                <router-link to="/admin/users/add" class="btn btn-blue shadow">
                    Add User
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
            users: [],
            count: 0,
            search: null,
            current: 1,
            page_count: 1,
            next_Link: '',
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
            axios.get('/api/users/'+qs).then(response => {
                //this.users = response.data.results.splice(-1, 1);
                this.users = response.data.results;
                if (this.users.filter(u => u.email === "AnonymousUser")) {
                    this.users = this.users.filter(u => u.email !== "AnonymousUser");
                }
                this.next_Link = response.data.next;
                this.prev_link = response.data.previous;
                this.count = response.data.count;
                this.current = response.data.current;
                this.page_count = response.data.page_count;
                this.setLoading(false);

            }).catch(error => {
                this.setLoading(false);
            });
        },
        moment(str) {
            return window.moment(str);
        },
        next() {
            let page = this.next_Link.split("?page=")[1];
            this.get(this.search, page);
        },
        previous() {
            let page = this.prev_link.split("?page=")[1];
            this.get(this.search, page);
        },
        async get_search() {
            await this.get(this.search);
            this.search = null;
        },
        edit(id) {
            router.push('/admin/users/'+id);
        },
        ...mapMutations(['setLoading'])
    }
}
</script>