<template>
    <div class="sm:container mx-auto sm:px-2 pt-2 pb-8">
        <div class="bg-white border sm:rounded shadow p-2">
            <h2 class="font-normal text-center mb-2">Application settings</h2>
            <p class="text-center">Configure the application to your liking</p>
            <div>
                <div class="flex text-sm shadow table-wrapper">
                    <table class="table text-sm">
                        <thead>
                            <tr>
                                <th>Key</th>
                                <th>Value</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <mw-settings-item :item="item" v-for="item in config.results" :key="item.id" @saved="get(search_query)"></mw-settings-item>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import SettingsItem from '../../../components/SettingsItem.vue';
export default {
    data: () => {
        return {
            config: [],
            search_query: ""
        }
    },
    components: {
        'mw-settings-item': SettingsItem
    },
    computed: {
        ...mapGetters(['user'])
    },
    mounted() {
        this.get();
    },
    methods: {
        get(query = null, page = null) {
            this.toggleLoading();
            this.config = [];
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
            axios.get('/api/settings/'+qs).then(response => {
                this.config = response.data;
                this.toggleLoading();            
            }).catch(error => {
                this.toggleLoading();
            });                ;
        },
        async search() {
            await this.get(this.search_query);
            this.search_query = null;
        },
        ...mapMutations(['toggleLoading'])
    }
}
</script>