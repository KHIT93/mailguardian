<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="card p-2">
            <h2 class="font-normal text-center mb-2">SpamAssasin Rule management</h2>
            <p>Here you can manage the sa-rules that have been created on the system</p>
            <div class="card table-wrapper">
                <table class="table text-sm">
                    <thead>
                        <tr>
                            <th>Rule</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="count == 0">
                            <td colspan="2">There are currently no SpamAssassin rules to display</td>
                        </tr>
                        <tr v-for="item in rules" :key="item.id" v-else @click="edit(item.id)">
                            <td>{{ item.name }}</td>
                            <td>{{ item.score }}</td>
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
                <router-link to="/admin/spamassassin/rules/add" class="btn btn-blue shadow">
                    Add SpamAssasin Rule
                </router-link>
            </div>
        </div>
    </div>
</mg-page>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex';
import router from '../../../../routing/router';
export default {
    data: () => {
        return {
            rules: [],
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
            axios.get('/api/sa-rules/'+qs).then(response => {
                this.rules = response.data.results;
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
        edit(id) {
            router.push('/admin/spamassassin/rules/'+id);
        },
        ...mapMutations(['setLoading'])
    }
}
</script>