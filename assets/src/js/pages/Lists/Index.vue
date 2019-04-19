<template>
<mg-page>
    <div class="sm:container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex card p-2 mb-2">
            <div class="sm:w-1/2">
                <div class="p-2">
                    <button @click="show_blacklist_modal" class="btn btn-black shadow" type="button">
                        Add blacklist entry
                    </button>
                    <button @click="show_whitelist_modal" class="btn btn-gray-lightest shadow" type="button">
                        Add whitelist entry
                    </button>
                </div>
            </div>
            <div class="sm:w-1/2">
                <form @submit.prevent="search">
                    <div class="flex text-sm items-center">
                        <div class="text-gray-700 w-3/4 md:w-5/6 p-2">
                            <div class="font-semibold">
                                <input type="text" name="search" class="form-input" v-model="search_query" placeholder="Type something here..."/>
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
                </form>
            </div>
        </div>
        <div class="sm:flex mt-4 sm:pr-2">
            <div class="card sm:w-1/2 p-2 sm:mr-1">
                <h2 class="font-normal text-center border-b">Whitelist</h2>
                <mg-lists-table :list="whitelist" @next="next_whitelist" @previous="previous_whitelist" @confirmDelete="delete_entry_modal"></mg-lists-table>
            </div>
            <div class="card sm:w-1/2 p-2 sm:ml-1">
                <h2 class="font-normal text-center border-b">Blacklist</h2>
                <mg-lists-table :list="blacklist" @next="next_blacklist" @previous="previous_blacklist" @confirmDelete="delete_entry_modal"></mg-lists-table>
            </div>
        </div>
    </div>
</mg-page>
</template>
<script>
import { mapMutations, mapGetters } from 'vuex';
import Form from '../../classes/Form';
import ListsTable from '../../components/ListsTable.vue';
import Modal from '../../components/Modal.vue';
import ListEntryForm from '../../components/ListEntryForm.vue';
export default {
    components: {
        'mg-lists-table': ListsTable,
        'mg-modal': Modal,
    },
    data: () => {
        return {
            search_query: null,
            blacklist: [],
            whitelist: [],
            entry_to_delete: {},
            delete_modal: false,
        }
    },
    created() {
        this.get();
    },
    computed: {
        ...mapGetters(['loading'])
    },
    methods: {
        get(query = null) {
            this.get_whitelist(query);
            this.get_blacklist(query);
        },
        get_blacklist(query = null, page = null) {
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
            axios.get('/api/blacklist/'+qs).then(response => {
                this.blacklist = response.data;
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
            });
        },
        get_whitelist(query = null, page = null) {
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
            axios.get('/api/whitelist/'+qs).then(response => {
                this.whitelist = response.data;
                this.setLoading(false);
            }).catch(error => {
                this.setLoading(false);
            });
        },
        async search() {
            await this.get(this.search_query);
            this.search_query = null;
        },
        show_blacklist_modal() {
            this.$modal.show(ListEntryForm,{
                listingType: 'blacklisted'
            },
            {
                clickToClose: false,
                adaptive: true,
                height: 'auto'
            });
        },
        show_whitelist_modal() {
            this.$modal.show(ListEntryForm,{
                listingType: 'whitelisted'
            },
            {
                clickToClose: false,
                adaptive: true,
                height: 'auto'
            });
        },
    delete_entry_modal(item) {
        this.$modal.show('dialog', {
            title: 'Delete entry?',
            text: `Are you sure that you want to delete the ${item.listing_type} entry from ${item.from_address} to ${item.to_address }@${item.to_domain}?`,
            buttons: [
                {
                    title: 'Yes',
                    handler: () => {
                        this.setLoading(true);
                        axios.delete('/api/lists/'+item.id+'/').then(response => {
                            this.setLoading(false);
                            this.notify(this.createNotification('Entry deleted', `The ${item.listing_type} entry from ${item.from_address} to ${item.to_address }@${item.to_domain} has been deleted`, 'success'));
                        }).catch(error => {
                            this.setLoading(false);
                            this.notify(this.createNotification('An error occurred', `${error}`, 'error'));
                        });
                        this.$modal.hide('dialog');
                        this.get(this.search_query);
                    },
                    default: true
                },
                {
                    title: 'No'
                }
            ]
        });
    },
        next_whitelist(event) {
            let page = 0;
            page = this.whitelist.next.split("?page=")[1];
            this.get_whitelist(this.search_query, page);
        },
        previous_whitelist(event) {
            let page = 0;
            page = this.whitelist.previous.split("?page=")[1];
            this.get_whitelist(this.search_query, page);
        },
        next_blacklist(event) {
            let page = 0;
            page = this.blacklist.next.split("?page=")[1];
            this.get_blacklist(this.search_query, page);
        },
        previous_blacklist(event) {
            let page = 0;
            page = this.blacklist.previous.split("?page=")[1];
            this.get_blacklist(this.search_query, page);
        },
        ...mapMutations(['toggleLoading', 'setLoading', 'notify'])
    }
}
</script>