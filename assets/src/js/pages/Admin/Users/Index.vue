<template>
    <div class="container mx-auto sm:px-2 pt-2 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <h2 class="font-normal text-center mb-2">User management</h2>
            <p>Here you can manage the users that have been created on the system</p>
            <div class="bg-white border sm:rounded shadow">
                <div class="flex shadow">
                    <div class="text-grey-darker w-1/3 sm:w-1/5 border-r px-2 py-2 font-semibold">
                        <div class="">
                            Email
                        </div>
                    </div>
                    <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r px-2 py-2 font-semibold">
                        <div class="">
                            First name
                        </div>
                    </div>
                    <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r px-2 py-2 font-semibold">
                        <div class="">
                            Last name
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/3 sm:w-1/5 border-r px-2 py-2 font-semibold">
                        <div class="">
                            Staff member
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/3 sm:w-1/5 border-r px-2 py-2 font-semibold">
                        <div class="">
                            Domain Administrator
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/3 sm:w-1/5 px-2 py-2 font-semibold">
                        <div class="">
                            Domain
                        </div>
                    </div>
                </div>
                <div class="flex text-sm break-words items-center p-2" v-if="count == 0">
                    <p>There are currently no users to display</p>
                </div>
                <div class="flex hover:bg-grey-lighter text-sm cursor-pointer break-words" v-for="item in users" :key="item.id" v-else @click="edit(item.id)">
                    <div class="text-grey-darker w-1/3 sm:w-1/5 border-r p-2">
                        <div class="">
                            <p>{{ item.email }}</p>
                        </div>
                    </div>
                    <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r p-2">
                        <div class="">
                            <p>{{ item.first_name }}</p>
                        </div>
                    </div>
                    <div class="text-grey-darker hidden sm:block sm:w-1/5 border-r p-2">
                        <div class="">
                            <p>{{ item.last_name }}</p>
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/3 sm:w-1/5 sm:w-1/5 border-r p-2">
                        <div class="text-grey-darker p-2">
                            <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green': item.is_staff, 'bg-grey': !item.is_staff }" >
                                    {{ item.is_staff | yesno }}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/3 sm:w-1/5 sm:w-1/5 border-r p-2">
                        <div class="text-grey-darker p-2">
                            <div class="items-center text-white leading-none lg:rounded-full flex lg:inline-flex">
                                <span class="flex rounded-full uppercase px-2 py-1 text-xs font-bold" :class="{ 'bg-green': item.mailuser.is_domain_admin, 'bg-grey': !item.mailuser.is_domain_admin }" >
                                    {{ item.mailuser.is_domain_admin | yesno }}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="text-grey-darker w-1/3 sm:w-1/5 sm:w-1/5 p-2">
                        <div class="">
                            <p v-if="item.mailuser">{{ item.mailuser.domain_id }}</p>
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
                <router-link to="/admin/users/add" class="flex-no-shrink bg-blue hover:bg-blue-dark border-blue hover:border-blue-dark text-sm border-4 text-white py-1 px-2 rounded shadow no-underline">
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
            axios.get('/api/users/'+qs).then(response => {
                //this.users = response.data.results.splice(-1, 1);
                this.users = response.data.results;
                if (this.users.filter(u => u.username === "AnonymousUser")) {
                    this.users = this.users.splice(-1, 1);
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