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
            <div class="bg-white border sm:rounded shadow sm:w-1/2 p-2 mr-1">
                <mw-lists-table :list="whitelist"></mw-lists-table>
            </div>
            <div class="bg-white border sm:rounded shadow sm:w-1/2 p-2 ml-1">
                <mw-lists-table :list="blacklist"></mw-lists-table>
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
            search_query: "",
            blacklist: [],
            whitelist: [],
            show_modal: false,
            listing_choice_from: '',
            listing_choice_to: '',
            form: new Form({
                from_address: '',
                to_address: '',
                from_domain: '',
                to_domain: '',
                from_ip_address: '',
                to_ip_address: '',
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
        get(query = null) {
            if(!this.loading) {
                this.toggleLoading();
            }
            let qs = '';
            if (query) {
                qs = '?search='+query;
            }
            axios.get('/api/whitelist/'+qs).then(response => {
                this.whitelist = response.data;
            });
            axios.get('/api/blacklist/'+qs).then(response => {
                this.blacklist = response.data;
                this.toggleLoading();
            });
        },
        search() {
            this.get(this.search_query);
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
            });
        },
        cancel_list() {
            this.show_modal = false;
            this.form.reset();
        },
        ...mapMutations(['toggleLoading'])
    }
}
</script>