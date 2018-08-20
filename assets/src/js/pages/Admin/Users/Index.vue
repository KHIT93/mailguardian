<template>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card">
            <h2 class="font-normal text-center mb-2">User management</h2>
            <p>Here you can manage the users that have been created on the system</p>
            <div class="card table-wrapper">
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
                                    <span class="badge-inner" :class="{ 'bg-green': item.is_staff, 'bg-grey': !item.is_staff }" >
                                        {{ item.is_staff | yesno }}
                                    </span>
                                </div>
                            </td>
                            <td>
                                <div class="badge">
                                    <span class="badge-inner" :class="{ 'bg-green': item.is_domain_admin, 'bg-grey': !item.is_domain_admin }" >
                                        {{ item.is_domain_admin | yesno }}
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
                <router-link to="/admin/users/add" class="btn btn-blue shadow">
                    Add User
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
            users: [],
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
            axios.get('/api/users/'+qs).then(response => {
                //this.users = response.data.results.splice(-1, 1);
                this.users = response.data.results;
                if (this.users.filter(u => u.email === "AnonymousUser")) {
                    this.users = this.users.filter(u => u.email !== "AnonymousUser");
                }
                this.count = response.data.count;
                this.current = response.data.current;
                this.page_count = response.data.page_count;

            });
        },
        moment(str) {
            return window.moment(str);
        },
        next() {
            page = this.users.next.split("?page=")[1];
            this.get(this.search, page);
        },
        previous() {
            page = this.users.previous.split("?page=")[1];
            this.get(this.search, page);
        },
        edit(id) {
            router.push('/admin/users/'+id);
        }
    }
}
</script>