<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card p-2">
            <h2 class="font-normal text-center mb-2">Notification management</h2>
            <p>Here you can manage the notifications that have been created on the system</p>
            <div class="card card-no-shadow card-no-border table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Body</th>
                            <th>Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="count == 0">
                            <td colspan="3">There are currently no notifications to display</td>
                        </tr>
                        <tr v-for="item in notifications" :key="item.id" v-else @click="edit(item.id)">
                            <td>{{ item.title }}</td>
                            <td>{{ item.body }}</td>
                            <td>{{ item.notification_type }}</td>
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
                <router-link to="/admin/notifications/add" class="btn btn-blue shadow">
                    Add Notification
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
            notifications: [],
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
            axios.get('/api/notifications/'+qs).then(response => {
                this.notifications = response.data.results;
                this.count = response.data.count;
                this.current = response.data.current;
                this.page_count = response.data.page_count;
                this.next = response.data.next;
                this.previous = response.data.previous;
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
            router.push('/admin/notifications/'+id);
        },
        ...mapMutations(['setLoading'])
    }
}
</script>