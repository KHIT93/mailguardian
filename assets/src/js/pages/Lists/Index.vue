<template>
    <div class="container mx-auto sm:px-4 pt-6 pb-8">
        <div class="sm:flex bg-white border sm:rounded shadow p-2 mb-2">
            <div class="sm:w-1/2">
                <div class="p-2">
                    <button @click="show_blacklist_modal" class="flex-no-shrink bg-black hover:bg-grey-darkest border-black hover:border-grey-darkest text-sm border-4 text-white py-1 px-2 rounded shadow" type="button">
                        Add blacklist entry
                    </button>
                    <button @click="show_whitelist_modal" class="flex-no-shrink bg-grey-lightest hover:bg-grey-lighter hover:border-grey-lighter border-grey-lightest text-sm border-4 text-black py-1 px-2 rounded shadow" type="button">
                        Add whitelist entry
                    </button>
                </div>
            </div>
            <div class="sm:w-1/2">
                <form @submit.prevent="search">
                    <div class="flex text-sm items-center">
                        <div class="text-grey-darker w-3/4 md:w-5/6 p-2">
                            <div class="font-semibold">
                                <input type="text" name="search" class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" v-model="search_query" placeholder="Type something here..."/>
                            </div>
                        </div>
                        <div class="text-grey-darker w-1/4 md:w-1/6 p-2">
                            <div class="">
                                <button type="submit" class="flex-no-shrink bg-blue hover:bg-blue-dark border-blue hover:border-blue-dark text-sm border-4 text-white py-1 px-2 rounded shadow">
                                    Search
                                </button>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div class="sm:flex">
            <div class="bg-white border sm:rounded shadow sm:w-1/2 p-2 sm:mr-1">
                <h2 class="font-normal text-center border-b">Whitelist</h2>
                <mw-lists-table :list="whitelist" @next="next_whitelist" @previous="previous_whitelist" @confirmDelete="delete_entry_modal"></mw-lists-table>
            </div>
            <div class="bg-white border sm:rounded shadow sm:w-1/2 p-2 sm:ml-1">
                <h2 class="font-normal text-center border-b">Blacklist</h2>
                <mw-lists-table :list="blacklist" @next="next_blacklist" @previous="previous_blacklist" @confirmDelete="delete_entry_modal"></mw-lists-table>
            </div>
        </div>
        <mw-modal @close="cancel_list" @submit="submit_list" :show="show_modal" :modal-title="'Add ' + form.listing_type + ' entry'">
            <form @submit.prevent="submit_list">
                <div>
                    <div class="md:flex md:items-center mb-6">
                        <div class="md:w-1/4">
                            <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="from_address">
                                I want to make a listing based on
                            </label>
                        </div>
                        <div class="md:w-3/4">
                            <div class="relative">
                                <select v-model="listing_choice_from" class="block appearance-none w-full bg-grey-lighter hover:border-blue border border-grey-lighter text-grey-darker py-2 px-4">
                                    <option value="">-- Select --</option>
                                    <option value="from_address">Senders email address or domain</option>
                                    <option value="from_ip_address">Senders IP-address</option>
                                </select>
                                <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6" v-if="listing_choice_from == 'from_address'">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="from_address">
                            From
                        </label>
                    </div>
                    <div class="md:w-3/4 inline-flex">
                        <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded py-2 px-4 text-grey-darker" name="from_address" v-model="form.from_address" id="from_address" type="email" placeholder="JaneDoe">
                        <span class="select-none bg-grey-lighter appearance-none border border-grey-lighter py-2 px-4 text-grey-darker">@</span>
                        <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue w-full rounded py-2 px-4 text-grey-darker" name="from_domain" v-model="form.from_domain" id="from_domain" type="text" placeholder="example.com">
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6" v-if="listing_choice_from == 'from_ip_address'">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="from_ip_address">
                            From
                        </label>
                    </div>
                    <div class="md:w-3/4">
                        <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="from_ip_address" v-model="form.from_ip_address" id="from_ip_address" type="text" placeholder="111.222.333.444">
                    </div>
                </div>

                <div>
                    <div class="md:flex md:items-center mb-6">
                        <div class="md:w-1/4">
                            <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="from_address">
                                I want to make a listing based on
                            </label>
                        </div>
                        <div class="md:w-3/4">
                            <div class="relative">
                                <select v-model="listing_choice_to" class="block appearance-none w-full bg-grey-lighter hover:border-blue border border-grey-lighter text-grey-darker py-2 px-4">
                                    <option value="">-- Select --</option>
                                    <option value="to_address">Recipients email address or domain</option>
                                    <option value="to_ip_address">Recipients IP-address</option>
                                </select>
                                <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6" v-if="listing_choice_to == 'to_address'">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="to_address">
                            To
                        </label>
                    </div>
                    <div class="md:w-3/4 inline-flex">
                        <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded py-2 px-4 text-grey-darker" name="to_address" v-model="form.to_address" id="to_address" type="email" placeholder="JohnDoe">
                        <span class="select-none bg-grey-lighter appearance-none border border-grey-lighter py-2 px-4 text-grey-darker">@</span>
                        <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="to_domain" v-model="form.to_domain" id="to_domain" type="text" placeholder="example.com">                    
                    </div>
                </div>

                <div class="md:flex md:items-center mb-6" v-if="listing_choice_to == 'to_ip_address'">
                    <div class="md:w-1/4">
                        <label class="block text-grey-darker font-bold md:text-right mb-1 md:mb-0 pr-4" for="to_ip_address">
                            To
                        </label>
                    </div>
                    <div class="md:w-3/4">
                        <input class="bg-grey-lighter appearance-none border border-grey-lighter hover:border-blue rounded w-full py-2 px-4 text-grey-darker" name="to_ip_address" v-model="form.to_ip_address" id="to_ip_address" type="text" placeholder="111.222.333.444">
                    </div>
                </div>
            </form>
        </mw-modal>
        <mw-modal @close="delete_entry_no" @submit="delete_entry" submit-button-text="Yes" close-button-text="No" :show="delete_modal" modal-title="Delete entry?">
            <p>Are you sure that you want to delete the {{ entry_to_delete.listing_type }} entry from {{ entry_to_delete._from }} to {{ entry_to_delete._to }}?</p>
        </mw-modal>
    </div>
