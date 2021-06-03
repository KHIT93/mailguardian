<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-2 pt-6 pb-8">
        <div class="card p-2">
            <h2 class="font-normal text-center mb-2">MailScanner Configuration</h2>
            <p class="text-center">Here you can search, add, edit or remove data from the MailScanner configuration files</p>
            <p class="text-center text-red-500">Please only do changes to these settings if you are technically qualified to do so and make sure to consult the MailScanner documentation first</p>
            <div class="sm:flex card p-2 mt-2 mb-2 sm:items-center">
                <div class="sm:w-1/4">
                    <div class="p-2">
                        <router-link to="/admin/mailscanner/configuration/add" class="flex-shrink-0 bg-gray-100 hover:bg-gray-200 hover:border-gray-200 border-gray-100 text-sm border-4 text-gray-900 py-1 px-2 rounded shadow no-underline">
                            Add configuration option
                        </router-link>
                    </div>
                </div>
                <form @submit.prevent="search">
                <div>
                    <div class="flex text-sm items-center">
                        <div class="text-gray-700 w-3/4 md:w-5/6 p-2">
                            <div class="font-semibold">
                                <input type="text" name="search" class="form-input border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1" v-model="search_query" placeholder="Type something here..."/>
                            </div>
                        </div>
                        <div>
                            <div class="md:flex md:ml-2">
                                <div class="">
                                    <select v-model="search_file" class="form-select border-1 bg-gray-100 text-sm border-gray-100 pl-4 pr-4 text-gray-900 rounded w-full my-1">
                                        <option value="">-- Select file --</option>
                                        <option v-for="file in files" :key="file" :value="file">{{ file }}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="text-gray-700 w-1/4 md:w-1/6 p-2">
                            <div class="">
                                <button type="submit" class="btn btn-blue shadow">
                                    Search
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                </form>
            </div>
            <mg-mailscanner-configuration-table :list="config" @next="next" @previous="previous" @saved="get(query, file)"></mg-mailscanner-configuration-table>
        </div>
    </div>
</mg-page>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex';
import MailScannerConfigurationTable from '../../../components/MailScannerConfigurationTable.vue';
export default {
    data: () => {
        return {
            config: [],
            search_query: "",
            search_file: ""
        }
    },
    components: {
        'mg-mailscanner-configuration-table': MailScannerConfigurationTable
    },
    computed: {
        files() {
            let distinct = [];
            if (this.config.results) {
                for (let i = 0; i < this.config.results.length; i++) {
                    if (distinct.includes(this.config.results[i].filepath)) continue;
                    distinct[i] = this.config.results[i].filepath;
                }
            }
            return distinct;
        },
        ...mapGetters(['user'])
    },
    created() {
        this.get();
    },
    methods: {
        get(query = null, file = null, page = null) {
            this.setLoading(true);
            let qs = '';
            if (query) {
                qs = '?search='+query;
            }
            if (page) {
                qs = '?page='+page;
            }
            if (file) {
                qs = '?filename='+file;
            }
            if (query && page) {
                qs = '?search='+query+'&page='+page;
            }
            if (query && file) {
                qs = '?search='+query+'&filename='+file;
            }
            if (query && file && page) {
                qs = '?search='+query+'&filename='+file+'&page='+page;
            }

            axios.get('/api/mailscanner-configuration/'+qs).then(response => {
                this.config = response.data;
            });
            this.setLoading(false);
        },
        next() {
            if (this.config.next) {
                this.get(this.search_query, this.search_file, this.config.next.split("?page=")[1]);
            }
        },
        previous() {
            if (this.config.previous) {
                this.get(this.search_query, this.search_file, this.config.previous.split("?page=")[1]);
            }
        },
        async search() {
            await this.get(this.search_query,this.search_file);
        },
        ...mapMutations(['toggleLoading', 'setLoading'])
    }
}
</script>