</template>
<script>
import { mapMutations, mapGetters } from 'vuex';
import Form from '../../classes/Form';
import ListsTable from '../../components/ListsTable.vue';
import Modal from '../../components/Modal.vue';
export default {
    components: {
        'mw-lists-table': ListsTable,
        'mw-modal': Modal
    },
    data: () => {
        return {
            search_query: null,
            blacklist: [],
            whitelist: [],
            entry_to_delete: {},
            show_modal: false,
            delete_modal: false,
            listing_choice_from: '',
            listing_choice_to: '',
            form: new Form({
                from_address: '',
                to_address: '',
                from_domain: '',
                to_domain: '',
                from_ip_address: null,
                to_ip_address: null,
                listing_type: ''
            })
        }
    },
    mounted() {
        this.toggleLoading()
        this.get();
    },
    computed: {
        ...mapGetters(['loading'])
    },
    methods: {
        async get(query = null) {
            if(!this.loading) {
                this.toggleLoading();
            }
            await this.get_whitelist(query);
            await this.get_blacklist(query);
            this.toggleLoading();
        },
        get_blacklist(query = null, page = null) {
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
            });
        },
        get_whitelist(query = null, page = null) {
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
            });
        },
        async search() {
            await this.get(this.search_query);
            this.search_query = null;
        },
        show_blacklist_modal() {
            this.form.listing_type = 'blacklisted'
            this.show_modal = true;
        },
        show_whitelist_modal() {
            this.form.listing_type = 'whitelisted'
            this.show_modal = true;
        },
        submit_list() {
            this.toggleLoading();
            this.form.post('/api/lists/').then(() => {
                this.toggleLoading();
                this.show_modal = false;
                this.get();
            });
        },
        cancel_list() {
            this.show_modal = false;
            this.form.reset();
        },
        delete_entry_modal(item) {
            console.log(item);
            this.entry_to_delete = item;
            this.delete_modal = true;
        },
        delete_entry() {
            this.toggleLoading();
            axios.delete('/api/lists/'+this.entry_to_delete.id+'/').then(response => {
                this.toggleLoading();
                this.entry_to_delete = {};
                this.delete_modal = false;
                this.get();
            }).catch(error => {
                this.toggleLoading();
                this.entry_to_delete = {};
                this.delete_modal = false;
            });
        },
        delete_entry_no() {
            this.entry_to_delete = {};
            this.delete_modal = false;
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
        ...mapMutations(['toggleLoading'])
    }
}
</script>